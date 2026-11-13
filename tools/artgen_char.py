"""Original anime character sprite generator.

Characters are drawn as vector art with cairo: cel-shaded skin, layered hair,
large expressive eyes and nine expressions per character. Everything is
authored from code so the cast stays consistent across sprites and CGs.
"""
from __future__ import annotations

import math
import os

import cairo
import numpy as np
from PIL import Image, ImageFilter, ImageChops

from art_common import rgb, rgba, out, mix, vertical_gradient, grain

W, H = 900, 1500
S = 2  # supersampling

EXPRESSIONS = [
    "neutral", "happy", "sad", "angry", "scared",
    "crying", "surprised", "evil", "shocked",
]

PALETTES = {
    "ethan": {
        "skin": "#e7c1b0", "skin_shadow": "#c39084", "skin_light": "#f2d6c8",
        "hair": "#20232f", "hair_light": "#38445e", "hair_dark": "#0d0f16",
        "brow": "#171923", "iris": "#c98a38", "iris_dark": "#6f4215", "iris_light": "#f0c774",
        "lash": "#2a2026", "mouth": "#944f50", "mouth_dark": "#4d2228",
        "outfit": "#2c3547", "outfit_dark": "#1a202c", "outfit_light": "#43526c",
        "shirt": "#b9b3a4", "accent": "#8e3b3f", "line": "#16141a",
    },
    "maya": {
        "skin": "#f0cbb5", "skin_shadow": "#c9947d", "skin_light": "#fbdfcc",
        "hair": "#5b3527", "hair_light": "#8f5638", "hair_dark": "#2e1812",
        "brow": "#4b2b20", "iris": "#7c4a28", "iris_dark": "#3f2210", "iris_light": "#c58a54",
        "lash": "#3a2420", "mouth": "#a95555", "mouth_dark": "#5d2528",
        "outfit": "#c2a258", "outfit_dark": "#8f733a", "outfit_light": "#ddc077",
        "shirt": "#e9e0cd", "accent": "#2f6d6a", "line": "#211915",
    },
    "girl": {
        "skin": "#e6e0e8", "skin_shadow": "#b6aebb", "skin_light": "#f7f3f8",
        "hair": "#cbd2de", "hair_light": "#f4f6fb", "hair_dark": "#8d94a4",
        "brow": "#8d8fa0", "iris": "#7fa6c9", "iris_dark": "#3d5d7d", "iris_light": "#c4e0f2",
        "lash": "#5a5563", "mouth": "#9b6b72", "mouth_dark": "#5b313a",
        "outfit": "#c9cdd6", "outfit_dark": "#8e949f", "outfit_light": "#eef0f4",
        "shirt": "#d9dce3", "accent": "#8f2d3c", "line": "#4d4a57",
    },
    "entity": {
        "skin": "#232128", "skin_shadow": "#121016", "skin_light": "#3a3540",
        "hair": "#070609", "hair_light": "#1c1720", "hair_dark": "#000000",
        "brow": "#000000", "iris": "#e8e5dc", "iris_dark": "#8f8a7e", "iris_light": "#ffffff",
        "lash": "#000000", "mouth": "#3a0c12", "mouth_dark": "#0c0204",
        "outfit": "#0d0c11", "outfit_dark": "#050407", "outfit_light": "#23202a",
        "shirt": "#151319", "accent": "#8f1f2c", "line": "#020203",
    },
}

# The parents share the cast's rendering style, with adult palettes and
# distinct silhouettes so their dialogue portraits remain recognizable.
PALETTES["mom"] = dict(
    PALETTES["maya"],
    skin="#e8c3b2", skin_shadow="#b68679", skin_light="#f5d8c8",
    hair="#77727a", hair_light="#aaa2a8", hair_dark="#49444e",
    brow="#55434a", iris="#786052", iris_dark="#42302a", iris_light="#baa08a",
    outfit="#39404a", outfit_dark="#242932", outfit_light="#565f6c",
    accent="#77616a",
)
PALETTES["dad"] = dict(
    PALETTES["ethan"],
    skin="#d8b4a3", skin_shadow="#a77c70", skin_light="#ead0c0",
    hair="#74675f", hair_light="#a19082", hair_dark="#413a38",
    brow="#403834", iris="#66564b", iris_dark="#352923", iris_light="#a08770",
    outfit="#3a3538", outfit_dark="#242124", outfit_light="#554d4d",
    shirt="#c0b7a8", accent="#74515a",
)


def rr(ctx, x, y, w, h, r):
    ctx.new_path()
    ctx.arc(x + r, y + r, r, math.pi, 1.5 * math.pi)
    ctx.arc(x + w - r, y + r, r, 1.5 * math.pi, 2 * math.pi)
    ctx.arc(x + w - r, y + h - r, r, 0, 0.5 * math.pi)
    ctx.arc(x + r, y + h - r, r, 0.5 * math.pi, math.pi)
    ctx.close_path()


def quad(ctx, x0, y0, cx, cy, x1, y1):
    ctx.curve_to(x0 + (cx - x0) * 2 / 3, y0 + (cy - y0) * 2 / 3,
                 x1 + (cx - x1) * 2 / 3, y1 + (cy - y1) * 2 / 3, x1, y1)


def ell(ctx, cx, cy, rx, ry, rot=0.0, a0=0.0, a1=2 * math.pi):
    ctx.save()
    ctx.translate(cx, cy)
    ctx.rotate(rot)
    ctx.scale(rx, ry)
    ctx.arc(0, 0, 1, a0, a1)
    ctx.restore()


def C(ctx, color, alpha=1.0):
    r, g, b = rgb(color)
    ctx.set_source_rgba(r / 255, g / 255, b / 255, alpha)


def grad(ctx, x0, y0, x1, y1, c0, c1, a0=1.0, a1=1.0):
    g = cairo.LinearGradient(x0, y0, x1, y1)
    r0, g0, b0 = rgb(c0)
    r1, g1, b1 = rgb(c1)
    g.add_color_stop_rgba(0, r0 / 255, g0 / 255, b0 / 255, a0)
    g.add_color_stop_rgba(1, r1 / 255, g1 / 255, b1 / 255, a1)
    ctx.set_source(g)


def fill_outline(ctx, fill=None, outline=None, width=3.0):
    if fill is not None:
        if isinstance(fill, tuple) and len(fill) == 3 and isinstance(fill[0], (int, float)):
            ctx.set_source_rgb(*fill)
        elif isinstance(fill, str):
            C(ctx, fill)
        else:
            ctx.set_source(fill)
    if fill is not None or outline is not None:
        if outline:
            ctx.fill_preserve()
        else:
            ctx.fill()
    if outline:
        C(ctx, outline)
        ctx.set_line_width(width)
        ctx.stroke()
    if fill is None and outline is None:
        ctx.new_path()


def face_path(ctx):
    ctx.new_path()
    ctx.move_to(450, 196)
    ctx.curve_to(536, 198, 584, 278, 590, 398)
    ctx.curve_to(594, 466, 578, 520, 544, 572)
    ctx.curve_to(516, 614, 480, 642, 450, 650)
    ctx.curve_to(420, 642, 384, 614, 356, 572)
    ctx.curve_to(322, 520, 306, 466, 310, 398)
    ctx.curve_to(316, 278, 364, 198, 450, 196)
    ctx.close_path()


