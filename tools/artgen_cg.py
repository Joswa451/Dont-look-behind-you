"""Cinematic CG illustrations composited from the original art pipeline."""
from __future__ import annotations

import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance

from art_common import (
    ROOT, IMG, out, rgb, mix, radial_glow, add_screen_glow, vignette, grain,
    bloom, soft_blur, finish_bg, save, rain_layer, fog_layer,
)
from artgen_bg import dust_motes
from artgen_char import draw_character

BG = os.path.join(IMG, "backgrounds")
CH = os.path.join(IMG, "characters")
CG = os.path.join(IMG, "cg")
W, H = 1920, 1080


def bg(name):
    return Image.open(os.path.join(BG, name)).convert("RGBA")


def sprite(name, expr):
    return draw_character(name, expr)


def place(base, name, expr, scale=0.7, cx=960, bottom=H + 40, alpha=1.0,
          tint=None, tint_alpha=0.0, flip=False, brightness=1.0, contrast=1.0,
          shadow=False, blur=0.0):
    im = sprite(name, expr)
    w, h = int(im.width * scale), int(im.height * scale)
    im = im.resize((w, h), Image.LANCZOS)
    if flip:
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
    if brightness != 1.0:
        im = ImageEnhance.Brightness(im).enhance(brightness)
    if contrast != 1.0:
        im = ImageEnhance.Contrast(im).enhance(contrast)
    if tint is not None and tint_alpha > 0:
        t = Image.new("RGBA", im.size, rgb(tint) + (255,))
        t.putalpha(im.getchannel("A").point(lambda v: int(v * tint_alpha)))
        im = Image.alpha_composite(im, t)
    if alpha < 1.0:
        a = im.getchannel("A").point(lambda v: int(v * alpha))
        im.putalpha(a)
    if blur:
        im = im.filter(ImageFilter.GaussianBlur(blur))
    x = int(cx - w / 2)
    y = int(bottom - h)
    if shadow:
        sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
        sh.paste(Image.new("RGBA", im.size, (0, 0, 0, 110)), (x, y), im)
        sh = sh.filter(ImageFilter.GaussianBlur(22))
        base = Image.alpha_composite(base, sh)
    base.alpha_composite(im, (x, y))
    return base, (x, y, w, h)


def grade(img, color=(10, 8, 16), warm=0.0, contrast=1.02, saturation=1.0, brightness=1.0):
    im = img.convert("RGB")
    if warm > 0:
        im = Image.blend(im, Image.new("RGB", im.size, (255, 178, 120)), warm * 0.25)
    elif warm < 0:
        im = Image.blend(im, Image.new("RGB", im.size, (90, 130, 190)), -warm * 0.22)
    im = ImageEnhance.Color(im).enhance(saturation)
    im = ImageEnhance.Contrast(im).enhance(contrast)
    im = ImageEnhance.Brightness(im).enhance(brightness)
    return im.convert("RGBA")


def glitch(img, seed=1, strength=1.0, bars=20):
    rng = random.Random(seed)
    im = img.convert("RGBA")
    w, h = im.size
    out_im = im.copy()
    for _ in range(bars):
        y = rng.randrange(h)
        bh = rng.randrange(2, 16)
        dx = int(rng.uniform(-40, 40) * strength)
        strip = im.crop((0, y, w, min(h, y + bh)))
        out_im.alpha_composite(strip, (dx, y))
    # chromatic offset
    arr = np.array(out_im.convert("RGB"), dtype=np.uint8, copy=True)
    r = np.roll(arr[:, :, 0], int(3 * strength), axis=1)
    b = np.roll(arr[:, :, 2], -int(3 * strength), axis=1)
    arr[:, :, 0] = r
    arr[:, :, 2] = b
    out_im = Image.fromarray(arr, "RGB").convert("RGBA")
    # colored bars
    d = ImageDraw.Draw(out_im)
    for _ in range(int(3 * strength)):
        y = rng.randrange(h)
        d.rectangle([0, y, w, y + rng.randrange(2, 7)], fill=(190, 26, 40, rng.randrange(40, 120)))
    return out_im


def film_border(img, size=26):
    w, h = img.size
    l = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(l)
    d.rectangle([0, 0, w, size], fill=(0, 0, 0, 230))
    d.rectangle([0, h - size, w, h], fill=(0, 0, 0, 230))
    d.rectangle([0, 0, size, h], fill=(0, 0, 0, 180))
    d.rectangle([w - size, 0, w, h], fill=(0, 0, 0, 180))
    return Image.alpha_composite(img, l)


