"""UI art: logo, dialogue box, buttons, phone, overlays and particles."""
from __future__ import annotations

import math
import os
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

from art_common import (
    out, rgb, mix, vertical_gradient, radial_glow, noise, grain, vignette,
    make_dust_sprite, make_glitch_strip, save, IMG, ROOT,
)

FONTS = os.path.join(ROOT, "game", "fonts")
CINZEL = os.path.join(FONTS, "Cinzel.ttf")
GARA = os.path.join(FONTS, "CormorantGaramond.ttf")
GARAMOND = os.path.join(FONTS, "EBGaramond.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def logo():
    W, H = 1460, 560
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # title mask
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    f1 = font(CINZEL, 168)
    f2 = font(CINZEL, 138)
    line1 = "DON'T LOOK"
    line2 = "BEHIND YOU"
    b1 = d.textbbox((0, 0), line1, font=f1)
    b2 = d.textbbox((0, 0), line2, font=f2)
    x1 = (W - (b1[2] - b1[0])) // 2
    x2 = (W - (b2[2] - b2[0])) // 2
    d.text((x1, 30), line1, font=f1, fill=255)
    d.text((x2, 190), line2, font=f2, fill=255)
    # grunge: erode with noise and scratches
    m = np.array(mask, dtype=np.float32)
    n = noise((W, H), scale=3.2, seed=4, octaves=4)
    erode = np.clip((n - 0.22) * 1.8, 0, 1)
    m = m * (0.55 + 0.45 * erode)
    # occasional horizontal cuts
    rng = random.Random(5)
    for _ in range(70):
        y = rng.randrange(H)
        th = rng.randrange(1, 4)
        x0 = rng.randrange(W)
        ln = rng.randrange(20, 220)
        m[y:y + th, x0:x0 + ln] *= rng.uniform(0.0, 0.5)
    mask = Image.fromarray(np.clip(m, 0, 255).astype(np.uint8), "L")

    # glow
    glow = mask.filter(ImageFilter.GaussianBlur(22))
    gl = Image.new("RGBA", (W, H), (130, 18, 28, 0))
    gl.putalpha(glow.point(lambda v: int(v * 0.55)))
    im = Image.alpha_composite(im, gl)

    # red offset behind
    red = Image.new("RGBA", (W, H), (115, 18, 26, 235))
    red.putalpha(mask.point(lambda v: int(v * 0.9)))
    im.alpha_composite(red, (7, 4))
    cyan = Image.new("RGBA", (W, H), (25, 45, 58, 140))
    cyan.putalpha(mask.point(lambda v: int(v * 0.6)))
    im.alpha_composite(cyan, (-4, 2))

    # main text
    main = Image.new("RGBA", (W, H), (228, 221, 208, 255))
    main.putalpha(mask)
    im = Image.alpha_composite(im, main)
    # dark red inner gradient
    grad = vertical_gradient((W, H), (245, 240, 226), (154, 142, 128)).convert("RGBA")
    tinted = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    tinted.paste(grad, (0, 0), mask)
    im = Image.alpha_composite(im, tinted)

    # thin red line + subtitle
    d = ImageDraw.Draw(im)
    d.line([(330, 380), (1130, 380)], fill=(150, 28, 34, 220), width=2)
    d.line([(400, 390), (1060, 390)], fill=(150, 28, 34, 80), width=1)
    fs = font(GARAMOND, 44)
    sub = "A   P S Y C H O L O G I C A L   H O R R O R"
    bb = d.textbbox((0, 0), sub, font=fs)
    d.text(((W - (bb[2] - bb[0])) // 2, 400), sub, font=fs, fill=(176, 168, 154, 220))
    fs2 = font(GARAMOND, 30)
    sub2 = "seven nights. one voice. do not turn around."
    bb = d.textbbox((0, 0), sub2, font=fs2)
    d.text(((W - (bb[2] - bb[0])) // 2, 465), sub2, font=fs2, fill=(126, 120, 114, 200))
    save(im, out("ui", "logo.png"))


def textbox():
    W, H = 1920, 380
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    arr = np.zeros((H, W, 4), dtype=np.uint8)
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    a = (np.clip((yy - 0.08) / 0.92, 0, 1) ** 1.3 * 232).astype(np.uint8)
    arr[..., 0] = 9
    arr[..., 1] = 8
    arr[..., 2] = 11
    arr[..., 3] = np.repeat(a, W, axis=1)
    im = Image.fromarray(arr, "RGBA")
    # reddish top hairline
    d = ImageDraw.Draw(im)
    d.line([(60, 44), (W - 60, 44)], fill=(126, 26, 32, 190), width=2)
    d.line([(60, 50), (W - 60, 50)], fill=(60, 18, 22, 90), width=1)
    # grunge speckles
    rng = random.Random(7)
    for _ in range(420):
        x = rng.uniform(40, W - 40)
        y = rng.uniform(40, H - 20)
        d.point((x, y), fill=(150, 140, 130, rng.randint(4, 22)))
    # edge fade
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).rectangle([0, 40, W, H], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(10))
    im.putalpha(ImageChops.multiply(im.getchannel("A"), mask))
    save(im, out("ui", "textbox.png"))


def namebox():
    W, H = 640, 92
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(0, 0), (W - 40, 0), (W, H - 18), (0, H - 4)], fill=(20, 17, 20, 238))
    d.polygon([(0, 0), (14, 0), (14, H - 4), (0, H - 4)], fill=(141, 28, 35, 255))
    d.line([(20, H - 8), (W - 50, H - 18)], fill=(132, 26, 32, 120), width=2)
    for i in range(30):
        x = random.Random(i).uniform(30, W - 50)
        y = random.Random(i + 9).uniform(8, H - 16)
        d.point((x, y), fill=(210, 200, 185, random.Random(i + 20).randint(10, 40)))
    save(im, out("ui", "namebox.png"))


def button(name, hover=False):
    W, H = 560, 82
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if hover:
        d.polygon([(0, 0), (W - 26, 0), (W, H - 12), (0, H)], fill=(80, 20, 26, 160))
        d.polygon([(0, 0), (10, 0), (10, H), (0, H)], fill=(198, 42, 52, 255))
        d.line([(14, H - 12), (W - 30, H - 12)], fill=(180, 44, 52, 130), width=2)
        for i in range(6):
            d.line([(14 + i * 18, H - 14 - i), (60 + i * 18, H - 14 - i)], fill=(220, 80, 84, 60), width=1)
    else:
        d.polygon([(0, 0), (W - 26, 0), (W, H - 12), (0, H)], fill=(12, 11, 14, 120))
        d.polygon([(0, 0), (7, 0), (7, H), (0, H)], fill=(108, 24, 30, 210))
        d.line([(12, H - 10), (W - 30, H - 10)], fill=(92, 26, 32, 80), width=1)
    save(im, out("ui", "button_hover.png" if hover else "button_idle.png"))


def choice_button(name, hover=False):
    W, H = 1240, 96
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if hover:
        d.polygon([(26, 0), (W - 20, 0), (W, H - 10), (0, H)], fill=(64, 17, 23, 200))
        d.rectangle([0, H - 5, W, H], fill=(158, 32, 42, 200))
        d.rectangle([0, 0, 5, H], fill=(198, 42, 52, 255))
    else:
        d.polygon([(26, 0), (W - 20, 0), (W, H - 10), (0, H)], fill=(10, 9, 12, 205))
        d.rectangle([0, H - 4, W, H], fill=(90, 24, 30, 120))
        d.rectangle([0, 0, 3, H], fill=(120, 26, 33, 200))
    # grunge
    for i in range(50):
        x = random.Random(i + (100 if hover else 0)).uniform(20, W - 30)
        y = random.Random(i + 4).uniform(4, H - 8)
        d.point((x, y), fill=(190, 180, 170, random.Random(i + 2).randint(5, 22)))
    save(im, out("ui", "choice_hover.png" if hover else "choice_idle.png"))


def phone_frame():
    W, H = 760, 1240
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # body
    d.rounded_rectangle([0, 0, W, H], radius=54, fill=(9, 9, 12, 250), outline=(82, 78, 82, 255), width=4)
    d.rounded_rectangle([8, 8, W - 8, H - 8], radius=48, outline=(35, 33, 38, 255), width=3)
    # screen
    d.rounded_rectangle([28, 30, W - 28, H - 60], radius=34, fill=(12, 15, 18, 252))
    d.rounded_rectangle([28, 30, W - 28, H - 60], radius=34, outline=(52, 50, 56, 255), width=2)
    # notch / speaker
    d.rounded_rectangle([W / 2 - 70, 38, W / 2 + 70, 58], radius=12, fill=(4, 4, 6, 255))
    d.ellipse([W / 2 - 12, 42, W / 2 - 2, 52], fill=(26, 30, 34, 255))
    # home bar
    d.rounded_rectangle([W / 2 - 60, H - 42, W / 2 + 60, H - 34], radius=4, fill=(74, 70, 70, 255))
    # screen grid / vignette
    screen = im.crop((28, 30, W - 28, H - 60))
    arr = np.array(screen, dtype=np.uint8, copy=True)
    yy, xx = np.mgrid[0:arr.shape[0], 0:arr.shape[1]].astype(np.float32)
    cx, cy = arr.shape[1] / 2, arr.shape[0] / 2
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / max(cx, cy)
    shade = np.clip(dist * 0.25, 0, 0.3)
    for c in range(3):
        arr[..., c] = (arr[..., c] * (1 - shade)).astype(np.uint8)
    screen = Image.fromarray(arr, "RGBA")
    im.paste(screen, (28, 30))
    # red recording light
    d = ImageDraw.Draw(im)
    d.ellipse([W - 74, H - 50, W - 62, H - 38], fill=(160, 32, 38, 220))
    # subtle scratches
    rng = random.Random(4)
    for _ in range(60):
        x = rng.uniform(30, W - 30)
        y = rng.uniform(30, H - 60)
        d.point((x, y), fill=(170, 160, 150, rng.randint(4, 20)))
    save(im, out("ui", "phone_frame.png"))


def overlays():
    W, H = 1920, 1080
    # vignette
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.62)) ** 2)
    a = np.clip((d - 0.52) / 0.9, 0, 1) ** 1.2 * 235
    arr = np.zeros((H, W, 4), dtype=np.uint8)
    arr[..., 3] = a.astype(np.uint8)
    save(Image.fromarray(arr, "RGBA"), out("effects", "vignette.png"))
    # scanlines
    arr = np.zeros((H, W, 4), dtype=np.uint8)
    arr[::4, :, 3] = 30
    arr[::4, :, 0:3] = 0
    save(Image.fromarray(arr, "RGBA"), out("effects", "scanlines.png"))
    # subtle bottom shadow
    arr = np.zeros((H, W, 4), dtype=np.uint8)
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    arr[..., 0] = 0
    arr[..., 1] = 0
    arr[..., 2] = 0
    arr[..., 3] = np.repeat((np.clip((yy - 0.7) / 0.3, 0, 1) ** 1.5 * 150).astype(np.uint8), W, axis=1)
    save(Image.fromarray(arr, "RGBA"), out("effects", "bottom_shadow.png"))
    # glitch screens
    for i, seed in enumerate((1, 2)):
        g = make_glitch_strip((W, H), seed, color=(170, 24, 34), bars=26)
        # add large offset slices
        rgba = np.array(g, dtype=np.uint8, copy=True)
        rng = random.Random(seed)
        for _ in range(8):
            y = rng.randrange(H - 80)
            h = rng.randrange(20, 80)
            rgba[y:y + h, :, 0] = np.roll(rgba[y:y + h, :, 0], rng.randint(-30, 30), axis=1)
        g = Image.fromarray(rgba, "RGBA")
        save(g, out("effects", f"glitch_{i+1}.png"))
    # particles
    save(make_dust_sprite(26, (235, 230, 215)), out("effects", "particle.png"))
    save(make_dust_sprite(58, (220, 214, 200)), out("effects", "particle_big.png"))
    # sanity eye icon
    ic = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    d = ImageDraw.Draw(ic)
    d.arc([6, 22, 90, 74], 180, 360, fill=(198, 66, 66, 255), width=5)
    d.arc([6, 42, 90, 94], 0, 180, fill=(198, 66, 66, 255), width=5)
    d.ellipse([30, 34, 66, 70], outline=(214, 92, 92, 255), width=4)
    d.ellipse([40, 44, 56, 60], fill=(214, 92, 92, 255))
    save(ic, out("ui", "sanity_icon.png"))
    # gallery lock
    gl = Image.new("RGBA", (640, 360), (0, 0, 0, 0))
    d = ImageDraw.Draw(gl)
    d.rectangle([0, 0, 640, 360], fill=(10, 10, 13, 255), outline=(62, 56, 60, 255), width=3)
    for i in range(20):
        d.line([(0, i * 22), (640, i * 22 - 40)], fill=(20, 20, 25, 120), width=1)
    d.rounded_rectangle([280, 130, 360, 230], radius=12, outline=(118, 112, 108, 180), width=6)
    d.arc([280, 80, 360, 180], 180, 360, fill=(118, 112, 108, 180), width=6)
    d.ellipse([312, 170, 328, 186], fill=(140, 32, 40, 220))
    d.text((252, 250), "LOCKED", fill=(120, 112, 108, 180))
    save(gl, out("ui", "gallery_locked.png"))
    # ending silhouette strip
    save(make_dust_sprite(12, (200, 40, 50)), out("effects", "ember.png"))
    # arrow glyph
    ar = Image.new("RGBA", (40, 40), (0, 0, 0, 0))
    d = ImageDraw.Draw(ar)
    d.polygon([(8, 8), (32, 20), (8, 32), (14, 20)], fill=(210, 80, 80, 220))
    save(ar, out("ui", "arrow.png"))


def ending_seal():
    W, H = 760, 260
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.line([(40, 30), (W - 40, 30)], fill=(120, 26, 32, 180), width=2)
    d.line([(40, H - 30), (W - 40, H - 30)], fill=(120, 26, 32, 180), width=2)
    f = font(CINZEL, 76)
    txt = "END"
    bb = d.textbbox((0, 0), txt, font=f)
    d.text(((W - (bb[2] - bb[0])) / 2, 60), txt, font=f, fill=(210, 200, 186, 230))
    d.text((W / 2 - 90, 170), "DON'T LOOK BEHIND YOU", fill=(130, 122, 116, 180))
    save(im, out("ui", "ending_seal.png"))


if __name__ == "__main__":
    logo()
    textbox()
    namebox()
    button("idle", False)
    button("hover", True)
    choice_button("idle", False)
    choice_button("hover", True)
    phone_frame()
    overlays()
    ending_seal()