def neck_path(ctx):
    ctx.new_path()
    ctx.move_to(404, 600)
    ctx.curve_to(408, 640, 405, 690, 393, 735)
    ctx.line_to(507, 735)
    ctx.curve_to(495, 690, 492, 640, 496, 600)
    ctx.close_path()


def draw_neck(ctx, pal, entity=False):
    grad(ctx, 380, 600, 520, 740, pal["skin_shadow"], pal["skin"], 1, 1)
    neck_path(ctx)
    fill_outline(ctx, outline=pal["line"], width=2.2)
    # shadow beneath jaw
    ctx.new_path()
    ctx.move_to(392, 610)
    ctx.curve_to(420, 655, 480, 655, 508, 610)
    ctx.curve_to(486, 668, 414, 668, 392, 610)
    ctx.close_path()
    C(ctx, pal["skin_shadow"], 0.85)
    ctx.fill()
    if entity:
        C(ctx, "#000000", 0.5)
        ctx.rectangle(400, 660, 100, 50)
        ctx.fill()


def draw_face(ctx, pal, expr, entity=False):
    grad(ctx, 320, 220, 590, 640, pal["skin_light"], pal["skin"], 1, 1)
    face_path(ctx)
    fill_outline(ctx, outline=pal["line"], width=2.6)

    # cheek shadow (right side)
    ctx.new_path()
    ctx.move_to(500, 390)
    ctx.curve_to(575, 410, 586, 500, 548, 566)
    ctx.curve_to(548, 500, 530, 430, 500, 390)
    ctx.close_path()
    C(ctx, pal["skin_shadow"], 0.45)
    ctx.fill()

    # forehead shadow from bangs
    ctx.new_path()
    ctx.move_to(320, 360)
    ctx.curve_to(360, 410, 540, 410, 586, 350)
    ctx.line_to(586, 300)
    ctx.line_to(320, 300)
    ctx.close_path()
    grad(ctx, 450, 300, 450, 420, pal["skin_shadow"], pal["skin"], 0.45, 0.0)
    ctx.fill()

    # nose
    ctx.new_path()
    ctx.move_to(455, 510)
    ctx.curve_to(450, 522, 444, 532, 439, 536)
    ctx.curve_to(447, 541, 456, 539, 461, 533)
    C(ctx, pal["skin_shadow"], 0.8)
    ctx.set_line_width(2.6)
    ctx.set_line_cap(cairo.LINE_CAP_ROUND)
    ctx.stroke()

    # expression extras
    if expr == "shocked":
        # sunken eyes
        for cx in (382, 518):
            ctx.new_path()
            ell(ctx, cx, 458, 54, 34, 0, 0, 2 * math.pi)
            C(ctx, "#6c5566", 0.20)
            ctx.fill()
    if expr in ("sad", "crying"):
        # faint under-eye shadow
        for cx in (382, 518):
            ctx.new_path()
            ell(ctx, cx, 486, 42, 14, 0, 0, 2 * math.pi)
            C(ctx, "#a4767f", 0.14)
            ctx.fill()
    if entity:
        # cracks
        cracks = [
            [(348, 300), (370, 360), (352, 410), (378, 450)],
            [(548, 330), (528, 380), (546, 430), (520, 470)],
            [(430, 220), (438, 280), (420, 320)],
            [(470, 600), (456, 560), (468, 520)],
        ]
        for pts in cracks:
            ctx.new_path()
            ctx.move_to(*pts[0])
            for p in pts[1:]:
                ctx.line_to(*p)
            C(ctx, "#000000", 0.55)
            ctx.set_line_width(2.4)
            ctx.stroke()
            ctx.new_path()
            ctx.move_to(pts[0][0] + 2, pts[0][1])
            for p in pts[1:]:
                ctx.line_to(p[0] + 2, p[1])
            C(ctx, pal["accent"], 0.35)
            ctx.set_line_width(1.2)
            ctx.stroke()