def finish(img, vig=0.78, gr=0.05, bl=0.4, seed=4):
    im = img.convert("RGB")
    im = bloom(im, 170, 25, bl)
    im = vignette(im, vig)
    im = grain(im, gr, seed)
    return im


def hand_on_mirror(img, x, y, scale=1.0, color=(210, 205, 205), alpha=42):
    l = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(l)
    s = scale
    d.ellipse([x - 46 * s, y - 58 * s, x + 46 * s, y + 58 * s], fill=color + (alpha,))
    for i, (ox, oy, ln) in enumerate([(-32, -52, 46), (-10, -66, 58), (14, -64, 54), (36, -52, 42), (48, 10, 36)]):
        d.rounded_rectangle([x + ox * s - 9 * s, y + oy * s, x + ox * s + 9 * s, y + oy * s + ln * s],
                            radius=9 * s, fill=color + (alpha,))
    l = l.filter(ImageFilter.GaussianBlur(3))
    return Image.alpha_composite(img, l)


def silhouette_adult(base, cx, bottom, height, color=(10, 8, 12), alpha=210, female=True, blur=2):
    w = int(height * 0.42)
    l = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(l)
    hw = int(height * 0.10)
    # head
    d.ellipse([cx - hw, bottom - height, cx + hw, bottom - height + hw * 2.1], fill=color + (alpha,))
    # neck
    d.rectangle([cx - hw * 0.35, bottom - height + hw * 1.8, cx + hw * 0.35, bottom - height + hw * 2.6], fill=color + (alpha,))
    # shoulders / body
    top = bottom - height + hw * 2.2
    if female:
        d.polygon([(cx - w * 0.45, bottom), (cx - w * 0.34, top), (cx - w * 0.12, top - hw * 0.2),
                   (cx + w * 0.12, top - hw * 0.2), (cx + w * 0.34, top), (cx + w * 0.45, bottom)], fill=color + (alpha,))
    else:
        d.polygon([(cx - w * 0.5, bottom), (cx - w * 0.38, top), (cx - w * 0.12, top - hw * 0.3),
                   (cx + w * 0.12, top - hw * 0.3), (cx + w * 0.38, top), (cx + w * 0.5, bottom)], fill=color + (alpha,))
    if blur:
        l = l.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(base, l)


def phone_overlay(base, x, y, scale=1.0):
    l = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(l)
    w, h = int(150 * scale), int(290 * scale)
    d.rounded_rectangle([x, y, x + w, y + h], radius=int(20 * scale), fill=(8, 8, 10, 245), outline=(90, 86, 88, 255), width=max(2, int(3 * scale)))
    d.rounded_rectangle([x + 10 * scale, y + 22 * scale, x + w - 10 * scale, y + h - 30 * scale], radius=int(9 * scale), fill=(24, 30, 36, 255))
    # screen glow / caller
    d.ellipse([x + w * 0.30, y + h * 0.24, x + w * 0.70, y + h * 0.52], fill=(30, 42, 50, 255))
    d.text((x + 18 * scale, y + h * 0.60), "UNKNOWN", fill=(195, 190, 175, 230))
    d.text((x + 18 * scale, y + h * 0.70), "03:00", fill=(180, 50, 55, 230))
    l = l.filter(ImageFilter.GaussianBlur(0.4))
    out_im = Image.alpha_composite(base, l)
    out_im = Image.alpha_composite(out_im, radial_glow(base.size, (x + w / 2, y + h / 2), 260, (90, 140, 160), 70, 2.0))
    return out_im


# ---------------------------------------------------------------------------
def cg_girl_first():
    im = bg("bg_hallway.jpg")
    im = grade(im, warm=-0.5, contrast=1.06, saturation=0.8, brightness=0.82)
    # distant girl, cold backlight
    im, _ = place(im, "girl", "neutral", scale=0.50, cx=1000, bottom=880, alpha=0.96,
                  tint="#9fb7d6", tint_alpha=0.10, brightness=1.1, contrast=1.05, shadow=True)
    im = Image.alpha_composite(im, radial_glow(im.size, (1000, 520), 520, (110, 140, 180), 55, 2.2))
    # red glow from the ajar door
    im = Image.alpha_composite(im, radial_glow(im.size, (470, 640), 300, (150, 30, 36), 50, 2.2))
    im = soft_blur(im.convert("RGB"), 0.5).convert("RGBA")
    im = finish(im, 0.82, 0.055, 0.42, seed=2)
    save(im, os.path.join(CG, "cg_girl_first.jpg"))


