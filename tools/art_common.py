"""Shared painting utilities for DON'T LOOK BEHIND YOU.

All artwork in this project is authored procedurally from scratch with
Pillow + cairo. No third-party images are used.
"""
from __future__ import annotations

import math
import os
import random
from contextlib import contextmanager

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(ROOT, "game", "images")


def out(*parts: str) -> str:
    path = os.path.join(IMG, *parts)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def rgb(value):
    if isinstance(value, tuple):
        return value[:3]
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def rgba(value: str, alpha=255):
    r, g, b = rgb(value)
    return (r, g, b, alpha)


def mix(c1, c2, t):
    if isinstance(c1, str):
        c1 = rgb(c1)
    if isinstance(c2, str):
        c2 = rgb(c2)
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def gradient(size, top, bottom, horizontal=False):
    """Linear gradient RGB image."""
    w, h = size
    if isinstance(top, str):
        top = rgb(top)
    if isinstance(bottom, str):
        bottom = rgb(bottom)
    n = w if horizontal else h
    t = np.linspace(0.0, 1.0, n, dtype=np.float32)[:, None]
    a = np.array(top, dtype=np.float32)[None, :]
    b = np.array(bottom, dtype=np.float32)[None, :]
    line = (a + (b - a) * t).astype(np.uint8)
    if horizontal:
        arr = np.repeat(line[None, :, :], h, axis=0)
    else:
        arr = np.repeat(line[:, None, :], w, axis=1)
    return Image.fromarray(arr, "RGB")


def vertical_gradient(size, top, bottom):
    return gradient(size, top, bottom, horizontal=False)


def radial_glow(size, center, radius, color, strength=255, falloff=2.2, aspect=1.0):
    """RGBA radial glow."""
    w, h = size
    if isinstance(color, str):
        color = rgb(color)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx = (xx - center[0]) / max(1.0, radius * aspect)
    dy = (yy - center[1]) / max(1.0, radius)
    d = np.sqrt(dx * dx + dy * dy)
    a = np.clip(1.0 - d, 0.0, 1.0) ** falloff * strength
    arr = np.zeros((h, w, 4), dtype=np.uint8)
    arr[..., 0] = color[0]
    arr[..., 1] = color[1]
    arr[..., 2] = color[2]
    arr[..., 3] = a.astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def add_glow(base, center, radius, color, strength=180, falloff=2.3, blend=ImageChops.add):
    glow = radial_glow(base.size, center, radius, color, strength, falloff)
    layer = Image.new("RGB", base.size, (0, 0, 0))
    layer.paste(glow, (0, 0), glow)
    return Image.blend(base, ImageChops.add(base, layer), 0.85)


def add_screen_glow(base, center, radius, color, strength=160, falloff=2.0):
    glow = radial_glow(base.size, center, radius, color, strength, falloff)
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    layer = Image.alpha_composite(layer, glow)
    out = Image.alpha_composite(base.convert("RGBA"), layer)
    return out.convert(base.mode)


def noise(size, scale=1.0, seed=0, octaves=4):
    """Fractal value noise in 0..1."""
    rng = np.random.default_rng(seed)
    w, h = size
    total = np.zeros((h, w), dtype=np.float32)
    amp = 1.0
    norm = 0.0
    for o in range(octaves):
        gw = max(2, int(w / (scale * (2 ** (octaves - o - 1)))))
        gh = max(2, int(h / (scale * (2 ** (octaves - o - 1)))))
        g = rng.random((gh, gw)).astype(np.float32)
        layer = np.array(Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC), dtype=np.float32) / 255.0
        total += layer * amp
        norm += amp
        amp *= 0.5
    total /= norm
    return total


def tex_overlay(base, color=(12, 12, 18), amount=0.10, scale=3.0, seed=1):
    n = noise(base.size, scale=scale, seed=seed)
    n = (n - n.min()) / max(1e-5, n.max() - n.min())
    layer = Image.fromarray((n * 255).astype(np.uint8)).convert("RGB")
    tint = Image.new("RGB", base.size, color)
    layer = ImageChops.multiply(layer, tint)
    return Image.blend(base, ImageChops.add(base, ImageChops.multiply(layer, Image.new("RGB", base.size, (80, 80, 80)))), amount)


def grain(base, amount=0.045, seed=7):
    rng = np.random.default_rng(seed)
    w, h = base.size
    n = rng.normal(0, 1, (h, w, 1)).astype(np.float32)
    arr = np.asarray(base.convert("RGB"), dtype=np.float32) / 255.0
    arr = np.clip(arr + n * amount, 0, 1)
    return Image.fromarray((arr * 255).astype(np.uint8), "RGB")


def vignette(base, strength=0.72, radius=0.75, color=(0, 0, 0)):
    w, h = base.size
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, cy = w / 2, h / 2
    d = np.sqrt(((xx - cx) / (w * radius)) ** 2 + ((yy - cy) / (h * radius)) ** 2)
    v = np.clip((d - 0.55) / 1.1, 0, 1) ** 1.4 * strength
    arr = np.asarray(base.convert("RGB"), dtype=np.float32)
    dark = np.array(color, dtype=np.float32)
    arr = arr * (1 - v[..., None]) + dark * v[..., None]
    return Image.fromarray(arr.astype(np.uint8), "RGB")


def bloom(base, threshold=170, radius=28, strength=0.55):
    arr = np.asarray(base.convert("RGB"), dtype=np.float32)
    mask = np.clip((arr - threshold) / (255 - threshold), 0, 1)
    bright = (arr * mask).astype(np.uint8)
    blur = Image.fromarray(bright, "RGB").filter(ImageFilter.GaussianBlur(radius))
    return Image.blend(base, ImageChops.add(base, blur), strength)


