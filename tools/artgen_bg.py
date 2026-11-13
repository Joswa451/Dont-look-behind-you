"""Procedural painted backgrounds for DON'T LOOK BEHIND YOU."""
from __future__ import annotations

import math
import random

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

from art_common import (
    IMG, out, rgb, rgba, mix, vertical_gradient, radial_glow, add_screen_glow,
    noise, grain, vignette, bloom, soft_blur, rain_layer, fog_layer, light_shaft,
    polygon_gradient, finish_bg, save, make_dust_sprite,
)

W, H = 1920, 1080


def canvas(top="#101018", bottom="#08080d"):
    return vertical_gradient((W, H), top, bottom).convert("RGBA")


def layer():
    return Image.new("RGBA", (W, H), (0, 0, 0, 0))


def d_of(im):
    return ImageDraw.Draw(im)


def over(base, *layers):
    for l in layers:
        base = Image.alpha_composite(base, l)
    return base


def cracked(img, points, color=(8, 8, 12, 150), width=2, branches=2, seed=0):
    d = d_of(img)
    rng = random.Random(seed)
    for _ in range(branches):
        pts = [(x + rng.randint(-4, 4), y + rng.randint(-4, 4)) for x, y in points]
        d.line(pts, fill=color, width=width)
        # side splinters
        for i in range(1, len(pts) - 1, 2):
            x, y = pts[i]
            ang = rng.uniform(-2.6, 2.6)
            ln = rng.uniform(12, 52)
            d.line([(x, y), (x + math.cos(ang) * ln, y + math.sin(ang) * ln)], fill=color, width=max(1, width - 1))


def stains(img, spots, color=(0, 0, 0), alpha=70, seed=0):
    rng = random.Random(seed)
    l = layer()
    d = d_of(l)
    for cx, cy, r in spots:
        for i in range(10):
            rr = r * rng.uniform(0.5, 1.15)
            ox = cx + rng.gauss(0, r * 0.35)
            oy = cy + rng.gauss(0, r * 0.28)
            d.ellipse([ox - rr, oy - rr * 0.7, ox + rr, oy + rr * 0.7],
                      fill=color + (int(alpha * rng.uniform(0.12, 0.35)),))
    l = l.filter(ImageFilter.GaussianBlur(18))
    return Image.alpha_composite(img, l)