def cg_jumpscare():
    im = sprite("entity", "evil")
    # crop face / shoulders
    crop = im.crop((0, 210, 900, 716)).resize((W, H), Image.LANCZOS)
    crop = grade(crop, warm=-0.2, contrast=1.35, saturation=0.7, brightness=0.62)
    crop = glitch(crop, seed=7, strength=1.2, bars=26)
    # white-hot eyes
    for ex, scale in [(640, 1.0), (1210, 1.0)]:
        crop = Image.alpha_composite(crop, radial_glow((W, H), (ex, 480), 170, (255, 246, 222), 130, 2.2))
    # blood-red vignette + scanlines
    arr_im = crop.convert("RGB")
    im2 = add_screen_glow(arr_im, (960, 480), 900, (120, 10, 18), 90)
    l = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(l)
    for y in range(0, H, 4):
        d.line([(0, y), (W, y)], fill=(0, 0, 0, 38), width=1)
    im2 = Image.alpha_composite(im2.convert("RGBA"), l)
    im2 = film_border(im2, 12)
    im2 = finish(im2, 0.9, 0.075, 0.5, seed=9)
    save(im2, os.path.join(CG, "cg_jumpscare.jpg"))


def cg_mirror():
    base = bg("bg_bathroom.jpg")
    base = grade(base, warm=-0.6, contrast=1.1, saturation=0.72, brightness=0.8)
    # mirror reflection of Ethan, wrong expression
    mirror = (748, 158, 1232, 542)
    refl = sprite("ethan", "evil")
    mw = mirror[2] - mirror[0]
    mh = mirror[3] - mirror[1]
    rw = int(mw * 1.25)
    rh = int(rw * 1500 / 900)
    refl = refl.resize((rw, rh), Image.LANCZOS).transpose(Image.FLIP_LEFT_RIGHT)
    canvas = Image.new("RGBA", (mw, mh), (0, 0, 0, 0))
    canvas.alpha_composite(refl, (int(mw / 2 - rw / 2), int(mh - rh + 110)))
    mask = Image.new("L", (mw, mh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, mw, mh], radius=6, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(10))
    canvas.putalpha(ImageChops.multiply(canvas.getchannel("A"), mask))
    # tint reflection cold and dim
    t = Image.new("RGBA", canvas.size, (45, 65, 75, 255))
    t.putalpha(canvas.getchannel("A").point(lambda v: int(v * 0.30)))
    canvas = Image.alpha_composite(canvas, t)
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    layer.alpha_composite(canvas, (mirror[0], mirror[1]))
    base = Image.alpha_composite(base, layer)
    # Ethan foreground, back to us-ish / scared
    base, _ = place(base, "ethan", "scared", scale=0.92, cx=520, bottom=1150, brightness=0.8, contrast=1.05, shadow=True)
    # hand pressed against mirror
    base = hand_on_mirror(base, 905, 430, scale=1.3, alpha=48)
    # entity barely there in mirror
    lay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ent = sprite("entity", "evil")
    ew, eh = 330, 550
    ent = ent.resize((ew, eh), Image.LANCZOS)
    ent.putalpha(ent.getchannel("A").point(lambda v: int(v * 0.16)))
    lay.alpha_composite(ent, (830, 120))
    base = Image.alpha_composite(base, lay)
    # crack the mirror
    d = ImageDraw.Draw(base)
    rng = random.Random(4)
    for i in range(5):
        x, y = 1000, 320
        pts = [(x, y)]
        for _ in range(7):
            x += rng.uniform(-80, 80)
            y += rng.uniform(-70, 70)
            pts.append((x, y))
        d.line(pts, fill=(5, 8, 9, 120), width=2)
    base = glitch(base, seed=3, strength=0.35, bars=5)
    base = finish(base, 0.85, 0.055, 0.4, seed=4)
    save(base, os.path.join(CG, "cg_mirror.jpg"))