def soft_blur(base, radius=0.6):
    return base.filter(ImageFilter.GaussianBlur(radius))


def paste_soft(base, sprite, xy, shadow=True):
    base = base.convert("RGBA")
    sprite = sprite.convert("RGBA")
    if shadow:
        sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
        sh.paste(Image.new("RGBA", sprite.size, (0, 0, 0, 100)), xy, sprite)
        sh = sh.filter(ImageFilter.GaussianBlur(14))
        base = Image.alpha_composite(base, sh)
    base.alpha_composite(sprite, xy)
    return base


def rain_layer(size, density=420, length=48, alpha=90, angle=8, seed=3, color=(190, 210, 235)):
    w, h = size
    rng = random.Random(seed)
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(density):
        x = rng.uniform(-100, w + 100)
        y = rng.uniform(-100, h + 100)
        ln = rng.uniform(length * 0.4, length)
        a = int(alpha * rng.uniform(0.35, 1.0))
        d.line([(x, y), (x + math.tan(math.radians(angle)) * ln, y + ln)], fill=color + (a,), width=rng.choice([1, 1, 2]))
    return layer


def fog_layer(size, color=(150, 160, 175), alpha=70, seed=2, scale=4.0):
    n = noise(size, scale=scale, seed=seed, octaves=5)
    n = np.clip((n - 0.35) * 2.2, 0, 1)
    arr = np.zeros((size[1], size[0], 4), dtype=np.uint8)
    arr[..., 0] = color[0]
    arr[..., 1] = color[1]
    arr[..., 2] = color[2]
    arr[..., 3] = (n * alpha).astype(np.uint8)
    layer = Image.fromarray(arr, "RGBA").filter(ImageFilter.GaussianBlur(9))
    return layer


def light_shaft(size, poly, color=(210, 225, 255), alpha=60):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).polygon(poly, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(22))
    glow = radial_glow(size, (sum(p[0] for p in poly) / len(poly), 0), size[1] * 0.7, color, alpha * 2)
    layer.paste(glow, (0, 0), ImageChops.multiply(glow.getchannel("A"), mask))
    return layer


def polygon_gradient(size, points, top, bottom, alpha=255):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).polygon(points, fill=alpha)
    g = vertical_gradient(size, top, bottom).convert("RGBA")
    layer.paste(g, (0, 0), mask)
    return layer


def rounded_rect_gradient(size, box, radius, top, bottom, outline=None, width=2, alpha=255):
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(box, radius=radius, fill=alpha)
    g = vertical_gradient(size, top, bottom).convert("RGBA")
    layer.paste(g, (0, 0), mask)
    d = ImageDraw.Draw(layer)
    if outline:
        d.rounded_rectangle(box, radius=radius, outline=outline, width=width)
    return layer


def finish_bg(img, vignette_strength=0.7, grain_amount=0.04, bloom_strength=0.28, seed=9):
    img = bloom(img, threshold=175, radius=30, strength=bloom_strength)
    img = vignette(img, strength=vignette_strength)
    img = grain(img, grain_amount, seed=seed)
    return img


def save(img, path, quality=95):
    if path.endswith(".jpg"):
        img.convert("RGB").save(path, quality=quality, subsampling=1)
    else:
        img.save(path)
    print("wrote", path, img.size)


def perspective_floor(size, horizon, vanish_x, color_near, color_far, y_top=None):
    w, h = size
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    if y_top is None:
        y_top = horizon
    # gradient via horizontal bands
    for y in range(y_top, h):
        t = (y - y_top) / max(1, (h - y_top))
        c = mix(color_far, color_near, t ** 0.7)
        d.line([(0, y), (w, y)], fill=c + (255,))
    # perspective seams
    for i in range(-8, 25):
        x_bottom = vanish_x + (i - 8) * (w / 9.5)
        d.line([(vanish_x, y_top), (x_bottom, h)], fill=(0, 0, 0, 28), width=1)
    return layer


@contextmanager
def highres(base_size, scale=2):
    """Create a supersampled RGB canvas and yield (canvas, draw)."""
    w, h = base_size
    c = Image.new("RGB", (w * scale, h * scale), (0, 0, 0))
    yield c
    # caller downsamples with down()


def down(img, size):
    return img.resize(size, Image.LANCZOS)


def make_dust_sprite(size=22, color=(230, 228, 218)):
    """Soft mote for the menu particle system."""
    s = size * 4
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    for i in range(5, 0, -1):
        a = int(150 * (i / 5) ** 2)
        r = int((s / 2 - 2) * (i / 5))
        d.ellipse([s / 2 - r, s / 2 - r, s / 2 + r, s / 2 + r], fill=color + (a,))
    return im.resize((size, size), Image.LANCZOS)


def make_glitch_strip(size, seed, color=(180, 30, 42), bars=10):
    w, h = size
    rng = random.Random(seed)
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(bars):
        y = rng.randrange(h)
        bh = rng.randrange(1, 10)
        a = rng.randrange(20, 130)
        c = color if rng.random() < 0.6 else (220, 220, 230)
        d.rectangle([0, y, w, y + bh], fill=c + (a,))
        if rng.random() < 0.4:
            x = rng.randrange(w)
            d.rectangle([x, y - 2, x + rng.randrange(20, 180), y + bh + 2], fill=(0, 0, 0, 150))
    return layer