def draw_eyes(ctx, pal, expr, entity=False):
    closed = expr in ("happy", "crying")
    for idx, cx in enumerate((382, 518)):
        inward = 1 if idx == 0 else -1
        cy = 456
        sx = cx
        # expression geometry
        upper, lower = 33, 22
        iris_r = 21
        pupil_r = 8.5
        if expr == "sad":
            upper, lower = 27, 20
            cy += 2
        elif expr == "angry":
            upper, lower = 22, 18
            cy += 1
        elif expr == "scared":
            upper, lower = 42, 33
            iris_r, pupil_r = 18, 5.2
        elif expr == "surprised":
            upper, lower = 44, 34
            iris_r, pupil_r = 20, 6.5
        elif expr == "evil":
            upper, lower = 19, 23
            iris_r, pupil_r = 21, 4.5
        elif expr == "shocked":
            upper, lower = 49, 38
            iris_r, pupil_r = 16, 3.6
        elif expr == "crying":
            upper, lower = 25, 22

        eye_top = cy - upper
        eye_bot = cy + lower
        outer_x = cx - inward * 46
        inner_x = cx + inward * 40

        if closed:
            # closed / squeezed eyelids
            ctx.new_path()
            if expr == "happy":
                ctx.move_to(outer_x, cy + 2)
                ctx.curve_to(cx - inward * 20, cy - 28, cx + inward * 16, cy - 30, inner_x, cy - 1)
            else:
                ctx.move_to(outer_x, cy - 4)
                ctx.curve_to(cx - inward * 18, cy + 18, cx + inward * 16, cy + 18, inner_x, cy - 4)
            C(ctx, pal["lash"])
            ctx.set_line_width(7.5 if expr == "happy" else 6.5)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.stroke()
            # lashes
            ctx.new_path()
            ctx.move_to(outer_x - 2, cy - 4)
            ctx.line_to(outer_x - 14, cy - 14 if expr == "happy" else cy + 2)
            ctx.set_line_width(4)
            ctx.stroke()
            if expr == "crying":
                # tear streams
                for t in range(2):
                    tx = cx - inward * (10 + t * 22)
                    ty = cy + 6
                    length = 150 + idx * 40 + t * 20
                    grad(ctx, tx, ty, tx, ty + length, "#cfe6f2", "#8ec4dd", 0.85, 0.0)
                    ctx.new_path()
                    ctx.move_to(tx, ty)
                    ctx.curve_to(tx - 3, ty + length * 0.5, tx + 4, ty + length * 0.8, tx + 1, ty + length)
                    ctx.set_line_width(7)
                    ctx.stroke()
                ctx.new_path()
                ell(ctx, outer_x - 4, eye_bot + 22, 5, 8, 0, 0, 2 * math.pi)
                C(ctx, "#dceff8", 0.9)
                ctx.fill()
            continue

        # eye white
        ctx.new_path()
        ctx.move_to(outer_x, cy + 2)
        ctx.curve_to(outer_x + inward * 12, eye_top - 2, cx + inward * 6, eye_top - 4, inner_x, cy - 2)
        ctx.curve_to(cx + inward * 8, eye_bot + 2, outer_x + inward * 16, eye_bot + 4, outer_x, cy + 2)
        ctx.close_path()
        ctx.save()
        ctx.clip()
        g = cairo.LinearGradient(0, eye_top, 0, eye_bot)
        g.add_color_stop_rgba(0, 0.82, 0.83, 0.84, 1)
        g.add_color_stop_rgba(1, 0.97, 0.95, 0.94, 1)
        ctx.set_source(g)
        ctx.paint()
        # iris
        ix, iy = cx + inward * 1.5, cy + 2
        rg = cairo.RadialGradient(ix - 5, iy - 7, 2, ix, iy, iris_r + 3)
        r0, g0, b0 = rgb(pal["iris_light"])
        r1, g1, b1 = rgb(pal["iris_dark"])
        rg.add_color_stop_rgba(0, r0 / 255, g0 / 255, b0 / 255, 1)
        rg.add_color_stop_rgba(0.55, *(c / 255 for c in rgb(pal["iris"])), 1)
        rg.add_color_stop_rgba(1, r1 / 255, g1 / 255, b1 / 255, 1)
        ctx.set_source(rg)
        ctx.new_path()
        ctx.arc(ix, iy, iris_r, 0, 2 * math.pi)
        ctx.fill()
        # limbal ring
        ctx.new_path()
        ctx.arc(ix, iy, iris_r, 0, 2 * math.pi)
        C(ctx, pal["iris_dark"], 0.8)
        ctx.set_line_width(2.4)
        ctx.stroke()
        # pupil (slit for evil/entity)
        ctx.new_path()
        if expr == "evil" or entity:
            ctx.save()
            ctx.translate(ix, iy)
            ctx.scale(1, 2.3)
            ctx.arc(0, 0, pupil_r * 0.55, 0, 2 * math.pi)
            ctx.restore()
        else:
            ctx.arc(ix, iy, pupil_r, 0, 2 * math.pi)
        C(ctx, "#08070a")
        ctx.fill()
        # highlights
        ctx.new_path()
        ctx.arc(ix - 7, iy - 8, max(3.5, pupil_r * 0.62), 0, 2 * math.pi)
        C(ctx, "#ffffff", 0.9)
        ctx.fill()
        ctx.new_path()
        ctx.arc(ix + 8, iy + 7, max(2.0, pupil_r * 0.33), 0, 2 * math.pi)
        C(ctx, "#ffffff", 0.55)
        ctx.fill()
        # lower iris glow
        ctx.new_path()
        ctx.arc(ix, iy + iris_r * 0.45, iris_r * 0.5, 0.15, math.pi - 0.15)
        C(ctx, pal["iris_light"], 0.30)
        ctx.set_line_width(3)
        ctx.stroke()
        ctx.restore()

        # upper lash line
        ctx.new_path()
        ctx.move_to(outer_x - 2, cy + 1)
        ctx.curve_to(outer_x + inward * 12, eye_top - 2, cx + inward * 6, eye_top - 4, inner_x, cy - 2)
        C(ctx, pal["lash"])
        ctx.set_line_width(8.0)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()
        # lash flick
        ctx.new_path()
        if inward == 1:
            ctx.move_to(outer_x + 1, cy)
            ctx.line_to(outer_x - 16, cy - 11)
        else:
            ctx.move_to(outer_x - 1, cy)
            ctx.line_to(outer_x + 16, cy - 11)
        ctx.set_line_width(4.5)
        ctx.stroke()
        # lower lid
        ctx.new_path()
        ctx.move_to(outer_x + inward * 4, cy + 4)
        ctx.curve_to(outer_x + inward * 18, eye_bot + 3, cx + inward * 8, eye_bot + 2, inner_x, cy)
        C(ctx, pal["skin_shadow"] if not entity else pal["line"], 0.75)
        ctx.set_line_width(2.2)
        ctx.stroke()
        # eyelid crease
        ctx.new_path()
        ctx.move_to(outer_x + inward * 8, eye_top - 16)
        ctx.curve_to(cx, eye_top - 24, cx + inward * 22, eye_top - 20, inner_x + inward * 4, eye_top - 8)
        C(ctx, pal["skin_shadow"], 0.35)
        ctx.set_line_width(1.8)
        ctx.stroke()

        # eye shadow under for angry/shocked
        if expr in ("angry", "shocked", "scared"):
            ctx.new_path()
            ell(ctx, cx, cy, 52, 33, 0, 0, 2 * math.pi)
            C(ctx, "#5b3d4a", 0.10 if expr != "shocked" else 0.18)
            ctx.fill()

        # sweat drop
        if expr in ("scared", "surprised") and idx == 1:
            ctx.new_path()
            ctx.move_to(610, 390)
            ctx.curve_to(596, 414, 598, 432, 610, 432)
            ctx.curve_to(622, 432, 624, 414, 610, 390)
            C(ctx, "#bfe1ee", 0.82)
            ctx.fill()
            ctx.new_path()
            ctx.arc(607, 412, 3, 0, 2 * math.pi)
            C(ctx, "#ffffff", 0.8)
            ctx.fill()


def draw_brows(ctx, pal, expr):
    for idx, cx in enumerate((382, 518)):
        inward = 1 if idx == 0 else -1
        y = 372
        tilt = 0
        arch = -8
        thickness = 10
        if expr == "happy":
            arch = -14
        elif expr == "sad":
            y = 378
            tilt = -16 * inward
            arch = -4
        elif expr == "angry":
            y = 380
            tilt = 15 * inward
            arch = 3
            thickness = 12
        elif expr == "scared":
            y = 356
            arch = -16
        elif expr == "surprised":
            y = 350
            arch = -20
        elif expr == "evil":
            y = 382
            tilt = -8 * inward
            arch = 2
            thickness = 8
        elif expr == "shocked":
            y = 348
            arch = -22
        elif expr == "crying":
            y = 380
            tilt = -12 * inward
            arch = 0
        elif expr == "neutral":
            arch = -9

        outer = (cx - inward * 42, y + tilt * 0.2 - arch)
        inner = (cx + inward * 34, y - tilt * 0.5)
        ctrl = (cx - inward * 5, y - arch - 16)
        # tapered brow polygon
        ctx.new_path()
        ctx.move_to(outer[0], outer[1] - thickness * 0.45)
        ctx.curve_to(ctrl[0], ctrl[1] - thickness, inner[0], inner[1] - thickness * 0.2,
                     inner[0], inner[1] + thickness * 0.25)
        ctx.curve_to(ctrl[0], ctrl[1] + thickness * 0.55, outer[0], outer[1] + thickness * 0.55,
                     outer[0], outer[1] - thickness * 0.45)
        ctx.close_path()
        C(ctx, pal["brow"], 0.95)
        ctx.fill()