def cg_hidden_room():
    base = bg("bg_hiddenroom.jpg")
    base = grade(base, warm=0.2, contrast=1.1, saturation=0.82, brightness=0.9)
    base, _ = place(base, "ethan", "surprised", scale=0.66, cx=560, bottom=1120,
                    brightness=0.85, contrast=1.05, shadow=True)
    base, _ = place(base, "maya", "scared", scale=0.62, cx=1340, bottom=1120,
                    brightness=0.82, contrast=1.05, shadow=True)
    # flashlight cones
    l = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(l)
    d.polygon([(560, 800), (760, 760), (1120, 250), (900, 220)], fill=(240, 216, 160, 34))
    d.polygon([(1300, 800), (1400, 770), (1490, 300), (1330, 280)], fill=(240, 216, 160, 26))
    l = l.filter(ImageFilter.GaussianBlur(30))
    base = Image.alpha_composite(base, l)
    base = add_screen_glow(base.convert("RGB"), (1040, 350), 650, (220, 160, 80), 45).convert("RGBA")
    # highlight the drawings / red string
    base = Image.alpha_composite(base, radial_glow(base.size, (1000, 300), 420, (150, 40, 40), 36, 2.1))
    base = finish(base, 0.8, 0.06, 0.42, seed=5)
    save(base, os.path.join(CG, "cg_hidden_room.jpg"))