def window(img, box, night=True, rain=True, blinds=True, warm=False, seed=1):
    x1, y1, x2, y2 = box
    l = layer()
    d = d_of(l)
    if warm:
        sky_top, sky_bottom = "#5d4a3a", "#2b2220"
    else:
        sky_top, sky_bottom = "#1c2b45" if night else "#73869a", "#0a0f1a" if night else "#c4c2b4"
    g = vertical_gradient((x2 - x1, y2 - y1), sky_top, sky_bottom).convert("RGBA")
    l.paste(g, (x1, y1))
    if night:
        rng = random.Random(seed)
        dd = d_of(l)
        for _ in range(45):
            sx = rng.uniform(x1, x2)
            sy = rng.uniform(y1, y1 + (y2 - y1) * 0.55)
            dd.point((sx, sy), fill=(220, 225, 240, rng.randint(60, 190)))
        # distant city blocks
        dd.rectangle([x1, y1 + (y2 - y1) * 0.58, x2, y2], fill=(8, 12, 20, 230))
        for i in range(16):
            bx = x1 + (i / 16) * (x2 - x1)
            bh = rng.uniform(0.08, 0.28) * (y2 - y1)
            dd.rectangle([bx, y2 - bh, bx + 30, y2], fill=(6, 9, 16, 255))
            for wy in range(int(y2 - bh + 8), y2 - 5, 13):
                for wx in range(int(bx + 5), int(bx + 27), 10):
                    if rng.random() < 0.24:
                        dd.rectangle([wx, wy, wx + 3, wy + 4], fill=(214, 182, 116, 130))
    if rain:
        rl = rain_layer((x2 - x1, y2 - y1), density=120, length=30, alpha=65, seed=seed + 2)
        l.alpha_composite(rl, (x1, y1))
    # frame
    d.rectangle([x1 - 10, y1 - 10, x2 + 10, y2 + 10], outline=(20, 18, 22, 255), width=12)
    d.rectangle([x1, y1, x2, y2], outline=(58, 54, 58, 255), width=3)
    d.line([( (x1+x2)//2, y1), ((x1+x2)//2, y2)], fill=(42, 40, 44, 255), width=6)
    d.line([(x1, (y1+y2)//2), (x2, (y1+y2)//2)], fill=(42, 40, 44, 255), width=6)
    if blinds:
        for by in range(y1, y2, 17):
            d.rectangle([x1, by, x2, by + 7], fill=(12, 11, 14, 140))
    return l, (x1, y1, x2, y2)


def door(img, box, open_amount=0.0, color=(20, 16, 18), frame=(34, 29, 29), glow=None, seed=0):
    x1, y1, x2, y2 = box
    l = layer()
    d = d_of(l)
    d.rectangle([x1 - 12, y1 - 12, x2 + 12, y2], fill=frame + (255,))
    if open_amount > 0:
        d.rectangle([x1, y1, x2, y2], fill=(3, 3, 5, 255))
        if glow:
            gl = radial_glow((W, H), ((x1 + x2) / 2, (y1 + y2) / 2), (y2 - y1) * 0.7, glow, 150, 2.0)
            l = Image.alpha_composite(l, gl)
        # door plane swung inward
        w = (x2 - x1) * (1 - open_amount)
        d.polygon([(x1, y1), (x1 + w, y1 + 22), (x1 + w, y2), (x1, y2)], fill=color + (255,))
        d.line([(x1, y1), (x1 + w, y1 + 22)], fill=(52, 45, 44, 255), width=4)
        d.ellipse([x1 + w - 30, y1 + (y2 - y1) * 0.5, x1 + w - 16, y1 + (y2 - y1) * 0.5 + 14], fill=(150, 120, 70, 255))
    else:
        d.rectangle([x1, y1, x2, y2], fill=color + (255,))
        d.rectangle([x1 + 18, y1 + 24, x2 - 18, y2 - 18], outline=(50, 42, 40, 255), width=3)
        d.rectangle([x1 + 34, y1 + 48, x2 - 34, y1 + (y2 - y1) * 0.44], outline=(44, 37, 36, 255), width=2)
        d.rectangle([x1 + 34, y1 + (y2 - y1) * 0.52, x2 - 34, y2 - 40], outline=(44, 37, 36, 255), width=2)
        d.ellipse([x2 - 58, y1 + (y2 - y1) * 0.5, x2 - 40, y1 + (y2 - y1) * 0.5 + 18], fill=(154, 124, 68, 255))
    # light leak around frame
    if glow:
        leak = radial_glow((W, H), ((x1 + x2) / 2, y2), (x2 - x1) * 1.2, glow, 55, 2.4)
        l = Image.alpha_composite(l, leak)
    return l


def floor_boards(img, horizon=690, vanish=(960, 690), color=(30, 24, 22), seed=3):
    d = d_of(img)
    rng = random.Random(seed)
    for i in range(-14, 22):
        x_bottom = vanish[0] + (i - 3) * 118
        d.line([vanish, (x_bottom, H)], fill=(0, 0, 0, 34), width=1)
    for y in range(horizon + 20, H, 46):
        t = (y - horizon) / (H - horizon)
        d.line([(0, y), (W, y)], fill=(0, 0, 0, int(16 + 26 * t)), width=1)
    return img


def wall_cracks(img, seed=11, count=3, region=(0, 0, W, 650)):
    for i in range(count):
        x0 = random.Random(seed + i).uniform(*region[0:2]) if False else random.Random(seed + i).uniform(region[0], region[2])
        y0 = random.Random(seed + i + 20).uniform(region[1], region[1] + (region[3] - region[1]) * 0.7)
        pts = [(x0, y0)]
        for _ in range(9):
            x0 += random.Random(seed + i + len(pts) * 3).uniform(-22, 34)
            y0 += random.Random(seed + i + len(pts) * 7).uniform(8, 40)
            pts.append((x0, y0))
        cracked(img, pts, color=(5, 5, 8, 120), width=2, branches=1, seed=seed + i)


def dust_motes(img, count=90, color=(220, 215, 200), seed=5, alpha=55):
    rng = random.Random(seed)
    l = layer()
    d = d_of(l)
    for _ in range(count):
        x = rng.uniform(0, W)
        y = rng.uniform(0, H)
        r = rng.uniform(0.6, 2.3)
        a = int(alpha * rng.uniform(0.2, 1.0))
        d.ellipse([x - r, y - r, x + r, y + r], fill=color + (a,))
    return Image.alpha_composite(img, l)


def poster(img, box, color1, color2, seed=0, text_marks=True):
    x1, y1, x2, y2 = box
    l = layer()
    g = vertical_gradient((x2 - x1, y2 - y1), color1, color2).convert("RGBA")
    mask = Image.new("L", (x2 - x1, y2 - y1), 255)
    l.paste(g, (x1, y1), mask)
    d = d_of(l)
    d.rectangle([x1, y1, x2, y2], outline=(10, 9, 10, 180), width=3)
    rng = random.Random(seed)
    if text_marks:
        for i in range(rng.randint(3, 7)):
            yy = y1 + rng.uniform(15, (y2 - y1) * 0.8)
            d.line([(x1 + 12, yy), (x1 + rng.uniform(30, (x2 - x1) - 12), yy)],
                   fill=(220, 210, 190, rng.randint(30, 90)), width=rng.choice([2, 3, 5]))
    # torn corner
    d.polygon([(x2 - 34, y1), (x2, y1), (x2, y1 + 44)], fill=(8, 8, 10, 255))
    return l


def cardboard_box(img, box, light=(78, 59, 42), dark=(43, 32, 25), seed=0, label=False):
    x1, y1, x2, y2 = box
    l = layer()
    d = d_of(l)
    d.polygon([(x1, y1 + 18), (x1 + 24, y1), (x2, y1), (x2 - 18, y1 + 20)], fill=mix(light, (255, 255, 255), 0.14) + (255,))
    d.rectangle([x1, y1 + 18, x2 - 18, y2], fill=light + (255,))
    d.polygon([(x2 - 18, y1 + 20), (x2, y1), (x2, y2 - 10), (x2 - 18, y2)], fill=dark + (255,))
    d.line([(x1 + 10, y1 + 44), (x2 - 28, y1 + 44)], fill=(28, 21, 17, 160), width=3)
    if label:
        d.rectangle([x1 + 22, y1 + 65, x1 + 130, y1 + 120], fill=(180, 167, 140, 210))
        for i in range(3):
            d.line([(x1 + 30, y1 + 78 + i * 12), (x1 + 110, y1 + 78 + i * 12)], fill=(50, 44, 37, 150), width=2)
    return l


def hanging_bulb(img, pos, cable=120, glow=(255, 196, 120), strength=150, radius=320):
    x, y = pos
    d = d_of(img)
    d.line([(x, y - cable), (x, y - 20)], fill=(10, 9, 9, 255), width=3)
    d.rectangle([x - 9, y - 24, x + 9, y - 6], fill=(24, 22, 20, 255))
    glow_l = radial_glow((W, H), (x, y + 8), radius, glow, strength, 2.0)
    img = Image.alpha_composite(img, glow_l)
    d = d_of(img)
    d.ellipse([x - 13, y - 8, x + 13, y + 20], fill=(255, 239, 200, 255))
    d.ellipse([x - 7, y - 2, x + 7, y + 12], fill=(255, 255, 238, 255))
    return img


def candle(img, pos, height=36, glow=(220, 110, 50)):
    x, y = pos
    d = d_of(img)
    l = radial_glow((W, H), (x, y - height), 160, glow, 110, 2.0)
    img = Image.alpha_composite(img, l)
    d = d_of(img)
    d.rectangle([x - 5, y - height, x + 5, y], fill=(205, 190, 160, 255))
    d.ellipse([x - 4, y - height - 6, x + 4, y - height + 3], fill=(255, 210, 130, 255))
    d.ellipse([x - 2, y - height - 10, x + 2, y - height - 2], fill=(255, 250, 210, 255))
    return img


def eye_graffiti(img, box, color=(120, 24, 32, 170), seed=0):
    x1, y1, x2, y2 = box
    d = d_of(img)
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
    w = (x2 - x1) / 2
    h = (y2 - y1) / 2
    d.arc([x1, cy - h, x2, cy + h], 180, 360, fill=color, width=7)
    d.arc([x1, cy - h * 1.8, x2, cy + h * 0.4], 0, 180, fill=color, width=5)
    d.ellipse([cx - h * 0.55, cy - h * 0.55, cx + h * 0.55, cy + h * 0.55], outline=color, width=6)
    d.ellipse([cx - h * 0.18, cy - h * 0.18, cx + h * 0.18, cy + h * 0.18], fill=color)


# ---------------------------------------------------------------------------
# 1. BEDROOM (night / day)
# ---------------------------------------------------------------------------
def bedroom(day=False):
    base = canvas("#232532" if not day else "#5a5247", "#0b0a0f" if not day else "#3a332b")
    l = layer()
    d = d_of(l)

    # walls / floor
    d.rectangle([0, 0, W, 705], fill=(36, 38, 51, 255) if not day else (92, 84, 72, 255))
    wall_grad = polygon_gradient((W, H), [(0, 0), (W, 0), (W, 705), (0, 705)],
                                 "#35384a" if not day else "#7d7261", "#1a1a24" if not day else "#4a4137")
    l = Image.alpha_composite(l, wall_grad)
    img = Image.alpha_composite(base, l)

    floor = polygon_gradient((W, H), [(0, 705), (W, 705), (W, H), (0, H)],
                             "#2a2221" if not day else "#51453a", "#100c0e" if not day else "#2b241f")
    img = Image.alpha_composite(img, floor)
    floor_boards(img, 705, (900, 705), seed=4)

    # side wall shadow
    sh = layer()
    dd = d_of(sh)
    dd.polygon([(0, 0), (210, 0), (120, 705), (0, 705)], fill=(7, 7, 12, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(28))
    img = Image.alpha_composite(img, sh)

    win_l, wbox = window(img, (120, 170, 500, 560), night=not day, rain=True,
                         warm=day, seed=7)
    img = Image.alpha_composite(img, win_l)
    # window moonlight / daylight
    if day:
        img = Image.alpha_composite(img, light_shaft((W, H), [(130, 400), (490, 380), (970, 1080), (420, 1080)], (255, 226, 170), 45))
    else:
        img = Image.alpha_composite(img, light_shaft((W, H), [(130, 400), (490, 380), (900, 1080), (350, 1080)], (128, 164, 215), 55))
        img = add_screen_glow(img, (310, 360), 520, (80, 112, 170), 50)

    # curtains
    cur = layer()
    dc = d_of(cur)
    for ox, flip in [(-30, 1), (420, -1)]:
        pts = [(120 + ox, 140), (120 + ox + 90 * flip, 140), (120 + ox + 130 * flip, 620), (120 + ox + 30 * flip, 620)]
        dc.polygon(pts, fill=(40, 28, 40, 220) if not day else (96, 74, 65, 220))
    cur = cur.filter(ImageFilter.GaussianBlur(3))
    img = Image.alpha_composite(img, cur)

    # bed, right side
    bed = layer()
    db = d_of(bed)
    db.polygon([(1180, 640), (1810, 620), (1890, 940), (1230, 1000)], fill=(39, 50, 56, 255))
    db.polygon([(1180, 640), (1810, 620), (1840, 700), (1200, 730)], fill=(55, 66, 70, 255))
    db.polygon([(1230, 730), (1840, 700), (1890, 940), (1260, 980)], fill=(63, 73, 75, 255))
    # blanket folds
    for i in range(8):
        x = 1260 + i * 75
        db.line([(x, 745), (x + 30, 965)], fill=(39, 49, 52, 140), width=9)
    db.polygon([(1300, 630), (1660, 610), (1710, 690), (1320, 715)], fill=(153, 143, 128, 255))
    db.ellipse([1300, 600, 1510, 700], fill=(172, 162, 146, 255))
    db.ellipse([1460, 600, 1660, 690], fill=(158, 148, 134, 255))
    # headboard
    db.rectangle([1180, 470, 1840, 650], fill=(47, 38, 35, 255))
    db.rectangle([1200, 490, 1820, 630], fill=(59, 47, 42, 255))
    for i in range(4):
        db.rounded_rectangle([1220 + i * 150, 510, 1340 + i * 150, 615], radius=14, outline=(36, 29, 27, 255), width=5)
    img = Image.alpha_composite(img, bed)

    # desk + monitor left
    desk = layer()
    dd = d_of(desk)
    dd.polygon([(120, 780), (640, 760), (760, 840), (210, 870)], fill=(64, 45, 34, 255))
    dd.rectangle([150, 820, 210, 1040], fill=(42, 30, 25, 255))
    dd.rectangle([610, 805, 665, 1000], fill=(42, 30, 25, 255))
    dd.rectangle([320, 610, 620, 790], fill=(13, 14, 18, 255))
    dd.rectangle([336, 626, 604, 774], fill=(21, 30, 38, 255))
    if not day:
        dd.rectangle([336, 626, 604, 774], fill=(34, 52, 63, 255))
        for i in range(8):
            dd.line([(350, 650 + i * 15), (350 + 60 + i * 18, 650 + i * 15)], fill=(95, 138, 145, 160), width=2)
        mg = radial_glow((W, H), (470, 700), 260, (68, 130, 150), 100, 2.1)
        img = Image.alpha_composite(img, mg)
    # chair
    dd.rectangle([840, 760, 930, 990], fill=(27, 25, 27, 255))
    dd.rectangle([790, 740, 960, 790], fill=(36, 34, 36, 255))
    dd.rectangle([810, 980, 950, 1010], fill=(20, 18, 20, 255))
    img = Image.alpha_composite(img, desk)

    # closet door right wall
    img = Image.alpha_composite(img, door(img, (1580, 190, 1850, 700), open_amount=0.18, color=(35, 27, 27), frame=(52, 42, 38), glow=(80, 25, 30), seed=2))

    # posters
    img = Image.alpha_composite(img, poster(img, (600, 150, 760, 340), "#3a2434", "#15101b", seed=1))
    img = Image.alpha_composite(img, poster(img, (790, 230, 900, 380), "#25303a", "#111519", seed=2))
    # clock
    d = d_of(img)
    d.ellipse([690, 60, 790, 160], fill=(14, 13, 16, 255), outline=(74, 68, 66, 255), width=4)
    d.line([(740, 110), (740, 78)], fill=(180, 60, 60, 255), width=4)
    d.line([(740, 110), (764, 120)], fill=(150, 145, 135, 255), width=3)

    # boxes foreground
    img = Image.alpha_composite(img, cardboard_box(img, (40, 760, 330, 1040), seed=1, label=True))
    img = Image.alpha_composite(img, cardboard_box(img, (260, 880, 500, 1075), seed=2))

    # clutter on desk, phone
    d = d_of(img)
    d.rectangle([540, 745, 590, 785], fill=(10, 10, 14, 255))
    d.rectangle([548, 750, 582, 775], fill=(28, 43, 52, 255))
    d.rounded_rectangle([330, 770, 390, 790], radius=5, fill=(20, 19, 23, 255))
    d.ellipse([336, 774, 346, 784], fill=(80, 90, 90, 255))

    # dust, atmosphere
    img = Image.alpha_composite(img, fog_layer((W, H), (120, 130, 150), 28, seed=4))
    img = dust_motes(img, 80, seed=5, alpha=45)
    img = stains(img, [(1160, 390, 120), (0, 500, 110), (760, 640, 60)], color=(0, 0, 0), alpha=70, seed=4)
    wall_cracks(img, seed=10, count=2, region=(900, 0, 1500, 640))
    d = d_of(img)
    if not day:
        d.text((170, 975), "3B", fill=(96, 84, 74, 170))
    img = img.convert("RGB")
    img = finish_bg(img, 0.72 if not day else 0.55, 0.045, 0.3, seed=3)
    save(img, out("backgrounds", "bg_bedroom.png" if not day else "bg_bedroom_day.jpg"))


# ---------------------------------------------------------------------------
# 2. LIVING ROOM
# ---------------------------------------------------------------------------
def livingroom():
    base = canvas("#28222a", "#0a080b")
    img = base
    grad = polygon_gradient((W, H), [(0, 0), (W, 0), (W, 700), (0, 700)], "#3b3038", "#1a1419")
    img = Image.alpha_composite(img, grad)
    floor = polygon_gradient((W, H), [(0, 700), (W, 700), (W, H), (0, H)], "#3d2b24", "#150e0c")
    img = Image.alpha_composite(img, floor)
    floor_boards(img, 700, (1020, 700), seed=5)
    d = d_of(img)
    d.line([(0, 700), (W, 700)], fill=(18, 14, 14, 255), width=8)

    # window right
    win_l, _ = window(img, (1440, 140, 1820, 500), night=True, rain=True, seed=11)
    img = Image.alpha_composite(img, win_l)
    img = Image.alpha_composite(img, light_shaft((W, H), [(1460, 420), (1800, 400), (1660, 1080), (1150, 1080)], (110, 145, 200), 38))

    # kitchenette background right
    d = d_of(img)
    d.rectangle([1520, 520, 1920, 700], fill=(33, 30, 29, 255))
    d.rectangle([1560, 540, 1760, 690], fill=(20, 20, 20, 255))
    d.rectangle([1790, 540, 1900, 690], fill=(27, 27, 25, 255))
    for i in range(5):
        d.line([(1800, 560 + i * 24), (1890, 560 + i * 24)], fill=(55, 52, 46, 255), width=2)

    # sofa left-center
    sofa = layer()
    ds = d_of(sofa)
    ds.polygon([(230, 720), (890, 700), (980, 980), (210, 1020)], fill=(47, 51, 52, 255))
    ds.polygon([(250, 690), (880, 670), (930, 760), (250, 790)], fill=(63, 68, 68, 255))
    ds.polygon([(230, 720), (300, 715), (320, 1000), (230, 1020)], fill=(38, 41, 42, 255))
    ds.polygon([(810, 700), (890, 700), (980, 980), (890, 970)], fill=(32, 35, 36, 255))
    ds.line([(500, 720), (540, 990)], fill=(35, 38, 39, 170), width=12)
    ds.line([(680, 710), (730, 990)], fill=(35, 38, 39, 170), width=12)
    # cushions
    ds.rounded_rectangle([340, 720, 500, 840], radius=26, fill=(74, 63, 56, 255))
    ds.rounded_rectangle([640, 710, 800, 835], radius=26, fill=(64, 55, 50, 255))
    img = Image.alpha_composite(img, sofa)

    # coffee table
    d = d_of(img)
    d.polygon([(480, 900), (940, 870), (1030, 960), (530, 1000)], fill=(65, 45, 32, 255))
    d.rectangle([560, 990, 600, 1050], fill=(39, 27, 21, 255))
    d.rectangle([920, 955, 960, 1010], fill=(39, 27, 21, 255))
    # papers + mug
    d.polygon([(650, 900), (820, 890), (840, 940), (670, 950)], fill=(157, 148, 129, 255))
    d.ellipse([880, 890, 930, 930], fill=(30, 30, 32, 255))

    # TV left with static
    d = d_of(img)
    d.rectangle([70, 430, 390, 690], fill=(11, 11, 14, 255))
    d.rectangle([88, 448, 372, 660], fill=(28, 35, 38, 255))
    for i in range(40):
        yy = 450 + i * 5
        d.line([(90, yy), (370, yy)], fill=(45 + (i * 7) % 40, 58 + (i * 11) % 40, 60 + (i * 5) % 30, 120), width=1)
    tv = radial_glow((W, H), (230, 550), 320, (90, 130, 140), 90, 2.0)
    img = Image.alpha_composite(img, tv)

    # lamp on side table
    d = d_of(img)
    d.rectangle([1070, 680, 1160, 820], fill=(42, 30, 24, 255))
    d.line([(1115, 680), (1115, 610)], fill=(100, 84, 55, 255), width=5)
    d.polygon([(1060, 610), (1170, 610), (1140, 550), (1090, 550)], fill=(190, 152, 94, 255))
    img = Image.alpha_composite(img, radial_glow((W, H), (1115, 580), 420, (230, 170, 90), 150, 2.1))

    # hallway door back center
    img = Image.alpha_composite(img, door(img, (1010, 260, 1230, 700), open_amount=0.0, color=(39, 30, 28), frame=(54, 44, 38), glow=(120, 42, 40), seed=4))

    # boxes
    img = Image.alpha_composite(img, cardboard_box(img, (1290, 760, 1510, 950), seed=6, label=True))
    img = Image.alpha_composite(img, cardboard_box(img, (1470, 840, 1640, 1000), seed=7))

    # rug
    d = d_of(img)
    d.ellipse([300, 840, 1120, 1060], fill=(52, 30, 30, 160))
    d.ellipse([340, 860, 1080, 1035], outline=(82, 55, 48, 160), width=5)

    # atmosphere
    img = Image.alpha_composite(img, fog_layer((W, H), (130, 120, 130), 30, seed=8))
    img = dust_motes(img, 70, seed=9, alpha=40)
    img = stains(img, [(0, 200, 170), (1300, 600, 90)], seed=2)
    img = img.convert("RGB")
    save(finish_bg(img, 0.75, 0.05, 0.35, seed=6), out("backgrounds", "bg_livingroom.jpg"))


# ---------------------------------------------------------------------------
# 3. HALLWAY
# ---------------------------------------------------------------------------
def hallway():
    base = canvas("#2b2119", "#090709")
    img = base
    # wallpaper
    grad = polygon_gradient((W, H), [(0, 0), (W, 0), (W, H), (0, H)], "#3c2f23", "#100c0c")
    img = Image.alpha_composite(img, grad)
    # perspective corridor
    vx, vy = 1030, 520
    d = d_of(img)
    # ceiling
    d.polygon([(0, 0), (W, 0), (vx + 260, vy - 130), (vx - 260, vy - 130)], fill=(24, 19, 16, 255))
    # floor
    d.polygon([(0, H), (W, H), (vx + 260, vy + 130), (vx - 260, vy + 130)], fill=(30, 20, 18, 255))
    # side walls
    d.polygon([(0, 0), (vx - 260, vy - 130), (vx - 260, vy + 130), (0, H)], fill=(50, 38, 27, 255))
    d.polygon([(W, 0), (vx + 260, vy - 130), (vx + 260, vy + 130), (W, H)], fill=(42, 32, 24, 255))
    # back wall
    d.rectangle([vx - 260, vy - 130, vx + 260, vy + 130], fill=(45, 34, 25, 255))
    # carpet runner
    d.polygon([(520, H), (1450, H), (vx + 120, vy + 130), (vx - 120, vy + 130)], fill=(51, 23, 26, 255))
    d.polygon([(500, H), (530, H), (vx - 110, vy + 130), (vx - 120, vy + 130)], fill=(91, 62, 42, 255))
    d.polygon([(1440, H), (1470, H), (vx + 120, vy + 130), (vx + 110, vy + 130)], fill=(91, 62, 42, 255))
    # wallpaper stripes / panels
    for side in (-1, 1):
        for i in range(8):
            t0 = i / 8
            t1 = (i + 1) / 8
            if side < 0:
                xa = 0 + (vx - 260) * t0
                xb = 0 + (vx - 260) * t1
                ya = H * (1 - t0) + (vy + 130) * t0
                yb = H * (1 - t1) + (vy + 130) * t1
                d.line([(xa, ya), (xb, yb)], fill=(20, 15, 12, 90), width=2)
            else:
                xa = W + (vx + 260 - W) * t0
                xb = W + (vx + 260 - W) * t1
                ya = H * (1 - t0) + (vy + 130) * t0
                yb = H * (1 - t1) + (vy + 130) * t1
                d.line([(xa, ya), (xb, yb)], fill=(20, 15, 12, 90), width=2)
    # doors along both walls (hand-placed perspective boxes)
    door_boxes = [
        ("left", 30, 270, 286, 930, 0),
        ("left", 400, 360, 540, 820, 1),
        ("left", 670, 430, 760, 700, 2),
        ("right", 1634, 270, 1890, 930, 3),
        ("right", 1380, 360, 1520, 820, 4),
        ("right", 1160, 430, 1250, 700, 5),
    ]
    for side, x1, yt, x2, yb, idx in door_boxes:
        d = d_of(img)
        # frame
        d.rectangle([x1 - 12, yt - 12, x2 + 12, yb], fill=(51, 39, 30, 255))
        d.rectangle([x1, yt, x2, yb], fill=(31, 24, 20, 255))
        d.rectangle([x1 + 9, yt + 9, x2 - 9, yb - 14], outline=(19, 15, 12, 255), width=3)
        # upper/lower panels
        my = yt + (yb - yt) * 0.42
        d.rectangle([x1 + 20, yt + 22, x2 - 20, my], outline=(22, 17, 14, 180), width=2)
        d.rectangle([x1 + 20, my + 14, x2 - 20, yb - 30], outline=(22, 17, 14, 180), width=2)
        if idx == 1:
            # the door that is always slightly open
            gap = (x2 - x1) * 0.32
            d.rectangle([x1 + 9, yt + 9, x1 + gap, yb - 14], fill=(4, 3, 4, 255))
            d.rectangle([x1 + gap, yt + 12, x2 - 9, yb - 16], fill=(37, 27, 22, 255))
            d.rectangle([x1 + gap + 8, yt + 26, x2 - 20, my], outline=(19, 15, 12, 180), width=2)
            handle_x = x1 + gap - 9
            d.ellipse([handle_x, (yt + yb) / 2, handle_x + 13, (yt + yb) / 2 + 12], fill=(120, 95, 55, 255))
            img = Image.alpha_composite(img, radial_glow((W, H), (x1 + gap * 0.5, (yt + yb) / 2), 150, (160, 32, 36), 115, 2.1))
        else:
            handle_x = x2 - 26 if side == "left" else x1 + 14
            d.ellipse([handle_x, (yt + yb) / 2, handle_x + 13, (yt + yb) / 2 + 12], fill=(118, 92, 52, 255))
        # number plaque
        num = ["3A", "3B", "3C", "3D", "3E", "3F"][idx]
        d.rectangle([(x1 + x2) / 2 - 32, yt - 40, (x1 + x2) / 2 + 32, yt - 8], fill=(34, 28, 22, 255))
        d.text(((x1 + x2) / 2 - 12, yt - 34), num, fill=(166, 150, 120, 220))

    # end door
    img = Image.alpha_composite(img, door(img, (vx - 90, vy - 100, vx + 90, vy + 130), open_amount=0.0, color=(33, 25, 21), frame=(48, 37, 28), glow=(90, 25, 28), seed=3))
    # EXIT sign above end door
    d = d_of(img)
    d.rectangle([vx - 46, vy - 148, vx + 46, vy - 118], fill=(18, 40, 30, 255))
    d.text((vx - 22, vy - 143), "EXIT", fill=(80, 180, 120, 255))

    # ceiling lights
    for i, (lx, ly, rad) in enumerate([(500, 60, 300), (980, 300, 180), (vx, vy - 110, 130)]):
        img = Image.alpha_composite(img, radial_glow((W, H), (lx, ly), rad, (225, 190, 120), 85 if i != 1 else 35, 2.1))
        d = d_of(img)
        if i == 1:
            d.rectangle([lx - 60, ly - 8, lx + 60, ly + 5], fill=(42, 36, 28, 255))
        else:
            d.rectangle([lx - 70 + i * 16, ly - 6, lx + 70 - i * 16, ly + 8], fill=(205, 186, 145, 255))

    # peeling wallpaper
    d = d_of(img)
    rng = random.Random(12)
    for _ in range(16):
        x = rng.uniform(0, W)
        y = rng.uniform(80, 700)
        w = rng.uniform(20, 90)
        h = rng.uniform(40, 160)
        d.polygon([(x, y), (x + w, y + rng.uniform(-20, 20)), (x + w * 0.7, y + h), (x - w * 0.2, y + h * 0.8)],
                  fill=(26, 20, 17, rng.randint(90, 150)))
    # chair at end
    d = d_of(img)
    d.rectangle([vx + 150, vy + 20, vx + 210, vy + 130], fill=(24, 18, 16, 255))
    d.rectangle([vx + 130, vy + 10, vx + 230, vy + 40], fill=(33, 25, 20, 255))

    img = Image.alpha_composite(img, fog_layer((W, H), (150, 135, 110), 34, seed=3))
    img = dust_motes(img, 100, seed=2, alpha=55)
    img = stains(img, [(300, 300, 160), (900, 650, 120), (1500, 200, 90)], seed=8)
    img = img.convert("RGB")
    save(finish_bg(img, 0.78, 0.05, 0.32, seed=12), out("backgrounds", "bg_hallway.jpg"))


# ---------------------------------------------------------------------------
# 4. BATHROOM
# ---------------------------------------------------------------------------
def bathroom():
    base = canvas("#1f2a2a", "#070a0b")
    img = base
    grad = polygon_gradient((W, H), [(0, 0), (W, 0), (W, 690), (0, 690)], "#334342", "#16201f")
    img = Image.alpha_composite(img, grad)
    floor = polygon_gradient((W, H), [(0, 690), (W, 690), (W, H), (0, H)], "#2a3532", "#0b0e0e")
    img = Image.alpha_composite(img, floor)

    # tiles
    d = d_of(img)
    for x in range(0, W, 96):
        d.line([(x, 0), (x, 690)], fill=(18, 26, 25, 130), width=2)
    for y in range(0, 690, 84):
        d.line([(0, y), (W, y)], fill=(18, 26, 25, 130), width=2)
    for x in range(0, W, 120):
        d.line([(x, 690), (x - 80, H)], fill=(12, 18, 17, 100), width=2)
    for y in range(700, H, 55):
        d.line([(0, y), (W, y)], fill=(12, 18, 17, 90), width=2)
    # grime
    img = stains(img, [(250, 650, 200), (1600, 300, 180), (1000, 700, 240)], color=(10, 14, 12), alpha=110, seed=5)

    # mirror cabinet
    d = d_of(img)
    d.rectangle([730, 140, 1250, 560], fill=(16, 21, 22, 255))
    d.rectangle([748, 158, 1232, 542], fill=(52, 68, 68, 255))
    # dark reflection gradient
    refl = polygon_gradient((W, H), [(748, 158), (1232, 158), (1232, 542), (748, 542)], "#41585a", "#0c1112")
    img = Image.alpha_composite(img, refl)
    # reflected room suggestion
    d = d_of(img)
    d.rectangle([790, 420, 1180, 545], fill=(20, 27, 27, 190))
    d.rectangle([870, 235, 1090, 470], fill=(14, 19, 19, 200))
    # fog on mirror
    fog = radial_glow((W, H), (990, 350), 240, (200, 215, 210), 34, 1.6)
    img = Image.alpha_composite(img, fog)
    # handprint / smear
    d = d_of(img)
    d.ellipse([880, 300, 940, 390], fill=(200, 213, 208, 20))
    d.ellipse([900, 320, 920, 360], fill=(200, 213, 208, 26))
    # cracks
    cracked(img, [(1080, 170), (1050, 260), (1090, 330), (1040, 440)], color=(5, 8, 8, 180), width=3, branches=3, seed=3)
    d = d_of(img)
    d.rectangle([760, 570, 1220, 600], fill=(21, 27, 27, 255))

    # sink + faucet
    d = d_of(img)
    d.polygon([(700, 600), (1280, 600), (1320, 680), (660, 680)], fill=(63, 74, 73, 255))
    d.polygon([(760, 640), (1220, 640), (1200, 715), (780, 715)], fill=(35, 43, 42, 255))
    d.rectangle([960, 600, 1000, 650], fill=(120, 126, 118, 255))
    d.polygon([(940, 600), (1020, 600), (1000, 580), (960, 580)], fill=(140, 144, 134, 255))
    d.ellipse([930, 670, 1070, 690], fill=(9, 12, 12, 255))

    # bathtub right
    d = d_of(img)
    d.rounded_rectangle([1360, 620, 1920, 900], radius=34, fill=(55, 67, 65, 255))
    d.rounded_rectangle([1390, 640, 1890, 760], radius=24, fill=(34, 43, 43, 255))
    d.rounded_rectangle([1410, 760, 1870, 880], radius=20, fill=(25, 33, 33, 255))
    # shower curtain
    d.polygon([(1300, 330), (1600, 360), (1600, 780), (1270, 760)], fill=(70, 83, 81, 140))
    for i in range(8):
        d.line([(1300 + i * 38, 340), (1290 + i * 38, 770)], fill=(48, 60, 59, 120), width=3)
    # small window left
    win_l, _ = window(img, (130, 170, 400, 430), night=True, rain=True, blinds=False, seed=5)
    img = Image.alpha_composite(img, win_l)
    img = Image.alpha_composite(img, light_shaft((W, H), [(150, 300), (390, 290), (700, 1080), (300, 1080)], (120, 160, 175), 30))

    # fluorescent light
    d = d_of(img)
    d.rectangle([820, 60, 1170, 92], fill=(210, 225, 218, 255))
    d.rectangle([840, 92, 1150, 102], fill=(160, 180, 174, 255))
    img = Image.alpha_composite(img, radial_glow((W, H), (995, 90), 500, (170, 210, 200), 95, 2.0))

    # towel rack, red towel
    d = d_of(img)
    d.line([(1440, 260), (1780, 260)], fill=(120, 124, 112, 255), width=6)
    d.polygon([(1480, 260), (1740, 260), (1720, 500), (1500, 500)], fill=(83, 36, 37, 255))
    # blood/rust drip on sink
    for i in range(6):
        x = 840 + i * 55
        d.line([(x, 700), (x + 4, 740 + (i * 17) % 50)], fill=(100, 28, 26, 120), width=3)

    img = Image.alpha_composite(img, fog_layer((W, H), (140, 160, 155), 24, seed=3))
    img = dust_motes(img, 50, seed=4, alpha=35)
    img = img.convert("RGB")
    save(finish_bg(img, 0.8, 0.05, 0.36, seed=13), out("backgrounds", "bg_bathroom.jpg"))


# ---------------------------------------------------------------------------
# 5. KITCHEN
# ---------------------------------------------------------------------------
def kitchen():
    base = canvas("#1a221c", "#070907")
    img = base
    grad = polygon_gradient((W, H), [(0, 0), (W, 0), (W, 690), (0, 690)], "#273029", "#101510")
    img = Image.alpha_composite(img, grad)
    floor = polygon_gradient((W, H), [(0, 690), (W, 690), (W, H), (0, H)], "#27241e", "#0b0a08")
    img = Image.alpha_composite(img, floor)
    d = d_of(img)
    # back cabinets
    d.rectangle([0, 360, 1100, 690], fill=(32, 36, 30, 255))
    d.rectangle([0, 380, 1100, 430], fill=(52, 57, 46, 255))
    for x in range(0, 1100, 220):
        d.rectangle([x + 10, 395, x + 200, 425], outline=(23, 26, 21, 255), width=3)
        d.ellipse([x + 180, 402, x + 190, 412], fill=(130, 120, 88, 255))
    # counter
    d.rectangle([0, 540, 1180, 690], fill=(48, 46, 37, 255))
    d.rectangle([0, 530, 1180, 552], fill=(83, 78, 60, 255))
    # cabinets below
    for x in range(0, 1180, 240):
        d.rectangle([x + 12, 565, x + 220, 685], outline=(30, 29, 24, 255), width=3)
        d.ellipse([x + 190, 575, x + 202, 587], fill=(120, 112, 82, 255))
    # sink
    d.rectangle([420, 560, 690, 640], fill=(33, 39, 36, 255))
    d.rectangle([440, 575, 670, 628], fill=(20, 25, 24, 255))
    d.line([(540, 530), (540, 575)], fill=(133, 137, 120, 255), width=10)
    # knife block
    d.polygon([(760, 500), (920, 500), (900, 545), (780, 545)], fill=(58, 43, 31, 255))
    for i in range(5):
        d.line([(790 + i * 25, 500), (782 + i * 25, 450)], fill=(150, 153, 146, 255), width=6)
    # empty slot (missing knife)
    d.rectangle([866, 500, 880, 540], fill=(14, 12, 11, 255))
    # fridge right
    d.rectangle([1240, 220, 1560, 760], fill=(58, 62, 58, 255))
    d.rectangle([1250, 232, 1550, 500], outline=(35, 39, 36, 255), width=4)
    d.rectangle([1250, 510, 1550, 748], outline=(35, 39, 36, 255), width=4)
    d.rectangle([1520, 330, 1536, 430], fill=(150, 146, 126, 255))
    d.rectangle([1520, 560, 1536, 650], fill=(150, 146, 126, 255))
    # sticky note on fridge
    d.rectangle([1370, 300, 1460, 370], fill=(166, 158, 128, 255))
    d.text((1390, 315), "DON'T", fill=(91, 32, 32, 255))
    d.text((1390, 335), "OPEN", fill=(91, 32, 32, 255))
    # window above sink
    win_l, _ = window(img, (120, 70, 500, 320), night=True, rain=True, blinds=False, seed=9)
    img = Image.alpha_composite(img, win_l)
    img = Image.alpha_composite(img, light_shaft((W, H), [(140, 250), (480, 230), (900, 1080), (360, 1080)], (95, 130, 160), 28))
    # hanging bulb
    img = hanging_bulb(img, (980, 140), cable=90, glow=(240, 196, 120), strength=120, radius=500)
    # dining table foreground
    d = d_of(img)
    d.polygon([(100, 860), (760, 830), (900, 980), (230, 1020)], fill=(65, 50, 34, 255))
    d.rectangle([200, 990, 240, 1070], fill=(40, 30, 21, 255))
    d.rectangle([720, 960, 760, 1040], fill=(40, 30, 21, 255))
    d.ellipse([430, 830, 520, 875], fill=(34, 36, 32, 255))
    d.polygon([(560, 830), (600, 830), (610, 790), (550, 790)], fill=(148, 149, 132, 130))
    d.line([(580, 760), (580, 800)], fill=(110, 110, 100, 255), width=3)
    # shadows / atmosphere
    img = Image.alpha_composite(img, fog_layer((W, H), (110, 130, 110), 30, seed=6))
    img = dust_motes(img, 60, seed=7, alpha=40)
    img = stains(img, [(1050, 650, 220), (200, 500, 110)], color=(8, 10, 8), alpha=80, seed=9)
    img = img.convert("RGB")
    save(finish_bg(img, 0.8, 0.05, 0.32, seed=14), out("backgrounds", "bg_kitchen.jpg"))


# ---------------------------------------------------------------------------
# 6. ABANDONED SCHOOL EXTERIOR
# ---------------------------------------------------------------------------
def school():
    base = canvas("#141a26", "#06070b")
    img = base
    # sky with clouds
    sky = vertical_gradient((W, H), "#202a3e", "#0a0d15").convert("RGBA")
    img = Image.alpha_composite(img, sky)
    n = noise((W, H), scale=2.5, seed=4, octaves=5)
    arr = np.zeros((H, W, 4), dtype=np.uint8)
    arr[..., 0] = 70; arr[..., 1] = 82; arr[..., 2] = 104
    arr[..., 3] = (np.clip((n - 0.45) * 2.5, 0, 1) * 80).astype(np.uint8)
    img = Image.alpha_composite(img, Image.fromarray(arr, "RGBA").filter(ImageFilter.GaussianBlur(20)))
    # moon
    img = Image.alpha_composite(img, radial_glow((W, H), (1500, 170), 380, (170, 190, 220), 90, 2.2))
    d = d_of(img)
    d.ellipse([1450, 110, 1570, 230], fill=(204, 214, 226, 255))
    d.ellipse([1480, 130, 1510, 160], fill=(176, 188, 202, 255))
    d.ellipse([1520, 170, 1545, 192], fill=(180, 192, 205, 255))

    # building silhouette
    d = d_of(img)
    d.polygon([(180, 300), (1750, 300), (1820, 760), (100, 760)], fill=(20, 24, 32, 255))
    d.rectangle([380, 610, 450, 760], fill=(15, 18, 24, 255))
    # roof line / towers
    d.polygon([(260, 300), (260, 180), (470, 180), (470, 300)], fill=(18, 22, 30, 255))
    d.polygon([(1450, 300), (1450, 150), (1700, 150), (1700, 300)], fill=(18, 22, 30, 255))
    d.polygon([(260, 180), (365, 110), (470, 180)], fill=(14, 17, 23, 255))
    d.polygon([(1450, 150), (1575, 90), (1700, 150)], fill=(14, 17, 23, 255))
    # cross on tower
    d.rectangle([1560, 40, 1580, 110], fill=(20, 24, 31, 255))
    d.rectangle([1545, 60, 1595, 75], fill=(20, 24, 31, 255))
    # windows grid
    rng = random.Random(8)
    for row in range(3):
        for col in range(13):
            x = 340 + col * 100
            y = 340 + row * 100
            lit = rng.random() < 0.09
            d.rectangle([x, y, x + 46, y + 62], fill=(35, 43, 52, 255))
            if lit:
                d.rectangle([x + 4, y + 4, x + 42, y + 58], fill=(194, 168, 104, 170))
            else:
                d.rectangle([x + 4, y + 4, x + 42, y + 58], fill=(10, 14, 19, 255))
            d.line([(x + 23, y), (x + 23, y + 62)], fill=(24, 30, 38, 255), width=3)
    # fence + gate
    d = d_of(img)
    d.rectangle([0, 820, W, 1080], fill=(9, 11, 14, 255))
    for x in range(0, W, 34):
        d.line([(x, 760), (x + 18, 900)], fill=(19, 21, 24, 255), width=4)
    d.line([(0, 810), (W, 810)], fill=(22, 24, 27, 255), width=8)
    # arch gate
    d.arc([810, 640, 1110, 930], 180, 360, fill=(15, 17, 21, 255), width=30)
    d.rectangle([810, 780, 840, 1000], fill=(15, 17, 21, 255))
    d.rectangle([1080, 780, 1110, 1000], fill=(15, 17, 21, 255))
    # path
    d.polygon([(880, 950), (1040, 950), (1260, 1080), (660, 1080)], fill=(28, 30, 32, 255))
    # dead trees
    for tx, scale in [(240, 1.0), (1700, 1.25), (560, 0.7)]:
        base_y = 960
        d.line([(tx, base_y), (tx, base_y - 260 * scale)], fill=(13, 15, 18, 255), width=int(12 * scale) + 3)
        rng = random.Random(tx)
        for i in range(8):
            yy = base_y - 150 * scale - i * 16 * scale
            ang = rng.uniform(-1.2, 1.2)
            ln = rng.uniform(40, 110) * scale
            d.line([(tx, yy), (tx + math.cos(ang) * ln, yy - abs(math.sin(ang)) * ln * 0.6)], fill=(13, 15, 18, 255), width=max(2, int(6 * scale)))
    # fog, rain
    img = Image.alpha_composite(img, fog_layer((W, H), (120, 135, 155), 80, seed=12))
    img = Image.alpha_composite(img, rain_layer((W, H), density=760, length=60, alpha=80, seed=4))
    # sign
    d = d_of(img)
    d.rectangle([1180, 650, 1500, 700], fill=(30, 34, 38, 255), outline=(61, 66, 68, 255), width=3)
    d.text((1210, 665), "ST. AGNES  HOME", fill=(155, 156, 146, 200))
    img = dust_motes(img, 70, seed=2, alpha=40)
    img = img.convert("RGB")
    save(finish_bg(img, 0.75, 0.055, 0.3, seed=15), out("backgrounds", "bg_school.jpg"))


# ---------------------------------------------------------------------------
# 7. EMPTY CLASSROOM
# ---------------------------------------------------------------------------
def classroom():
    base = canvas("#222b39", "#080b11")
    img = base
    grad = polygon_gradient((W, H), [(0, 0), (W, 0), (W, 660), (0, 660)], "#33404f", "#141b26")
    img = Image.alpha_composite(img, grad)
    floor = polygon_gradient((W, H), [(0, 660), (W, 660), (W, H), (0, H)], "#3c3428", "#120f0c")
    img = Image.alpha_composite(img, floor)
    floor_boards(img, 660, (960, 660), seed=7)
    # side wall perspective
    d = d_of(img)
    d.polygon([(0, 0), (250, 120), (250, 760), (0, 900)], fill=(24, 30, 40, 255))
    d.polygon([(0, 900), (250, 760), (250, 780), (0, 1080)], fill=(17, 20, 25, 255))
    # windows right
    win_l, _ = window(img, (1380, 110, 1840, 500), night=True, rain=True, blinds=False, seed=21)
    img = Image.alpha_composite(img, win_l)
    img = Image.alpha_composite(img, light_shaft((W, H), [(1400, 400), (1820, 370), (1500, 1080), (940, 1080)], (135, 170, 220), 48))
    # blackboard
    d = d_of(img)
    d.rectangle([420, 150, 1240, 540], fill=(42, 31, 27, 255))
    d.rectangle([444, 174, 1216, 516], fill=(25, 40, 32, 255))
    # chalk writing
    d.text((560, 250), "DON'T LOOK", fill=(190, 196, 180, 190))
    d.text((610, 305), "BEHIND YOU", fill=(190, 196, 180, 190))
    d.line([(620, 390), (1030, 390)], fill=(150, 160, 148, 70), width=2)
    d.text((650, 420), "she is already inside", fill=(160, 170, 158, 120))
    # chalk dust
    rng = random.Random(5)
    for _ in range(80):
        x = rng.uniform(450, 1210)
        y = rng.uniform(200, 510)
        d.point((x, y), fill=(180, 190, 175, rng.randint(20, 80)))
    # teacher desk
    d = d_of(img)
    d.polygon([(760, 620), (1120, 610), (1180, 700), (790, 715)], fill=(61, 47, 33, 255))
    d.rectangle([800, 700, 840, 830], fill=(41, 31, 23, 255))
    d.rectangle([1100, 690, 1140, 820], fill=(41, 31, 23, 255))
    # desks progressively nearer
    rng = random.Random(3)
    rows = [(700, 0.55), (820, 0.78), (960, 1.08)]
    for ry, sc in rows:
        for i in range(7):
            x = 180 + i * 240 - (ry - 700) * 0.35
            w = 150 * sc
            h = 30 * sc
            top_y = ry + (i % 2) * 12 * sc
            d.polygon([(x, top_y), (x + w, top_y - 6 * sc), (x + w + 10, top_y + h), (x - 5, top_y + h + 4)], fill=(79, 61, 43, 255))
            d.rectangle([x + 10, top_y + h, x + 18, top_y + h + 90 * sc], fill=(25, 22, 20, 255))
            d.rectangle([x + w - 12, top_y + h, x + w - 4, top_y + h + 90 * sc], fill=(25, 22, 20, 255))
            d.rectangle([x + 20, top_y + h + 20, x + w, top_y + h + max(24, 34 * sc)], fill=(57, 44, 32, 255))
            # chair
            d.rectangle([x + 20, top_y + h + 70 * sc, x + 30, top_y + h + 160 * sc], fill=(35, 32, 30, 255))
            d.rectangle([x + 20, top_y + h + 70 * sc, x + w - 10, top_y + h + 78 * sc], fill=(45, 40, 35, 255))
    # broken window / papers
    d = d_of(img)
    for i in range(14):
        x = rng.uniform(120, 1800)
        y = rng.uniform(720, 1050)
        d.polygon([(x, y), (x + rng.uniform(20, 60), y + rng.uniform(-10, 10)), (x + rng.uniform(30, 80), y + rng.uniform(30, 70))],
                  fill=(150, 146, 126, rng.randint(50, 100)))
    # hanging ceiling lamp
    for lx in (500, 1000, 1500):
        d.line([(lx, 0), (lx, 95)], fill=(13, 13, 14, 255), width=3)
        d.polygon([(lx - 55, 95), (lx + 55, 95), (lx + 35, 120), (lx - 35, 120)], fill=(35, 39, 40, 255))
    img = Image.alpha_composite(img, radial_glow((W, H), (1000, 140), 420, (150, 175, 200), 55, 2.0))
    img = Image.alpha_composite(img, fog_layer((W, H), (150, 165, 185), 40, seed=2))
    img = dust_motes(img, 110, seed=6, alpha=60)
    img = stains(img, [(700, 600, 180), (1400, 800, 220)], seed=3)
    img = img.convert("RGB")
    save(finish_bg(img, 0.76, 0.05, 0.34, seed=16), out("backgrounds", "bg_classroom.jpg"))


# ---------------------------------------------------------------------------
# 8. RAINY CITY STREET
# ---------------------------------------------------------------------------
def street():
    base = canvas("#101522", "#040508")
    img = base
    # buildings
    d = d_of(img)
    rng = random.Random(6)
    for i in range(12):
        bw = rng.randint(120, 300)
        bx = i * 170 - 80
        bh = rng.randint(280, 720)
        d.rectangle([bx, H - bh - 200, bx + bw, H], fill=mix((14, 18, 28), (22, 26, 38), rng.random()) + (255,))
        # windows
        for wy in range(H - bh - 170, H - 150, 38):
            for wx in range(bx + 18, bx + bw - 20, 30):
                if rng.random() < 0.30:
                    col = (208, 176, 108) if rng.random() < 0.7 else (110, 150, 160)
                    d.rectangle([wx, wy, wx + 12, wy + 18], fill=col + (rng.randint(45, 150),))
    # road
    d = d_of(img)
    d.polygon([(0, 760), (W, 740), (W, H), (0, H)], fill=(15, 16, 20, 255))
    d.line([(0, 860), (W, 850)], fill=(49, 48, 45, 130), width=7)
    for i in range(8):
        x = i * 280 + 60
        d.rectangle([x, 930 + (i % 2) * 8, x + 130, 944 + (i % 2) * 8], fill=(120, 110, 82, 110))
    # wet reflections
    for i in range(40):
        x = rng.uniform(0, W)
        y = rng.uniform(760, H)
        d.line([(x, y), (x + rng.uniform(-60, 60), y + rng.uniform(20, 120))], fill=(60, 70, 80, rng.randint(15, 60)), width=rng.randint(2, 7))
    # sidewalks / storefront
    d.rectangle([0, 700, W, 770], fill=(35, 34, 32, 255))
    # neon signs
    signs = [(300, 520, "ASHCROFT", (170, 45, 55)), (1500, 560, "HOTEL", (60, 130, 150)), (980, 480, "3:00", (180, 60, 60)), (700, 620, "OPEN", (160, 130, 60))]
    for x, y, text, col in signs:
        d.rectangle([x - 16, y - 16, x + 200, y + 54], fill=(10, 10, 14, 210), outline=col + (180,), width=3)
        d.text((x, y), text, fill=col + (255,))
        img = Image.alpha_composite(img, radial_glow((W, H), (x + 85, y + 20), 240, col, 55, 2.2))
    # streetlights
    for x in (400, 1100, 1800):
        d.line([(x, 700), (x, 360)], fill=(24, 25, 28, 255), width=8)
        d.line([(x, 360), (x - 80, 340)], fill=(24, 25, 28, 255), width=6)
        img = Image.alpha_composite(img, hanging_bulb(img, (x - 80, 360), cable=2, glow=(240, 196, 120), strength=110, radius=360))
    # lone figure silhouette far
    d = d_of(img)
    d.ellipse([942, 690, 966, 718], fill=(8, 8, 10, 255))
    d.polygon([(930, 720), (978, 720), (990, 840), (918, 840)], fill=(8, 8, 10, 255))
    # car
    d.polygon([(120, 830), (520, 810), (600, 900), (60, 930)], fill=(21, 24, 29, 255))
    d.polygon([(200, 810), (300, 740), (460, 750), (520, 812)], fill=(17, 20, 25, 255))
    d.ellipse([120, 890, 200, 960], fill=(8, 8, 10, 255))
    d.ellipse([430, 880, 510, 950], fill=(8, 8, 10, 255))
    d.ellipse([500, 850, 540, 870], fill=(200, 180, 120, 150))
    # rain + fog
    img = Image.alpha_composite(img, rain_layer((W, H), density=1100, length=75, alpha=90, seed=4))
    img = Image.alpha_composite(img, fog_layer((W, H), (110, 125, 145), 55, seed=9))
    img = Image.alpha_composite(img, Image.new("RGBA", (W, H), (10, 12, 22, 38)))
    img = img.convert("RGB")
    save(finish_bg(img, 0.72, 0.06, 0.4, seed=17), out("backgrounds", "bg_street.jpg"))


# ---------------------------------------------------------------------------
# 9. UNDERGROUND RITUAL ROOM
# ---------------------------------------------------------------------------
def underground():
    base = canvas("#1a1114", "#050305")
    img = base
    grad = polygon_gradient((W, H), [(0, 0), (W, 0), (W, 720), (0, 720)], "#2a1a1c", "#0c080a")
    img = Image.alpha_composite(img, grad)
    floor = polygon_gradient((W, H), [(0, 720), (W, 720), (W, H), (0, H)], "#231518", "#080506")
    img = Image.alpha_composite(img, floor)
    # circular chamber
    d = d_of(img)
    d.ellipse([120, 300, 1800, 1060], outline=(44, 30, 31, 255), width=22)
    d.ellipse([220, 390, 1700, 1000], outline=(58, 38, 38, 255), width=8)
    # brick texture
    for y in range(0, 720, 44):
        for x in range(0, W, 90):
            off = 45 if (y // 44) % 2 else 0
            d.rectangle([x + off, y, x + off + 84, y + 38], outline=(12, 8, 9, 80), width=1)
    # chalk sigil on floor
    d = d_of(img)
    cx, cy = 960, 900
    for r in (180, 260, 340):
        d.ellipse([cx - r, cy - r * 0.42, cx + r, cy + r * 0.42], outline=(143, 128, 100, 70), width=3)
    for i in range(12):
        ang = i * math.pi / 6
        x = cx + math.cos(ang) * 330
        y = cy + math.sin(ang) * 138
        d.line([(cx, cy), (x, y)], fill=(130, 115, 90, 50), width=2)
    # chairs facing wall (ritual)
    for i, x in enumerate([430, 700, 970, 1240, 1510]):
        d = d_of(img)
        y = 640 + abs(i - 2) * 12
        d.rectangle([x - 45, y - 110, x + 45, y], fill=(35, 24, 22, 255))
        d.rectangle([x - 38, y - 100, x + 38, y - 45], fill=(47, 33, 29, 255))
        d.rectangle([x - 55, y - 10, x + 55, y + 18], fill=(29, 20, 19, 255))
        d.rectangle([x - 50, y + 18, x - 38, y + 90], fill=(24, 17, 16, 255))
        d.rectangle([x + 38, y + 18, x + 50, y + 90], fill=(24, 17, 16, 255))
    # candles
    for x, y in [(300, 700), (1620, 720), (520, 900), (1420, 940), (960, 780)]:
        img = candle(img, (x, y), height=50, glow=(220, 105, 45))
    # candles on wall sconces
    for x, y in [(240, 420), (1680, 420)]:
        d = d_of(img)
        d.rectangle([x - 10, y, x + 10, y + 90], fill=(32, 24, 22, 255))
        img = candle(img, (x, y), height=40)
    # drain
    d = d_of(img)
    d.ellipse([880, 830, 1040, 930], fill=(9, 6, 7, 255), outline=(72, 56, 48, 255), width=4)
    for i in range(6):
        d.line([(900 + i * 24, 850), (900 + i * 24, 910)], fill=(35, 28, 25, 255), width=3)
    # chains
    for x in (700, 1220):
        for y in range(0, 420, 18):
            d.ellipse([x - 6, y, x + 6, y + 14], outline=(58, 54, 50, 180), width=2)
    # red light
    img = Image.alpha_composite(img, radial_glow((W, H), (960, 500), 650, (130, 20, 26), 65, 2.0))
    img = Image.alpha_composite(img, fog_layer((W, H), (130, 90, 90), 45, seed=4))
    img = dust_motes(img, 80, seed=3, alpha=50)
    img = img.convert("RGB")
    save(finish_bg(img, 0.82, 0.055, 0.4, seed=18), out("backgrounds", "bg_underground.jpg"))


# ---------------------------------------------------------------------------
# 10. BASEMENT
# ---------------------------------------------------------------------------
def basement():
    base = canvas("#1c1b18", "#060605")
    img = base
    grad = polygon_gradient((W, H), [(0, 0), (W, 0), (W, 700), (0, 700)], "#2c2a25", "#12110f")
    img = Image.alpha_composite(img, grad)
    floor = polygon_gradient((W, H), [(0, 700), (W, 700), (W, H), (0, H)], "#25231e", "#080706")
    img = Image.alpha_composite(img, floor)
    # brick walls
    d = d_of(img)
    for y in range(0, 720, 50):
        for x in range(0, W, 110):
            off = 55 if (y // 50) % 2 else 0
            d.rectangle([x + off, y, x + off + 104, y + 44], outline=(13, 12, 11, 110), width=2)
            if random.Random(x * 7 + y).random() < 0.12:
                d.rectangle([x + off + 4, y + 4, x + off + 100, y + 40], fill=(20, 19, 16, 90))
    # stairs left
    d = d_of(img)
    for i in range(9):
        x = 70 + i * 42
        y = 220 + i * 50
        d.polygon([(x, y), (x + 250, y - 70), (x + 250, y - 50), (x, y + 20)], fill=(42, 39, 32, 255))
        d.polygon([(x, y + 20), (x + 250, y - 50), (x + 250, y - 35), (x, y + 35)], fill=(31, 29, 24, 255))
    # boiler
    d = d_of(img)
    d.rectangle([1300, 350, 1660, 760], fill=(38, 42, 40, 255))
    d.ellipse([1330, 380, 1630, 560], fill=(49, 54, 50, 255))
    d.ellipse([1380, 430, 1580, 540], fill=(25, 28, 27, 255))
    d.rectangle([1340, 600, 1390, 760], fill=(28, 31, 30, 255))
    d.rectangle([1570, 600, 1620, 760], fill=(28, 31, 30, 255))
    d.ellipse([1440, 640, 1480, 680], fill=(110, 80, 40, 200))
    # pipes
    for y in (300, 330):
        d.line([(0, y), (1300, y + 18)], fill=(48, 43, 36, 255), width=14)
        d.line([(0, y - 4), (1300, y + 14)], fill=(70, 62, 50, 180), width=3)
        for x in range(100, 1300, 220):
            d.rectangle([x, y - 10, x + 22, y + 28], fill=(60, 53, 43, 255))
    # hanging bulb
    img = hanging_bulb(img, (1000, 150), cable=120, glow=(230, 184, 112), strength=120, radius=620)
    # shelves / boxes
    d = d_of(img)
    d.rectangle([1720, 500, 1900, 900], fill=(30, 27, 22, 255))
    for y in (580, 700, 810):
        d.line([(1720, y), (1900, y)], fill=(40, 36, 29, 255), width=7)
    img = Image.alpha_composite(img, cardboard_box(img, (1000, 760, 1250, 980), seed=4))
    img = Image.alpha_composite(img, cardboard_box(img, (480, 820, 740, 1040), seed=5, label=True))
    # locked door back center
    img = Image.alpha_composite(img, door(img, (820, 330, 1090, 740), open_amount=0.0, color=(29, 23, 20), frame=(45, 36, 30), glow=(120, 30, 32), seed=6))
    d = d_of(img)
    d.rectangle([900, 300, 1020, 330], fill=(18, 15, 13, 255))
    d.text((920, 308), "KEEP OUT", fill=(120, 44, 40, 220))
    # water puddle
    d = d_of(img)
    d.ellipse([420, 940, 980, 1060], fill=(14, 18, 20, 180))
    d.ellipse([500, 970, 900, 1040], outline=(75, 82, 84, 60), width=2)
    # atmosphere
    img = Image.alpha_composite(img, fog_layer((W, H), (130, 120, 100), 35, seed=7))
    img = dust_motes(img, 90, seed=8, alpha=45)
    img = stains(img, [(300, 600, 200), (1500, 450, 160)], color=(5, 5, 4), alpha=90, seed=6)
    img = img.convert("RGB")
    save(finish_bg(img, 0.83, 0.055, 0.33, seed=19), out("backgrounds", "bg_basement.jpg"))


# ---------------------------------------------------------------------------
# 11. HIDDEN ROOM
# ---------------------------------------------------------------------------
def hiddenroom():
    base = canvas("#221915", "#070505")
    img = base
    grad = polygon_gradient((W, H), [(0, 0), (W, 0), (W, 700), (0, 700)], "#38261f", "#150d0b")
    img = Image.alpha_composite(img, grad)
    floor = polygon_gradient((W, H), [(0, 700), (W, 700), (W, H), (0, H)], "#2b1e18", "#0b0706")
    img = Image.alpha_composite(img, floor)
    # narrow room walls
    d = d_of(img)
    d.polygon([(0, 0), (280, 120), (280, 800), (0, 980)], fill=(43, 31, 25, 255))
    d.polygon([(W, 0), (1640, 120), (1640, 800), (W, 980)], fill=(36, 26, 21, 255))
    d.polygon([(0, 980), (280, 800), (1640, 800), (W, 980)], fill=(29, 20, 16, 255))
    # wall bricks
    for y in range(100, 800, 42):
        for x in range(280, 1640, 100):
            off = 50 if (y // 42) % 2 else 0
            d.rectangle([x + off, y, x + off + 94, y + 36], outline=(16, 11, 9, 80), width=1)
    # child drawings on walls
    rng = random.Random(5)
    for i in range(9):
        x = 330 + (i % 3) * 430 + rng.randint(-30, 30)
        y = 160 + (i // 3) * 190 + rng.randint(-20, 20)
        d.rectangle([x, y, x + 170, y + 140], fill=(176, 166, 143, 210))
        dd = d_of(img)
        # stick figures
        dd.ellipse([x + 62, y + 22, x + 106, y + 66], outline=(50, 42, 36, 220), width=4)
        dd.line([(x + 84, y + 66), (x + 84, y + 108)], fill=(50, 42, 36, 220), width=4)
        dd.line([(x + 84, y + 78), (x + 56, y + 98)], fill=(50, 42, 36, 220), width=4)
        dd.line([(x + 84, y + 78), (x + 112, y + 98)], fill=(50, 42, 36, 220), width=4)
        dd.line([(x + 84, y + 108), (x + 66, y + 132)], fill=(50, 42, 36, 220), width=4)
        dd.line([(x + 84, y + 108), (x + 102, y + 132)], fill=(50, 42, 36, 220), width=4)
        # scribbled eyes in corner
        dd.ellipse([x + 20, y + 90, x + 42, y + 112], outline=(110, 20, 20, 160), width=3)
        dd.ellipse([x + 27, y + 97, x + 35, y + 105], fill=(110, 20, 20, 160))
    # red string web
    d = d_of(img)
    pins = [(360, 180), (830, 220), (1240, 200), (1500, 360), (1080, 560), (600, 500), (390, 660)]
    for i, p in enumerate(pins):
        for q in pins[i + 1:]:
            if rng.random() < 0.5:
                d.line([p, q], fill=(118, 24, 26, 120), width=2)
    for x, y in pins:
        d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=(160, 36, 34, 255))
    # little bed left
    d = d_of(img)
    d.rectangle([300, 640, 700, 810], fill=(53, 38, 28, 255))
    d.rectangle([320, 620, 680, 690], fill=(85, 69, 51, 255))
    d.rectangle([340, 660, 470, 700], fill=(150, 137, 115, 255))
    d.rectangle([310, 810, 330, 900], fill=(35, 24, 19, 255))
    d.rectangle([670, 810, 690, 900], fill=(35, 24, 19, 255))
    # tape recorder on chair
    d = d_of(img)
    d.rectangle([1120, 620, 1320, 780], fill=(39, 30, 23, 255))
    d.rectangle([1090, 580, 1350, 630], fill=(58, 45, 33, 255))
    d.rectangle([1140, 520, 1290, 590], fill=(24, 22, 21, 255))
    d.rectangle([1160, 535, 1270, 575], fill=(55, 54, 48, 255))
    d.ellipse([1168, 542, 1196, 570], outline=(120, 118, 102, 255), width=2)
    d.ellipse([1234, 542, 1262, 570], outline=(120, 118, 102, 255), width=2)
    d.rectangle([1180, 578, 1240, 586], fill=(100, 34, 32, 200))
    # shrine of photos center
    d = d_of(img)
    d.rectangle([790, 470, 1070, 700], fill=(45, 32, 24, 255))
    for i in range(3):
        d.rectangle([810 + i * 80, 500, 870 + i * 80, 590], fill=(145, 136, 115, 230))
        d.ellipse([826 + i * 80, 515, 854 + i * 80, 545], fill=(70, 60, 50, 255))
        d.rectangle([818 + i * 80, 545, 862 + i * 80, 580], fill=(80, 66, 54, 255))
    # candles
    for x, y in [(760, 740), (1100, 760)]:
        img = candle(img, (x, y), height=44, glow=(220, 120, 60))
    # hanging bulb
    img = hanging_bulb(img, (960, 140), cable=100, glow=(235, 180, 100), strength=100, radius=540)
    # doorway behind (the wall we came through)
    d = d_of(img)
    d.rectangle([880, 240, 1080, 460], fill=(8, 7, 6, 255))
    d = d_of(img)
    d.rectangle([864, 224, 1096, 464], outline=(26, 20, 16, 255), width=10)
    # dust/atmosphere
    img = Image.alpha_composite(img, fog_layer((W, H), (140, 115, 90), 40, seed=4))
    img = dust_motes(img, 120, seed=5, alpha=55)
    img = stains(img, [(500, 400, 160), (1200, 640, 130)], seed=7)
    img = img.convert("RGB")
    save(finish_bg(img, 0.8, 0.06, 0.35, seed=20), out("backgrounds", "bg_hiddenroom.jpg"))


# ---------------------------------------------------------------------------
# 12. SUPERNATURAL DIMENSION
# ---------------------------------------------------------------------------
def void():
    base = canvas("#060208", "#010002")
    img = base
    # blood-red nebula
    n = noise((W, H), scale=2.0, seed=8, octaves=5)
    arr = np.zeros((H, W, 4), dtype=np.uint8)
    arr[..., 0] = 130
    arr[..., 1] = 20
    arr[..., 2] = 34
    arr[..., 3] = (np.clip((n - 0.42) * 2.8, 0, 1) * 115).astype(np.uint8)
    img = Image.alpha_composite(img, Image.fromarray(arr, "RGBA").filter(ImageFilter.GaussianBlur(30)))
    img = Image.alpha_composite(img, radial_glow((W, H), (960, 420), 900, (110, 18, 30), 80, 2.2))
    # hanging doors and mirrors floating
    rng = random.Random(4)
    for i in range(9):
        x = rng.randint(80, 1700)
        y = rng.randint(80, 760)
        w = rng.randint(90, 220)
        h = rng.randint(180, 380)
        ang = rng.uniform(-8, 8)
        # draw rotated via overlay
        l = layer()
        d = d_of(l)
        d.rectangle([x, y, x + w, y + h], fill=(9, 9, 12, 235), outline=(61, 54, 58, 210), width=5)
        d.rectangle([x + 12, y + 12, x + w - 12, y + h - 12], fill=(17, 16, 21, 220))
        if i % 3 == 0:
            # mirror surface with pale eye
            d.ellipse([x + w * 0.25, y + h * 0.35, x + w * 0.75, y + h * 0.65], outline=(180, 172, 180, 70), width=5)
            d.ellipse([x + w * 0.42, y + h * 0.44, x + w * 0.58, y + h * 0.56], fill=(150, 20, 30, 130))
        l = l.rotate(ang, resample=Image.BICUBIC, expand=False)
        img = Image.alpha_composite(img, l)
    # broken floor grid
    d = d_of(img)
    for i in range(-8, 18):
        d.line([(960, 760), (i * 160 - 500, H)], fill=(55, 45, 52, 70), width=2)
    for y in range(780, H, 60):
        d.line([(0, y), (W, y - 40)], fill=(55, 45, 52, 55), width=2)
    # giant eye in sky
    d = d_of(img)
    cx, cy = 960, 260
    d.arc([cx - 360, cy - 140, cx + 360, cy + 140], 180, 360, fill=(120, 115, 125, 30), width=10)
    d.arc([cx - 360, cy - 60, cx + 360, cy + 220], 0, 180, fill=(120, 115, 125, 22), width=7)
    d.ellipse([cx - 130, cy - 110, cx + 130, cy + 110], outline=(150, 140, 150, 45), width=8)
    d.ellipse([cx - 40, cy - 35, cx + 40, cy + 35], fill=(120, 20, 28, 100))
    # cracks of red light
    rng = random.Random(9)
    for i in range(7):
        x = rng.randint(0, W)
        pts = [(x, rng.randint(500, 800))]
        for _ in range(6):
            x += rng.randint(-120, 120)
            y = pts[-1][1] + rng.randint(20, 90)
            pts.append((x, y))
        d.line(pts, fill=(180, 30, 40, 60), width=3)
    # embers
    dust = layer()
    dd = d_of(dust)
    for i in range(160):
        x = rng.uniform(0, W)
        y = rng.uniform(0, H)
        r = rng.uniform(0.5, 2.5)
        dd.ellipse([x - r, y - r, x + r, y + r], fill=(220, 80, 70, rng.randint(25, 100)))
    img = Image.alpha_composite(img, dust)
    img = Image.alpha_composite(img, fog_layer((W, H), (150, 60, 70), 36, seed=6))
    img = img.convert("RGB")
    save(finish_bg(img, 0.88, 0.07, 0.45, seed=21), out("backgrounds", "bg_void.jpg"))


# ---------------------------------------------------------------------------
# 13. MAIN MENU
# ---------------------------------------------------------------------------
def menu_bg():
    base = canvas("#181420", "#030305")
    img = base
    grad = polygon_gradient((W, H), [(0, 0), (W, 0), (W, 720), (0, 720)], "#2a2233", "#0c0a12")
    img = Image.alpha_composite(img, grad)
    floor = polygon_gradient((W, H), [(0, 720), (W, 720), (W, H), (0, H)], "#241a1f", "#080506")
    img = Image.alpha_composite(img, floor)
    floor_boards(img, 720, (1300, 720), seed=8)
    # tall window right
    win_l, _ = window(img, (1250, 80, 1780, 620), night=True, rain=True, blinds=False, seed=31)
    img = Image.alpha_composite(img, win_l)
    img = Image.alpha_composite(img, light_shaft((W, H), [(1280, 500), (1750, 470), (1320, 1080), (760, 1080)], (90, 120, 170), 40))
    # mirror left
    d = d_of(img)
    d.rectangle([80, 140, 520, 680], fill=(14, 12, 16, 255))
    d.rectangle([100, 160, 500, 660], fill=(40, 45, 55, 255))
    refl = polygon_gradient((W, H), [(100, 160), (500, 160), (500, 660), (100, 660)], "#3b4250", "#08090d")
    img = Image.alpha_composite(img, refl)
    # ghostly girl in mirror (abstract)
    d = d_of(img)
    d.ellipse([255, 260, 345, 360], fill=(148, 150, 160, 35))
    d.polygon([(240, 360), (360, 360), (390, 660), (210, 660)], fill=(120, 122, 132, 25))
    d.rectangle([70, 130, 530, 150], fill=(29, 24, 22, 255))
    # hanging light
    img = hanging_bulb(img, (980, 150), cable=160, glow=(240, 196, 126), strength=90, radius=650)
    # old chair silhouette center-right
    d = d_of(img)
    d.rectangle([980, 560, 1110, 880], fill=(18, 14, 15, 255))
    d.rectangle([950, 540, 1140, 580], fill=(25, 19, 19, 255))
    d.rectangle([960, 880, 1130, 910], fill=(14, 11, 12, 255))
    # red door far center
    img = Image.alpha_composite(img, door(img, (760, 300, 940, 740), open_amount=0.16, color=(34, 22, 22), frame=(46, 31, 28), glow=(130, 28, 32), seed=9))
    # paper scraps / petals on floor
    rng = random.Random(3)
    for i in range(30):
        x = rng.uniform(0, W)
        y = rng.uniform(820, 1060)
        d.polygon([(x, y), (x + rng.uniform(8, 20), y + rng.uniform(-4, 4)), (x + rng.uniform(6, 16), y + rng.uniform(5, 12))],
                  fill=(150, 140, 120, rng.randint(10, 45)))
    # atmosphere
    img = Image.alpha_composite(img, fog_layer((W, H), (130, 125, 145), 42, seed=5))
    img = dust_motes(img, 140, seed=6, alpha=55)
    img = stains(img, [(400, 500, 200), (1200, 800, 180)], seed=6)
    img = img.convert("RGB")
    save(finish_bg(img, 0.8, 0.05, 0.42, seed=31), out("backgrounds", "bg_menu.jpg"))


# ---------------------------------------------------------------------------
# 14. PHONE PHOTO (sleeping Ethan)
# ---------------------------------------------------------------------------
def phone_photo():
    """A creepy phone snapshot of Ethan asleep, generated as a CG-style image."""
    Wp, Hp = 900, 1200
    im = vertical_gradient((Wp, Hp), "#12161d", "#050608").convert("RGBA")
    d = d_of(im)
    # bed / pillow perspective
    d.polygon([(0, 700), (900, 660), (900, 1200), (0, 1200)], fill=(33, 36, 40, 255))
    d.polygon([(0, 300), (620, 260), (900, 420), (900, 800), (0, 820)], fill=(55, 54, 54, 255))
    # blanket
    d.polygon([(0, 760), (900, 720), (900, 1200), (0, 1200)], fill=(42, 45, 49, 255))
    for i in range(9):
        d.line([(60 + i * 95, 780), (30 + i * 95, 1180)], fill=(30, 33, 37, 255), width=12)
    # sleeping head (dark silhouette on pillow)
    d.ellipse([230, 430, 580, 760], fill=(28, 27, 30, 255))
    d.ellipse([260, 470, 540, 720], fill=(23, 23, 26, 255))
    # hair
    d.polygon([(220, 520), (280, 400), (470, 380), (600, 470), (560, 550), (520, 480), (400, 460), (300, 500), (260, 600)], fill=(10, 10, 13, 255))
    # closed eye lines
    d.line([(320, 590), (370, 600)], fill=(90, 70, 65, 255), width=4)
    d.line([(450, 600), (500, 590)], fill=(90, 70, 65, 255), width=4)
    d.line([(390, 660), (440, 665)], fill=(75, 58, 55, 255), width=3)
    # strange figure standing at foot of bed (dark, barely visible)
    d.ellipse([610, 300, 690, 390], fill=(4, 4, 6, 255))
    d.polygon([(580, 390), (720, 390), (760, 760), (540, 760)], fill=(4, 4, 6, 255))
    d.ellipse([630, 330, 648, 348], fill=(150, 150, 145, 90))
    d.ellipse([658, 330, 676, 348], fill=(150, 150, 145, 90))
    # timestamp
    d.text((40, 40), "03:00:07", fill=(210, 60, 60, 220))
    im = im.convert("RGB")
    im = grain(im, 0.12, seed=5)
    im = vignette(im, 0.8)
    save(im, out("cg", "cg_phone_photo.jpg"))


if __name__ == "__main__":
    import sys
    which = sys.argv[1:] or ["all"]
    funcs = {
        "bedroom": bedroom, "bedroom_day": lambda: bedroom(True), "livingroom": livingroom,
        "hallway": hallway, "bathroom": bathroom, "kitchen": kitchen, "school": school,
        "classroom": classroom, "street": street, "underground": underground,
        "basement": basement, "hiddenroom": hiddenroom, "void": void,
        "menu": menu_bg, "phone_photo": phone_photo,
    }
    if "all" in which:
        for fn in funcs.values():
            fn()
    else:
        for w in which:
            funcs[w]()