def draw_mouth(ctx, pal, expr, entity=False):
    mx, my = 450, 580
    if expr == "neutral":
        ctx.new_path()
        ctx.move_to(mx - 24, my)
        ctx.curve_to(mx - 8, my + 4, mx + 8, my + 4, mx + 24, my)
        C(ctx, pal["mouth"])
        ctx.set_line_width(3.4)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()
    elif expr == "happy":
        ctx.new_path()
        ctx.move_to(mx - 34, my - 4)
        ctx.curve_to(mx - 14, my + 26, mx + 14, my + 26, mx + 34, my - 4)
        ctx.curve_to(mx + 14, my + 12, mx - 14, my + 12, mx - 34, my - 4)
        ctx.close_path()
        C(ctx, pal["mouth_dark"])
        ctx.fill()
        ctx.new_path()
        ctx.move_to(mx - 30, my - 2)
        ctx.curve_to(mx - 12, my + 20, mx + 12, my + 20, mx + 30, my - 2)
        C(ctx, pal["mouth"])
        ctx.set_line_width(2.4)
        ctx.stroke()
        # blush
        for bx in (342, 558):
            ctx.new_path()
            ell(ctx, bx, 532, 44, 18, 0, 0, 2 * math.pi)
            grad(ctx, bx - 44, 532, bx + 44, 532, "#e88fa2", "#e88fa2", 0.26, 0.0)
            ctx.fill()
    elif expr == "sad":
        ctx.new_path()
        ctx.move_to(mx - 26, my + 8)
        ctx.curve_to(mx - 8, my - 4, mx + 8, my - 4, mx + 26, my + 8)
        C(ctx, pal["mouth"])
        ctx.set_line_width(3.2)
        ctx.stroke()
    elif expr == "angry":
        ctx.new_path()
        ctx.move_to(mx - 34, my - 6)
        ctx.curve_to(mx - 12, my + 21, mx + 12, my + 21, mx + 34, my - 6)
        ctx.curve_to(mx + 10, my + 6, mx - 10, my + 6, mx - 34, my - 6)
        ctx.close_path()
        C(ctx, pal["mouth_dark"])
        ctx.fill()
        # teeth
        ctx.new_path()
        ctx.move_to(mx - 28, my - 2)
        ctx.curve_to(mx - 10, my + 8, mx + 10, my + 8, mx + 28, my - 2)
        C(ctx, "#e8e0d2", 0.9)
        ctx.set_line_width(4.5)
        ctx.stroke()
        for tx in (-18, 0, 18):
            ctx.new_path()
            ctx.move_to(mx + tx, my + 1)
            ctx.line_to(mx + tx, my + 8)
            C(ctx, pal["mouth_dark"], 0.6)
            ctx.set_line_width(1.4)
            ctx.stroke()
    elif expr == "scared":
        ctx.new_path()
        ell(ctx, mx, my + 6, 18, 27, 0, 0, 2 * math.pi)
        C(ctx, pal["mouth_dark"])
        ctx.fill()
        ctx.new_path()
        ell(ctx, mx, my + 12, 11, 14, 0, 0, 2 * math.pi)
        C(ctx, "#b05a62", 0.8)
        ctx.fill()
    elif expr == "crying":
        ctx.new_path()
        ctx.move_to(mx - 28, my)
        ctx.curve_to(mx - 18, my + 46, mx + 18, my + 46, mx + 28, my)
        ctx.curve_to(mx + 14, my + 14, mx - 14, my + 14, mx - 28, my)
        ctx.close_path()
        C(ctx, pal["mouth_dark"])
        ctx.fill()
        ctx.new_path()
        ell(ctx, mx, my + 28, 14, 12, 0, 0, 2 * math.pi)
        C(ctx, "#b25f68", 0.85)
        ctx.fill()
    elif expr == "surprised":
        ctx.new_path()
        ell(ctx, mx, my + 6, 15, 22, 0, 0, 2 * math.pi)
        C(ctx, pal["mouth_dark"])
        ctx.fill()
    elif expr == "evil":
        ctx.new_path()
        ctx.move_to(mx - 48, my - 14)
        ctx.curve_to(mx - 22, my + 34, mx + 22, my + 34, mx + 48, my - 14)
        ctx.curve_to(mx + 20, my + 12, mx - 20, my + 12, mx - 48, my - 14)
        ctx.close_path()
        C(ctx, pal["mouth_dark"])
        ctx.fill()
        ctx.new_path()
        ctx.move_to(mx - 44, my - 11)
        ctx.curve_to(mx - 20, my + 25, mx + 20, my + 25, mx + 44, my - 11)
        C(ctx, "#e9e1d4", 0.9)
        ctx.set_line_width(3.4)
        ctx.stroke()
        if entity:
            for tx in (-30, -10, 10, 30):
                ctx.new_path()
                ctx.move_to(mx + tx, my + 2)
                ctx.line_to(mx + tx * 0.9, my + 22)
                C(ctx, pal["mouth_dark"], 0.8)
                ctx.set_line_width(2)
                ctx.stroke()
        # blush of a different kind
        for bx in (338, 562):
            ctx.new_path()
            ell(ctx, bx, 528, 38, 14, 0, 0, 2 * math.pi)
            C(ctx, "#8f2d3c", 0.20)
            ctx.fill()
    elif expr == "shocked":
        ctx.new_path()
        ell(ctx, mx, my + 10, 26, 38, 0, 0, 2 * math.pi)
        C(ctx, pal["mouth_dark"])
        ctx.fill()
        ctx.new_path()
        ell(ctx, mx, my + 18, 17, 22, 0, 0, 2 * math.pi)
        C(ctx, "#31181d", 0.9)
        ctx.fill()
    if entity and expr not in ("evil",):
        # black drool
        ctx.new_path()
        ctx.move_to(mx - 12, my + 10)
        ctx.curve_to(mx - 14, my + 40, mx - 8, my + 70, mx - 12, my + 90)
        C(ctx, "#050305", 0.55)
        ctx.set_line_width(3)
        ctx.stroke()