def cg_parents():
    base = bg("bg_livingroom.jpg")
    base = grade(base, warm=0.15, contrast=1.12, saturation=0.72, brightness=0.55)
    # old camcorder frame
    l = Image.new("RGBA", base.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(l)
    d.rectangle([150, 90, 1770, 990], outline=(210, 205, 185, 90), width=6)
    d.rectangle([190, 130, 1730, 950], outline=(190, 185, 170, 40), width=2)
    d.text((210, 110), "PLAY  \u25b6", fill=(225, 220, 200, 170))
    d.text((1550, 110), "REC 00:03:00", fill=(185, 45, 45, 200))
    d.line([(210, 950), (210, 980)], fill=(200, 195, 175, 120), width=2)
    d.line([(500, 950), (500, 980)], fill=(200, 195, 175, 120), width=2)
    d.line([(210, 970), (500, 970)], fill=(200, 195, 175, 120), width=2)
    base = Image.alpha_composite(base, l)

    # ghostly parents
    base = silhouette_adult(base, 780, 930, 680, color=(20, 16, 22), alpha=205, female=False, blur=2)
    base = silhouette_adult(base, 1140, 920, 630, color=(22, 17, 23), alpha=205, female=True, blur=2)
    # warm rim / faint faces
    for cx, cy in [(780, 300), (1140, 330)]:
        base = Image.alpha_composite(base, radial_glow(base.size, (cx, cy), 90, (220, 180, 120), 26, 2.2))

    # Ethan in foreground, tears - seeing them again
    base, _ = place(base, "ethan", "crying", scale=0.95, cx=1490, bottom=1220, brightness=0.62,
                    contrast=1.06, tint="#b06a5a", tint_alpha=0.14, shadow=True)
    # tv static / tape artifacts
    rng = random.Random(5)
    d = ImageDraw.Draw(base)
    for _ in range(160):
        x = rng.uniform(150, 1770)
        y = rng.uniform(90, 990)
        d.point((x, y), fill=(220, 215, 200, rng.randint(10, 55)))
    base = glitch(base, seed=10, strength=0.18, bars=4)
    im = finish(base, 0.85, 0.09, 0.36, seed=6)
    # desaturate slightly / old film
    im = ImageEnhance.Color(im).enhance(0.72)
    save(im, os.path.join(CG, "cg_parents.jpg"))


def cg_bargain_flashback():
    """The parents' bargain, remembered through the hidden-room recording."""
    base = bg("bg_hiddenroom.jpg")
    base = grade(base, warm=-0.35, contrast=1.10, saturation=0.68, brightness=0.82)
    base = Image.alpha_composite(base, radial_glow(base.size, (970, 520), 620, (132, 34, 40), 65, 2.0))

    # Their faces stay readable while the room falls away into smoke and shadow.
    base, _ = place(base, "mom", "crying", scale=0.72, cx=720, bottom=1120,
                    brightness=0.78, tint="#b64a4f", tint_alpha=0.10, shadow=True)
    base, _ = place(base, "dad", "sad", scale=0.72, cx=1190, bottom=1120,
                    brightness=0.78, tint="#b64a4f", tint_alpha=0.10, shadow=True)

    # A child-sized hand and the music box mark the price of the bargain.
    d = ImageDraw.Draw(base)
    d.rounded_rectangle([810, 845, 1110, 1005], radius=22,
                        fill=(22, 20, 24, 235), outline=(154, 126, 90, 210), width=5)
    d.rectangle([842, 872, 1078, 978], outline=(93, 78, 66, 190), width=3)
    d.ellipse([927, 905, 993, 971], outline=(184, 148, 99, 210), width=4)
    d.line([(960, 922), (960, 951)], fill=(191, 162, 112, 220), width=3)
    # A fine red thread runs from the box toward the sealed door.
    d.line([(960, 850), (955, 650), (825, 420), (770, 270)],
           fill=(180, 37, 45, 145), width=3)

    base = Image.alpha_composite(base, fog_layer(base.size, (142, 126, 132), 34, seed=41, scale=3.5))
    base = glitch(base, seed=32, strength=0.14, bars=3)
    save(finish(base, 0.86, 0.07, 0.42, seed=14), os.path.join(CG, "cg_bargain_flashback.jpg"))


def cg_confrontation():
    base = bg("bg_void.jpg")
    base = grade(base, contrast=1.12, saturation=0.95, brightness=0.9)
    # rift
    base = Image.alpha_composite(base, radial_glow(base.size, (960, 470), 520, (180, 30, 40), 90, 2.1))
    # entity
    base, box = place(base, "entity", "evil", scale=1.34, cx=960, bottom=1330, brightness=0.95, contrast=1.15, shadow=True)
    # girl behind / side
    base, _ = place(base, "girl", "sad", scale=0.72, cx=1480, bottom=1120, alpha=0.9,
                    tint="#8e9cb6", tint_alpha=0.10, brightness=0.95, shadow=True)
    # Ethan foreground, small and scared
    base, _ = place(base, "ethan", "scared", scale=0.78, cx=430, bottom=1160, brightness=0.85,
                    contrast=1.08, shadow=True)
    # red threads
    d = ImageDraw.Draw(base)
    rng = random.Random(6)
    for i in range(18):
        x = rng.randint(200, 1700)
        pts = [(x, 1080)]
        for _ in range(5):
            x += rng.randint(-90, 90)
            pts.append((x, rng.randint(200, 900)))
        d.line(pts, fill=(160, 24, 34, rng.randint(30, 80)), width=rng.randint(1, 3))
    base = glitch(base, seed=12, strength=0.45, bars=8)
    base = finish(base, 0.88, 0.07, 0.5, seed=7)
    save(base, os.path.join(CG, "cg_confrontation.jpg"))


def cg_ending_truth():
    base = bg("bg_street.jpg")
    # dawn grade
    base = grade(base, warm=0.7, contrast=1.02, saturation=0.9, brightness=1.35)
    base = add_screen_glow(base.convert("RGB"), (1500, 160), 900, (255, 200, 150), 100).convert("RGBA")
    base = Image.alpha_composite(base, radial_glow(base.size, (1500, 140), 620, (255, 224, 180), 75, 2.2))
    # faint parents walking away into light
    base = silhouette_adult(base, 1330, 860, 420, color=(255, 242, 226), alpha=55, female=False, blur=6)
    base = silhouette_adult(base, 1460, 850, 390, color=(255, 242, 226), alpha=50, female=True, blur=6)
    # Ethan and Iris
    base, _ = place(base, "ethan", "sad", scale=0.70, cx=720, bottom=1120, brightness=1.02, shadow=True)
    base, _ = place(base, "girl", "happy", scale=0.66, cx=1030, bottom=1120, alpha=0.82,
                    tint="#fff3df", tint_alpha=0.10, brightness=1.15, shadow=True)
    base = Image.alpha_composite(base, radial_glow(base.size, (1030, 560), 430, (255, 248, 232), 55, 2.2))
    # petals
    d = ImageDraw.Draw(base)
    rng = random.Random(8)
    for _ in range(60):
        x = rng.uniform(0, W)
        y = rng.uniform(0, H)
        r = rng.uniform(2, 5)
        d.ellipse([x - r, y - r, x + r, y + r], fill=(255, 246, 232, rng.randint(30, 120)))
    im = finish(base, 0.55, 0.045, 0.4, seed=8)
    save(im, os.path.join(CG, "cg_ending_truth.jpg"))


def cg_ending_alone():
    base = bg("bg_bedroom.png")
    base = grade(base, warm=-0.3, contrast=1.12, saturation=0.7, brightness=0.72)
    # entity looming behind Ethan
    base, _ = place(base, "entity", "evil", scale=1.5, cx=960, bottom=1370, alpha=0.9,
                    tint="#6d1018", tint_alpha=0.10, brightness=0.85, shadow=True)
    base, _ = place(base, "ethan", "evil", scale=0.92, cx=760, bottom=1200, brightness=0.8,
                    contrast=1.08, shadow=True)
    # new tenant at the door, faceless silhouette
    base = silhouette_adult(base, 1700, 950, 560, color=(7, 7, 10), alpha=235, female=False, blur=1)
    # the phone glowing on the floor
    base = phone_overlay(base, 360, 760, scale=1.05)
    base = Image.alpha_composite(base, radial_glow(base.size, (960, 380), 600, (120, 16, 24), 60, 2.2))
    im = finish(base, 0.88, 0.06, 0.36, seed=9)
    save(im, os.path.join(CG, "cg_ending_alone.jpg"))


def cg_ending_call():
    base = bg("bg_bathroom.jpg")
    base = grade(base, warm=-0.45, contrast=1.12, saturation=0.7, brightness=0.7)
    # Ethan in the foreground, phone raised
    base, _ = place(base, "ethan", "shocked", scale=0.92, cx=520, bottom=1180, brightness=0.82,
                    contrast=1.1, shadow=True)
    base = phone_overlay(base, 320, 480, scale=1.15)
    # his reflection is the wrong one - already smiling
    mirror = (748, 158, 1232, 542)
    mw, mh = mirror[2] - mirror[0], mirror[3] - mirror[1]
    refl = sprite("ethan", "evil")
    rw = int(mw * 1.30)
    rh = int(rw * 1500 / 900)
    refl = refl.resize((rw, rh), Image.LANCZOS).transpose(Image.FLIP_LEFT_RIGHT)
    canvas = Image.new("RGBA", (mw, mh), (0, 0, 0, 0))
    canvas.alpha_composite(refl, (int(mw / 2 - rw / 2), int(mh - rh + 100)))
    mask = Image.new("L", (mw, mh), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, mw, mh], radius=8, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(8))
    canvas.putalpha(ImageChops.multiply(canvas.getchannel("A"), mask))
    lay = Image.new("RGBA", base.size, (0, 0, 0, 0))
    lay.alpha_composite(canvas, (mirror[0], mirror[1]))
    base = Image.alpha_composite(base, lay)
    # green phone glow, glitch
    base = add_screen_glow(base.convert("RGB"), (960, 500), 450, (90, 150, 130), 50).convert("RGBA")
    base = glitch(base, seed=15, strength=0.65, bars=12)
    base = finish(base, 0.86, 0.06, 0.42, seed=10)
    save(base, os.path.join(CG, "cg_ending_call.jpg"))