# ---------------------------------------------------------------------------
# HAIR
# ---------------------------------------------------------------------------
def hair_back(ctx, name, pal):
    if name in ("ethan", "dad"):
        ctx.new_path()
        ctx.move_to(450, 150)
        ctx.curve_to(330, 150, 286, 240, 286, 360)
        ctx.line_to(280, 470)
        ctx.line_to(308, 455)
        ctx.line_to(300, 520)
        ctx.line_to(330, 500)
        ctx.line_to(320, 560)
        ctx.line_to(365, 512)
        ctx.curve_to(370, 560, 380, 590, 400, 620)
        ctx.line_to(430, 560)
        ctx.line_to(450, 620)
        ctx.line_to(478, 556)
        ctx.line_to(506, 618)
        ctx.line_to(528, 550)
        ctx.line_to(562, 590)
        ctx.line_to(575, 520)
        ctx.line_to(612, 540)
        ctx.line_to(598, 470)
        ctx.line_to(622, 460)
        ctx.line_to(606, 360)
        ctx.curve_to(604, 240, 568, 150, 450, 150)
        ctx.close_path()
        grad(ctx, 320, 180, 600, 560, pal["hair_light"], pal["hair_dark"], 0.9, 1)
        fill_outline(ctx, outline=pal["line"], width=2.4)
    elif name in ("maya", "mom"):
        ctx.new_path()
        ctx.move_to(450, 165)
        ctx.curve_to(330, 165, 290, 250, 292, 380)
        ctx.curve_to(292, 470, 300, 560, 320, 640)
        ctx.curve_to(340, 690, 380, 700, 420, 680)
        ctx.curve_to(430, 640, 430, 600, 425, 560)
        ctx.curve_to(470, 595, 520, 600, 560, 650)
        ctx.curve_to(610, 690, 645, 640, 632, 570)
        ctx.curve_to(620, 500, 612, 440, 608, 380)
        ctx.curve_to(606, 250, 570, 165, 450, 165)
        ctx.close_path()
        grad(ctx, 310, 180, 620, 680, pal["hair_light"], pal["hair_dark"], 0.95, 1)
        fill_outline(ctx, outline=pal["line"], width=2.4)
    elif name == "girl":
        ctx.new_path()
        ctx.move_to(450, 150)
        ctx.curve_to(320, 150, 270, 245, 272, 380)
        ctx.curve_to(272, 520, 240, 720, 236, 980)
        ctx.line_to(276, 950)
        ctx.line_to(290, 1180)
        ctx.line_to(332, 1080)
        ctx.line_to(350, 1280)
        ctx.line_to(398, 1120)
        ctx.line_to(430, 1350)
        ctx.line_to(470, 1120)
        ctx.line_to(520, 1330)
        ctx.line_to(552, 1110)
        ctx.line_to(594, 1250)
        ctx.line_to(610, 1040)
        ctx.line_to(648, 1140)
        ctx.line_to(642, 900)
        ctx.curve_to(638, 680, 620, 480, 626, 380)
        ctx.curve_to(628, 245, 580, 150, 450, 150)
        ctx.close_path()
        g = cairo.LinearGradient(300, 180, 600, 1300)
        g.add_color_stop_rgba(0, *[c / 255 for c in rgb(pal["hair_light"])], 0.96)
        g.add_color_stop_rgba(0.5, *[c / 255 for c in rgb(pal["hair"])], 0.92)
        g.add_color_stop_rgba(1, *[c / 255 for c in rgb(pal["hair_dark"])], 0.55)
        ctx.set_source(g)
        ctx.fill_preserve()
        C(ctx, pal["line"], 0.55)
        ctx.set_line_width(2.0)
        ctx.stroke()
    elif name == "entity":
        ctx.new_path()
        ctx.move_to(450, 130)
        ctx.curve_to(330, 130, 280, 220, 278, 360)
        ctx.curve_to(276, 560, 230, 800, 200, 1080)
        ctx.line_to(250, 1020)
        ctx.line_to(260, 1200)
        ctx.line_to(320, 1050)
        ctx.line_to(340, 1340)
        ctx.line_to(400, 1080)
        ctx.line_to(430, 1400)
        ctx.line_to(480, 1070)
        ctx.line_to(520, 1380)
        ctx.line_to(560, 1080)
        ctx.line_to(600, 1300)
        ctx.line_to(630, 1030)
        ctx.line_to(680, 1160)
        ctx.line_to(650, 890)
        ctx.curve_to(630, 620, 624, 470, 626, 360)
        ctx.curve_to(624, 220, 574, 130, 450, 130)
        ctx.close_path()
        C(ctx, pal["hair"], 0.98)
        fill_outline(ctx, outline="#000000", width=2.0)


def hair_front(ctx, name, pal, expr):
    if name in ("ethan", "dad"):
        # bangs
        locks = [
            [(450, 176), (392, 182), (330, 250), (318, 354), (356, 320), (380, 376), (410, 300), (432, 360), (450, 280)],
            [(450, 176), (510, 180), (566, 250), (584, 356), (548, 318), (526, 378), (500, 296), (476, 362), (456, 282)],
            [(438, 172), (396, 188), (368, 220), (356, 286), (386, 262), (400, 312), (420, 244), (438, 290), (446, 236)],
        ]
        for lock in locks:
            ctx.new_path()
            ctx.move_to(*lock[0])
            for p in lock[1:]:
                ctx.line_to(*p)
            ctx.close_path()
            grad(ctx, 340, 170, 560, 380, pal["hair"], pal["hair_dark"], 1, 1)
            fill_outline(ctx, outline=pal["line"], width=2.0)
        # side locks
        for sx, sy, ex, ey in [(312, 330, 300, 500), (590, 330, 604, 500)]:
            ctx.new_path()
            ctx.move_to(sx, sy)
            ctx.curve_to(sx - 16, sy + 60, ex - 6, ey - 40, ex, ey)
            ctx.line_to(ex + 18, ey - 24)
            ctx.curve_to(ex + 10, sy + 80, sx + 20, sy + 40, sx, sy)
            ctx.close_path()
            C(ctx, pal["hair"], 1)
            fill_outline(ctx, outline=pal["line"], width=1.8)
        # highlights
        for x0, y0, x1, y1, x2, y2 in [(365, 210, 350, 280, 335, 320), (530, 205, 548, 280, 560, 320), (420, 196, 412, 250, 400, 290)]:
            ctx.new_path()
            ctx.move_to(x0, y0)
            quad(ctx, x0, y0, (x0 + x1) / 2, y0 + 20, x1, y1)
            ctx.line_to(x2, y2)
            C(ctx, pal["hair_light"], 0.55)
            ctx.set_line_width(5)
            ctx.set_line_cap(cairo.LINE_CAP_ROUND)
            ctx.stroke()
    elif name in ("maya", "mom"):
        # fringe
        ctx.new_path()
        ctx.move_to(304, 356)
        ctx.curve_to(320, 250, 380, 200, 450, 200)
        ctx.curve_to(520, 200, 580, 250, 596, 356)
        ctx.curve_to(566, 300, 536, 270, 510, 342)
        ctx.curve_to(492, 280, 470, 258, 452, 330)
        ctx.curve_to(432, 270, 408, 262, 390, 340)
        ctx.curve_to(376, 292, 348, 286, 330, 356)
        ctx.close_path()
        grad(ctx, 320, 200, 600, 360, pal["hair"], pal["hair_dark"], 1, 1)
        fill_outline(ctx, outline=pal["line"], width=2.0)
        # side locks curl inward
        for sx, flip in [(304, -1), (596, 1)]:
            ctx.new_path()
            ctx.move_to(sx, 320)
            ctx.curve_to(sx + flip * 18, 440, sx + flip * 10, 570, sx + flip * 44, 650)
            ctx.curve_to(sx + flip * 70, 620, sx + flip * 52, 560, sx + flip * 38, 500)
            ctx.curve_to(sx + flip * 24, 430, sx + flip * 10, 370, sx, 320)
            ctx.close_path()
            fill_outline(ctx, fill=pal["hair"], outline=pal["line"], width=1.8)
        # hair clip
        ctx.new_path()
        ctx.move_to(520, 300)
        ctx.line_to(562, 288)
        ctx.line_to(570, 306)
        ctx.line_to(528, 318)
        ctx.close_path()
        C(ctx, pal["accent"], 1)
        ctx.fill_preserve()
        C(ctx, "#e9d8b0", 0.9)
        ctx.set_line_width(1.4)
        ctx.stroke()
        # highlight sheen
        ctx.new_path()
        ctx.move_to(336, 262)
        ctx.curve_to(380, 224, 430, 216, 480, 222)
        C(ctx, pal["hair_light"], 0.45)
        ctx.set_line_width(10)
        ctx.stroke()
    elif name == "girl":
        # blunt fringe with parted strands
        ctx.new_path()
        ctx.move_to(306, 330)
        ctx.curve_to(322, 240, 380, 195, 450, 195)
        ctx.curve_to(520, 195, 578, 240, 594, 330)
        ctx.curve_to(570, 306, 544, 300, 520, 372)
        ctx.line_to(508, 300)
        ctx.curve_to(492, 350, 480, 350, 468, 292)
        ctx.line_to(456, 362)
        ctx.curve_to(444, 296, 432, 300, 420, 360)
        ctx.line_to(408, 294)
        ctx.curve_to(392, 340, 382, 344, 372, 300)
        ctx.line_to(356, 372)
        ctx.curve_to(340, 310, 326, 306, 306, 330)
        ctx.close_path()
        C(ctx, pal["hair"], 0.96)
        fill_outline(ctx, outline=pal["line"], width=2.0)
        # long side locks framing face
        for sx, flip in [(306, -1), (594, 1)]:
            ctx.new_path()
            ctx.move_to(sx, 300)
            ctx.curve_to(sx + flip * 24, 440, sx + flip * 18, 640, sx + flip * 30, 820)
            ctx.line_to(sx + flip * 58, 760)
            ctx.curve_to(sx + flip * 54, 600, sx + flip * 50, 420, sx + flip * 2, 300)
            ctx.close_path()
            g = cairo.LinearGradient(sx, 300, sx, 800)
            g.add_color_stop_rgba(0, *[c / 255 for c in rgb(pal["hair_light"])], 0.9)
            g.add_color_stop_rgba(1, *[c / 255 for c in rgb(pal["hair_dark"])], 0.55)
            ctx.set_source(g)
            ctx.fill_preserve()
            C(ctx, pal["line"], 0.6)
            ctx.set_line_width(1.8)
            ctx.stroke()
        # sheen
        ctx.new_path()
        ctx.move_to(340, 250)
        ctx.curve_to(390, 214, 460, 206, 520, 218)
        C(ctx, pal["hair_light"], 0.65)
        ctx.set_line_width(12)
        ctx.stroke()
        # thin shadow veil over eyes (mysterious)
        if expr in ("neutral", "sad"):
            ctx.new_path()
            ctx.rectangle(315, 400, 270, 110)
            C(ctx, "#5a5668", 0.10)
            ctx.fill()
    elif name == "entity":
        # stringy fringe strands
        strands = [
            [(450, 150), (350, 170), (300, 300), (310, 520), (326, 420), (344, 550), (360, 400), (382, 500), (400, 340), (420, 470), (438, 280)],
            [(450, 150), (550, 170), (600, 300), (590, 520), (574, 420), (556, 550), (540, 400), (518, 500), (500, 340), (480, 470), (462, 280)],
        ]
        for pts in strands:
            ctx.new_path()
            ctx.move_to(*pts[0])
            for p in pts[1:]:
                ctx.line_to(*p)
            ctx.close_path()
            C(ctx, pal["hair"], 0.95)
            fill_outline(ctx, outline="#000000", width=1.4)
        # tendrils rising
        for i in range(8):
            x = 250 + i * 58
            ctx.new_path()
            ctx.move_to(x, 210)
            ctx.curve_to(x - 30, 120, x + 20, 60, x - 10, 10)
            C(ctx, "#000000", 0.8)
            ctx.set_line_width(3.5)
            ctx.stroke()


# ---------------------------------------------------------------------------
# OUTFITS
# ---------------------------------------------------------------------------
def body_hoodie(ctx, pal):
    # hood behind neck
    ctx.new_path()
    ctx.move_to(340, 660)
    ctx.curve_to(300, 700, 286, 760, 300, 820)
    ctx.curve_to(330, 860, 390, 870, 430, 860)
    ctx.line_to(450, 790)
    ctx.line_to(470, 860)
    ctx.curve_to(520, 870, 580, 850, 606, 812)
    ctx.curve_to(616, 750, 600, 700, 560, 660)
    ctx.close_path()
    grad(ctx, 340, 660, 560, 870, pal["outfit_light"], pal["outfit_dark"], 1, 1)
    fill_outline(ctx, outline=pal["line"], width=2.6)

    # torso
    ctx.new_path()
    ctx.move_to(394, 700)
    ctx.curve_to(330, 716, 284, 770, 264, 850)
    ctx.curve_to(238, 1000, 220, 1280, 208, 1500)
    ctx.line_to(692, 1500)
    ctx.curve_to(680, 1280, 662, 1000, 636, 850)
    ctx.curve_to(616, 770, 570, 716, 506, 700)
    ctx.close_path()
    grad(ctx, 300, 720, 620, 1480, pal["outfit"], pal["outfit_dark"], 1, 1)
    fill_outline(ctx, outline=pal["line"], width=2.8)

    # shirt at collar
    ctx.new_path()
    ctx.move_to(404, 700)
    ctx.curve_to(430, 760, 470, 760, 496, 700)
    ctx.curve_to(470, 790, 430, 790, 404, 700)
    ctx.close_path()
    grad(ctx, 450, 690, 450, 790, pal["shirt"], mix(pal["shirt"], "#8b8578", 0.5), 1, 1)
    ctx.fill()

    # hoodie opening / zipper
    ctx.new_path()
    ctx.move_to(450, 740)
    ctx.line_to(450, 1500)
    C(ctx, pal["outfit_dark"], 0.9)
    ctx.set_line_width(3)
    ctx.stroke()
    ctx.new_path()
    for y in range(760, 1490, 26):
        ctx.move_to(444, y)
        ctx.line_to(456, y)
    C(ctx, "#7a8394", 0.35)
    ctx.set_line_width(1.4)
    ctx.stroke()
    # zipper pull
    ctx.new_path()
    rr(ctx, 440, 900, 14, 28, 5)
    C(ctx, "#9aa3b3", 0.9)
    ctx.fill()
    # drawstrings
    for sx, ex in [(420, 400), (480, 500)]:
        ctx.new_path()
        ctx.move_to(sx, 740)
        ctx.curve_to(sx, 800, ex, 850, ex, 900)
        C(ctx, "#cfc8b8", 0.9)
        ctx.set_line_width(5)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()
        ctx.new_path()
        rr(ctx, ex - 6, 896, 12, 26, 5)
        C(ctx, "#8b8578", 1)
        ctx.fill()
    # sleeves / seam shadows
    ctx.new_path()
    ctx.move_to(300, 840)
    ctx.curve_to(280, 1010, 258, 1250, 248, 1460)
    C(ctx, pal["outfit_dark"], 0.45)
    ctx.set_line_width(16)
    ctx.stroke()
    ctx.new_path()
    ctx.move_to(600, 840)
    ctx.curve_to(620, 1010, 640, 1250, 650, 1460)
    C(ctx, pal["outfit_dark"], 0.35)
    ctx.set_line_width(16)
    ctx.stroke()
    # pocket
    ctx.new_path()
    ctx.move_to(352, 1150)
    ctx.curve_to(420, 1180, 480, 1180, 548, 1150)
    ctx.line_to(548, 1280)
    ctx.curve_to(480, 1310, 420, 1310, 352, 1280)
    ctx.close_path()
    C(ctx, pal["outfit_dark"], 0.45)
    ctx.fill_preserve()
    C(ctx, pal["line"], 0.5)
    ctx.set_line_width(2)
    ctx.stroke()