def cg_ending_newgame():
    base = bg("bg_hallway.jpg")
    base = grade(base, warm=-0.25, contrast=1.08, saturation=0.85, brightness=0.85)
    # a new tenant with a suitcase
    base = silhouette_adult(base, 860, 980, 520, color=(9, 9, 13), alpha=240, female=False, blur=1)
    d = ImageDraw.Draw(base)
    d.rectangle([760, 820, 880, 980], fill=(25, 22, 24, 255))
    d.rectangle([784, 820, 796, 852], outline=(90, 80, 70, 255), width=4)
    # girl waiting at the end of the hall
    base, _ = place(base, "girl", "neutral", scale=0.42, cx=1040, bottom=830, alpha=0.88,
                    tint="#9bacc8", tint_alpha=0.12, brightness=1.1, shadow=True)
    # looping frame borders (new game +)
    l = Image.new("RGBA", base.size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(l)
    for i in range(4):
        inset = 40 + i * 26
        dd.rectangle([inset, inset, W - inset, H - inset], outline=(190, 188, 180, max(10, 70 - i * 15)), width=2)
    base = Image.alpha_composite(base, l)
    base = glitch(base, seed=21, strength=0.28, bars=6)
    im = finish(base, 0.84, 0.06, 0.4, seed=11)
    save(im, os.path.join(CG, "cg_ending_newgame.jpg"))


def make_all():
    cg_girl_first()
    cg_jumpscare()
    cg_mirror()
    cg_hidden_room()
    cg_parents()
    cg_bargain_flashback()
    cg_confrontation()
    cg_ending_truth()
    cg_ending_alone()
    cg_ending_call()
    cg_ending_newgame()


if __name__ == "__main__":
    make_all()