def body_maya(ctx, pal):
    # torso / blouse
    ctx.new_path()
    ctx.move_to(400, 690)
    ctx.curve_to(340, 706, 294, 758, 276, 840)
    ctx.curve_to(252, 1010, 238, 1260, 230, 1500)
    ctx.line_to(670, 1500)
    ctx.curve_to(662, 1260, 648, 1010, 624, 840)
    ctx.curve_to(606, 758, 560, 706, 500, 690)
    ctx.close_path()
    grad(ctx, 310, 700, 620, 1480, pal["shirt"], mix(pal["shirt"], "#a89c86", 0.6), 1, 1)
    fill_outline(ctx, outline=pal["line"], width=2.6)

    # cardigan panels
    for pts, flip in [([(300, 820), (330, 800), (390, 860), (360, 1500), (250, 1500), (268, 1000)], -1),
                      ([(600, 820), (570, 800), (510, 860), (540, 1500), (650, 1500), (632, 1000)], 1)]:
        ctx.new_path()
        ctx.move_to(*pts[0])
        for p in pts[1:]:
            ctx.line_to(*p)
        ctx.close_path()
        grad(ctx, 300, 820, 620, 1480, pal["outfit"], pal["outfit_dark"], 1, 1)
        fill_outline(ctx, outline=pal["line"], width=2.2)
    # cardigan edges
    for x in (388, 512):
        ctx.new_path()
        ctx.move_to(x, 862)
        ctx.line_to(x - (12 if x < 450 else -12), 1500)
        C(ctx, pal["outfit_light"], 0.8)
        ctx.set_line_width(5)
        ctx.stroke()
    # buttons
    for y in (980, 1080, 1180):
        ctx.new_path()
        ctx.arc(512, y, 7, 0, 2 * math.pi)
        C(ctx, "#e4d6ae", 1)
        ctx.fill_preserve()
        C(ctx, pal["outfit_dark"], 0.8)
        ctx.set_line_width(1.4)
        ctx.stroke()

    # scarf
    ctx.new_path()
    ctx.move_to(360, 700)
    ctx.curve_to(390, 760, 512, 770, 546, 700)
    ctx.curve_to(590, 720, 586, 790, 540, 820)
    ctx.curve_to(500, 850, 402, 850, 362, 818)
    ctx.curve_to(318, 786, 320, 724, 360, 700)
    ctx.close_path()
    grad(ctx, 350, 700, 550, 850, pal["accent"], mix(pal["accent"], "#0b1d1d", 0.55), 1, 1)
    fill_outline(ctx, outline=pal["line"], width=2.4)
    # scarf tail
    ctx.new_path()
    ctx.move_to(500, 805)
    ctx.curve_to(540, 880, 560, 960, 548, 1040)
    ctx.line_to(494, 1020)
    ctx.curve_to(500, 930, 480, 860, 466, 815)
    ctx.close_path()
    fill_outline(ctx, fill=pal["accent"], outline=pal["line"], width=2.0)
    # scarf knit lines
    ctx.new_path()
    for y in range(720, 830, 14):
        ctx.move_to(370, y)
        ctx.curve_to(430, y + 22, 490, y + 22, 540, y - 2)
    C(ctx, "#a9d6d0", 0.25)
    ctx.set_line_width(2)
    ctx.stroke()
    # necklace
    ctx.new_path()
    ctx.arc(450, 820, 34, 0.2, math.pi - 0.2)
    C(ctx, "#d6c28a", 0.9)
    ctx.set_line_width(2)
    ctx.stroke()
    ctx.new_path()
    ctx.arc(450, 854, 6, 0, 2 * math.pi)
    C(ctx, "#d6c28a", 1)
    ctx.fill()


def body_dad(ctx, pal):
    # A quiet collared shirt beneath a weathered jacket, distinct from Ethan's
    # hoodie while keeping the same full-body silhouette and line weight.
    ctx.new_path()
    ctx.move_to(398, 700)
    ctx.curve_to(340, 718, 292, 776, 270, 864)
    ctx.curve_to(246, 1030, 232, 1270, 226, 1500)
    ctx.line_to(674, 1500)
    ctx.curve_to(668, 1270, 654, 1030, 630, 864)
    ctx.curve_to(608, 776, 560, 718, 502, 700)
    ctx.close_path()
    grad(ctx, 300, 700, 620, 1480, pal["outfit"], pal["outfit_dark"], 1, 1)
    fill_outline(ctx, outline=pal["line"], width=2.8)

    ctx.new_path()
    ctx.move_to(405, 700)
    ctx.line_to(450, 748)
    ctx.line_to(495, 700)
    ctx.line_to(486, 1500)
    ctx.line_to(414, 1500)
    ctx.close_path()
    grad(ctx, 450, 720, 450, 1490, pal["shirt"], mix(pal["shirt"], "#847c72", 0.5), 1, 1)
    fill_outline(ctx, outline=pal["line"], width=2.0)

    for pts in (
        [(395, 706), (450, 760), (422, 920), (348, 792)],
        [(505, 706), (450, 760), (478, 920), (552, 792)],
    ):
        ctx.new_path()
        ctx.move_to(*pts[0])
        for point in pts[1:]:
            ctx.line_to(*point)
        ctx.close_path()
        C(ctx, pal["outfit_light"], 0.95)
        fill_outline(ctx, outline=pal["line"], width=2.2)

    ctx.new_path()
    ctx.move_to(440, 775)
    ctx.line_to(460, 775)
    ctx.line_to(468, 1040)
    ctx.line_to(450, 1070)
    ctx.line_to(432, 1040)
    ctx.close_path()
    grad(ctx, 450, 775, 450, 1070, pal["accent"], mix(pal["accent"], "#171317", 0.6), 1, 1)
    fill_outline(ctx, outline=pal["line"], width=1.8)

    for y in (1100, 1200, 1300):
        ctx.new_path()
        ctx.arc(528, y, 6, 0, 2 * math.pi)
        C(ctx, "#b3a382", 0.9)
        ctx.fill()


def body_girl(ctx, pal):
    # dress torso
    ctx.new_path()
    ctx.move_to(402, 690)
    ctx.curve_to(340, 704, 298, 752, 282, 830)
    ctx.curve_to(262, 1000, 252, 1280, 246, 1500)
    ctx.line_to(654, 1500)
    ctx.curve_to(648, 1280, 638, 1000, 618, 830)
    ctx.curve_to(602, 752, 560, 704, 498, 690)
    ctx.close_path()
    grad(ctx, 300, 700, 620, 1480, pal["outfit_light"], pal["outfit_dark"], 1, 1)
    fill_outline(ctx, outline=pal["line"], width=2.4)

    # collar
    ctx.new_path()
    ctx.move_to(386, 706)
    ctx.curve_to(420, 760, 480, 760, 514, 706)
    ctx.curve_to(500, 790, 400, 790, 386, 706)
    ctx.close_path()
    C(ctx, pal["outfit_light"], 1)
    fill_outline(ctx, outline=pal["line"], width=1.8)

    # ribbon
    ctx.new_path()
    ctx.move_to(450, 760)
    ctx.curve_to(414, 738, 390, 754, 402, 790)
    ctx.curve_to(414, 812, 438, 798, 450, 780)
    ctx.curve_to(462, 798, 486, 812, 498, 790)
    ctx.curve_to(510, 754, 486, 738, 450, 760)
    ctx.close_path()
    C(ctx, pal["accent"], 1)
    fill_outline(ctx, outline=pal["line"], width=1.6)
    ctx.new_path()
    ctx.move_to(444, 772)
    ctx.line_to(440, 830)
    ctx.line_to(458, 830)
    ctx.line_to(456, 772)
    ctx.close_path()
    C(ctx, pal["accent"], 0.95)
    ctx.fill()

    # long sleeves with tattered cuffs
    for sx, ex, flip in [(290, 236, -1), (610, 664, 1)]:
        ctx.new_path()
        ctx.move_to(sx, 820)
        ctx.curve_to(sx + flip * 14, 980, ex + flip * 8, 1200, ex, 1360)
        ctx.line_to(ex + flip * 46, 1350)
        ctx.curve_to(ex + flip * 54, 1180, sx + flip * 52, 960, sx + flip * 30, 826)
        ctx.close_path()
        fill_outline(ctx, fill=pal["outfit"], outline=pal["line"], width=2.0)
    # ghostly trim / embroidery
    ctx.new_path()
    ctx.move_to(340, 900)
    ctx.curve_to(360, 1100, 352, 1300, 330, 1460)
    C(ctx, "#ffffff", 0.16)
    ctx.set_line_width(10)
    ctx.stroke()
    # shadow folds
    for x in (360, 450, 540):
        ctx.new_path()
        ctx.move_to(x, 1000)
        ctx.curve_to(x + 10, 1160, x - 8, 1320, x + 4, 1490)
        C(ctx, pal["outfit_dark"], 0.22)
        ctx.set_line_width(10)
        ctx.stroke()


def body_entity(ctx, pal):
    # robe / elongated torso
    ctx.new_path()
    ctx.move_to(400, 660)
    ctx.curve_to(320, 690, 260, 750, 236, 850)
    ctx.curve_to(200, 1080, 188, 1300, 172, 1500)
    ctx.line_to(728, 1500)
    ctx.curve_to(712, 1300, 700, 1080, 664, 850)
    ctx.curve_to(640, 750, 580, 690, 500, 660)
    ctx.close_path()
    grad(ctx, 300, 680, 620, 1480, pal["outfit"], pal["outfit_dark"], 1, 1)
    fill_outline(ctx, outline="#000000", width=2.6)
    # inner void
    ctx.new_path()
    ctx.move_to(380, 760)
    ctx.curve_to(420, 820, 480, 820, 520, 760)
    ctx.curve_to(500, 900, 400, 900, 380, 760)
    ctx.close_path()
    C(ctx, "#000000", 0.8)
    ctx.fill()
    # tendrils from shoulders
    for i, (x, y, dx, dy, ex, ey) in enumerate([
        (250, 900, 140, 980, 80, 1160), (650, 900, 760, 980, 830, 1140),
        (230, 1100, 120, 1190, 190, 1380), (670, 1100, 790, 1180, 720, 1380),
        (300, 800, 220, 830, 170, 960), (600, 800, 690, 830, 750, 960),
    ]):
        ctx.new_path()
        ctx.move_to(x, y)
        ctx.curve_to(dx, dy, ex, ey, ex + (12 if i % 2 else -12), ey + 40)
        C(ctx, "#050407", 0.9)
        ctx.set_line_width(10 - i)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.stroke()
    # long fingers at bottom edge
    for fx in (300, 380, 460, 540, 620):
        ctx.new_path()
        ctx.move_to(fx, 1430)
        ctx.curve_to(fx - 6, 1470, fx + 4, 1490, fx - 2, 1500)
        C(ctx, "#0a0810", 0.8)
        ctx.set_line_width(8)
        ctx.stroke()


def draw_body(ctx, name, pal):
    if name == "ethan":
        body_hoodie(ctx, pal)
    elif name == "dad":
        body_dad(ctx, pal)
    elif name in ("maya", "mom"):
        body_maya(ctx, pal)
    elif name == "girl":
        body_girl(ctx, pal)
    else:
        body_entity(ctx, pal)


def draw_character(name, expr, size=(900, 1500)):
    pal = PALETTES[name]
    entity = name == "entity"
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W * S, H * S)
    ctx = cairo.Context(surf)
    ctx.set_antialias(cairo.ANTIALIAS_BEST)
    ctx.scale(S, S)

    # back hair
    hair_back(ctx, name, pal)
    # neck and body
    draw_neck(ctx, pal, entity)
    draw_body(ctx, name, pal)
    # face
    draw_face(ctx, pal, expr, entity)
    # facial features
    draw_eyes(ctx, pal, expr, entity)
    draw_brows(ctx, pal, expr)
    draw_mouth(ctx, pal, expr, entity)
    if name in ("mom", "dad"):
        # Fine crow's feet and smile lines establish adult faces without
        # breaking the clean anime linework used for the younger cast.
        C(ctx, pal["skin_shadow"], 0.64)
        ctx.set_line_width(2.2)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        for side in (-1, 1):
            ctx.new_path()
            ctx.move_to(382 + side * 42, 490)
            ctx.curve_to(382 + side * 51, 496, 382 + side * 54, 504, 382 + side * 57, 510)
            ctx.stroke()
            ctx.new_path()
            ctx.move_to(518 + side * 42, 490)
            ctx.curve_to(518 + side * 51, 496, 518 + side * 54, 504, 518 + side * 57, 510)
            ctx.stroke()
        for y in (333, 342):
            ctx.new_path()
            ctx.move_to(408, y)
            ctx.curve_to(435, y + 5, 465, y + 5, 492, y)
            ctx.stroke()
    # front hair
    hair_front(ctx, name, pal, expr)

    # rim light from right, cel highlight
    light = cairo.LinearGradient(580, 300, 760, 500)
    light.add_color_stop_rgba(0, 0, 0, 0, 0)
    light.add_color_stop_rgba(1, 0.72, 0.80, 0.95, 0.0)
    ctx.set_source(light)
    ctx.paint()

    surf.write_to_png("/tmp/_sprite.png")
    im = Image.open("/tmp/_sprite.png").convert("RGBA").resize(size, Image.LANCZOS)

    # soft rim glow on the right edge using alpha edge detection
    alpha = im.getchannel("A")
    edge = alpha.filter(ImageFilter.GaussianBlur(5))
    edge = ImageChops.subtract(edge, alpha.filter(ImageFilter.MinFilter(5)))
    edge = edge.filter(ImageFilter.GaussianBlur(6))
    rim = Image.new("RGBA", im.size, (116, 138, 180, 0))
    rim.putalpha(edge.point(lambda v: int(v * 0.55)))
    im = Image.alpha_composite(im, rim)

    # supernatural eye glow for the entity
    if entity:
        from art_common import radial_glow
        glows = Image.new("RGBA", im.size, (0, 0, 0, 0))
        for ex in (382, 518):
            g = radial_glow(im.size, (ex, 456), 120, (235, 232, 218), 62, 2.2)
            glows = Image.alpha_composite(glows, g)
        im = Image.alpha_composite(im, glows)

    # subtle lower-body fade into darkness (helps blends into scene)
    arr = np.linspace(0, 255, im.size[1], dtype=np.float32)[:, None]
    arr = np.clip((arr - 1380) / 120, 0, 1) * 255
    fade_arr = np.repeat(arr, im.size[0], axis=1).astype(np.uint8)
    fade = Image.fromarray(fade_arr, "L")
    dark = Image.new("RGBA", im.size, (5, 5, 8, 255))
    im = Image.composite(dark, im, fade.point(lambda v: int(v * 0.75)))
    return im


def build_all():
    outdir = out("characters")
    for name in PALETTES:
        for expr in EXPRESSIONS:
            im = draw_character(name, expr)
            path = os.path.join(outdir, f"{name}_{expr}.png")
            im.save(path, optimize=True)
            print("wrote", path, im.size)


if __name__ == "__main__":
    build_all()
