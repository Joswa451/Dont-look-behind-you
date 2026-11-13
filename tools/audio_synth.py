"""Original procedural music and sound design for DON'T LOOK BEHIND YOU.

Everything is synthesized from oscillators and noise. No external samples.
Tracks are written as mono/stereo float arrays, then encoded to OGG with
ffmpeg so Ren'Py can stream them.
"""
from __future__ import annotations

import math
import os
import random
import subprocess
import wave

import numpy as np

SR = 44100
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUS = os.path.join(ROOT, "game", "audio", "music")
SFX = os.path.join(ROOT, "game", "audio", "sfx")
os.makedirs(MUS, exist_ok=True)
os.makedirs(SFX, exist_ok=True)

rng = np.random.default_rng(7)


def midi(n):
    return 440.0 * (2 ** ((n - 69) / 12))


def time(dur):
    return np.arange(int(dur * SR), dtype=np.float64) / SR


def fade(x, fi=0.02, fo=0.05):
    n = len(x)
    a = int(min(fi * SR, n // 2))
    b = int(min(fo * SR, n // 2))
    if a:
        x[:a] *= np.linspace(0, 1, a)
    if b:
        x[-b:] *= np.linspace(1, 0, b)
    return x


def normalize(x, peak=0.9):
    m = np.max(np.abs(x)) + 1e-9
    return x / m * peak


def stereo(left, right):
    return np.stack([left, right], axis=1)


def place(buf, sig, start, pan=0.0, gain=1.0):
    i = int(start * SR)
    if i >= len(buf):
        return
    n = min(len(sig), len(buf) - i)
    if n <= 0:
        return
    ang = (pan + 1) * math.pi / 4
    buf[i:i + n, 0] += sig[:n] * gain * math.cos(ang)
    buf[i:i + n, 1] += sig[:n] * gain * math.sin(ang)


def fft_filter(x, low=None, high=None, order=2):
    n = len(x)
    if n == 0:
        return x
    nfft = 1 << (n - 1).bit_length()
    X = np.fft.rfft(x, nfft)
    f = np.fft.rfftfreq(nfft, 1 / SR)
    H = np.ones_like(f)
    if low:
        H *= 1 / (1 + (f / low) ** order)
    if high:
        H *= (f / high) ** order / (1 + (f / high) ** order)
    return np.fft.irfft(X * H, nfft)[:n]


def fft_convolve(x, ir):
    n = len(x) + len(ir) - 1
    nfft = 1 << (n - 1).bit_length()
    y = np.fft.irfft(np.fft.rfft(x, nfft) * np.fft.rfft(ir, nfft), nfft)
    return y[:len(x)]


def make_ir(dur=2.0, decay=3.2, seed=1, bright=0.7):
    r = np.random.default_rng(seed)
    t = time(dur)
    ir = r.normal(0, 1, len(t)) * np.exp(-decay * t)
    ir = fft_filter(ir, low=5000 * bright)
    ir[:int(0.008 * SR)] = 0
    return normalize(ir, 1.0)


def reverb(buf, amount=0.25, dur=2.2, decay=3.0, seed=3):
    out = buf.copy()
    for c in range(2):
        ir = make_ir(dur, decay, seed + c * 3)
        wet = fft_convolve(buf[:, c], ir)
        out[:, c] = buf[:, c] * (1 - amount * 0.35) + wet * amount
    return out


def noise(n, seed=0):
    return np.random.default_rng(seed).normal(0, 1, n)


def piano(freq, dur, amp=0.5, bright=1.0, detune=0.0):
    n = int(dur * SR)
    if n <= 2:
        return np.zeros(2)
    t = np.arange(n) / SR
    f0 = freq * (1 + detune)
    env = (1 - np.exp(-t / 0.006)) * np.exp(-t / (0.55 + dur * 0.35))
    sig = np.zeros(n)
    phase = np.random.uniform(0, 2 * math.pi, 10)
    for k in range(1, 10):
        f = f0 * k * (1 + 0.00038 * k * k)
        if f > SR * 0.46:
            break
        a = (1 / k ** 1.65) * np.exp(-t * (0.9 + k * 0.85))
        sig += a * np.sin(2 * math.pi * f * t + phase[k - 1])
    sig += 0.12 * fft_filter(noise(n, int(freq)), low=3800, high=500) * np.exp(-t / 0.012)
    sig *= env
    return sig * amp * bright


def bell(freq, dur, amp=0.4):
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = np.zeros(n)
    for ratio, decay, a in [(1, 2.1, 1.0), (2.01, 3.0, 0.55), (3.02, 4.2, 0.3), (4.18, 5.5, 0.16), (5.42, 7.0, 0.08)]:
        sig += a * np.sin(2 * math.pi * freq * ratio * t) * np.exp(-t * decay)
    sig *= (1 - np.exp(-t / 0.002))
    return sig * amp


def pad_chord(midis, dur, amp=0.25, cutoff=900, detune=0.004, seed=0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = np.zeros(n)
    for i, m in enumerate(midis):
        f = midi(m)
        for d in (-detune, 0, detune):
            ff = f * (1 + d)
            for k in range(1, 9):
                if ff * k > SR * 0.45:
                    break
                sig += (amp / (len(midis) * 3 * k)) * np.sin(2 * math.pi * ff * k * t + 0.6 * i + k * 0.2 + seed)
    sig = fft_filter(sig, low=cutoff)
    env = np.minimum(1, t / (dur * 0.28)) * np.minimum(1, (dur - t) / (dur * 0.3))
    lfo = 0.88 + 0.12 * np.sin(2 * math.pi * 0.06 * t + seed)
    return sig * env * lfo


def drone(freq, dur, amp=0.3, cutoff=400, seed=0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = np.zeros(n)
    for d in (-0.003, 0, 0.0035):
        for k in (1, 2, 3, 5):
            sig += (1 / k) * np.sin(2 * math.pi * freq * k * (1 + d) * t + seed + k)
    sig = fft_filter(sig, low=cutoff)
    env = np.minimum(1, t / 2.0) * np.minimum(1, (dur - t) / 2.0)
    return sig * amp * env


def low_thump(dur=0.5, freq=55, amp=0.7):
    n = int(dur * SR)
    t = np.arange(n) / SR
    env = np.exp(-t / 0.13)
    sig = np.sin(2 * math.pi * freq * t) * env
    sig += 0.25 * fft_filter(noise(n, 5), low=220) * np.exp(-t / 0.04)
    return sig * amp


def tick(amp=0.4):
    n = int(0.08 * SR)
    t = np.arange(n) / SR
    sig = np.sin(2 * math.pi * 1800 * t) * np.exp(-t / 0.006)
    sig += 0.5 * noise(n, 9) * np.exp(-t / 0.004)
    return sig * amp


def heartbeat(bpm=58, dur=6.0, amp=0.7):
    n = int(dur * SR)
    out = np.zeros(n)
    beat = 60 / bpm
    t0 = 0.15
    while t0 < dur - 0.5:
        for off, a in ((0, 1.0), (0.14, 0.62)):
            th = low_thump(0.45, 48, amp * a)
            i = int((t0 + off) * SR)
            k = min(len(th), n - i)
            out[i:i + k] += th[:k]
        t0 += beat
    return out


def riser(dur=3.0, amp=0.35, seed=2):
    n = int(dur * SR)
    t = np.arange(n) / SR
    nz = noise(n, seed)
    nz = fft_filter(nz, low=8000, high=150)
    nz *= np.linspace(0.15, 1, n)
    env = (t / dur) ** 2
    sig = nz * env * 0.5
    sig += 0.5 * np.sin(2 * math.pi * (80 + 600 * (t / dur) ** 2) * t) * env
    return normalize(sig, 1) * amp


def whisper_voice(dur=3.0, seed=11, amp=0.20):
    n = int(dur * SR)
    t = np.arange(n) / SR
    base = noise(n, seed)
    # formant-ish bands
    out = np.zeros(n)
    for f, q, a in [(600, 2, 1.0), (1100, 2.5, 0.7), (2300, 3, 0.4)]:
        out += fft_filter(base, low=f * 1.18, high=f * 0.82, order=q) * a
    env = (0.5 + 0.5 * np.sin(2 * math.pi * 2.1 * t + 0.5)) * np.minimum(1, t / 0.2) * np.minimum(1, (dur - t) / 0.4)
    # syllable modulation
    env *= 0.35 + 0.65 * (np.sin(2 * math.pi * 3.2 * t) > -0.3)
    return out * env * amp


def distortion(x, drive=3.0):
    return np.tanh(x * drive) / np.tanh(drive)


def save_ogg(x, path, quality=5):
    if x.ndim == 1:
        x = np.stack([x, x], axis=1)
    x = np.nan_to_num(x)
    x = np.clip(x, -1, 1)
    pcm = (x * 32767).astype(np.int16)
    wav = path + ".tmp.wav"
    with wave.open(wav, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-c:a", "libvorbis", "-q:a", str(quality), path], check=True)
    os.remove(wav)
    print("wrote", path, f"({x.shape[0]/SR:.1f}s)")


# ---------------------------------------------------------------------------
# MUSIC
# ---------------------------------------------------------------------------
def music_menu():
    dur = 64
    buf = np.zeros((int(dur * SR), 2))
    # low drones D / A
    place(buf, drone(midi(38), dur, 0.20, 240, 1), 0, pan=0.0)
    place(buf, drone(midi(45), dur, 0.12, 300, 2), 0, pan=-0.2)
    place(buf, pad_chord([50, 53, 57, 62], dur, 0.10, 700, 0.005, 3), 0, pan=0.1)
    # sparse piano
    notes = [(62, 0.8), (65, 1.0), (69, 1.2), (72, 0.9), (74, 1.4), (69, 1.1), (65, 0.8), (62, 1.0),
             (60, 1.2), (65, 0.9), (69, 1.3), (72, 0.7), (70, 1.1), (65, 0.8), (62, 1.4), (57, 1.0)]
    times = [2, 6.5, 9, 14, 18, 23.5, 28, 31, 36, 40, 44, 49, 53, 56.5, 59, 61.5]
    for i, (m, a) in enumerate(notes):
        place(buf, piano(midi(m), 5.5, 0.22, 0.8, 0.001), times[i], pan=(-0.45 if i % 2 else 0.45))
    # heartbeat slow
    place(buf, heartbeat(48, dur, 0.10), 0, pan=0)
    # distant whispers / air
    w = whisper_voice(7, 21, 0.025)
    for t in (10, 28, 47):
        place(buf, w, t, pan=0.6)
    place(buf, fft_filter(noise(int(dur * SR), 4), low=400, high=60) * 0.02, 0)
    buf = reverb(buf, 0.3, 2.8, 2.6, 2)
    buf = np.stack([fade(buf[:, 0], 2, 2), fade(buf[:, 1], 2, 2)], axis=1)
    save_ogg(normalize(buf, 0.82), os.path.join(MUS, "music_menu.ogg"))


def music_ch1():
    dur = 60
    buf = np.zeros((int(dur * SR), 2))
    chords = [
        ([45, 48, 52, 57], 0, 16),
        ([41, 45, 48, 53], 16, 16),
        ([48, 52, 55, 60], 32, 14),
        ([43, 47, 50, 55], 46, 14),
    ]
    for notes, st, ln in chords:
        place(buf, pad_chord(notes, ln, 0.15, 800, 0.004, st), st, pan=0.05)
        place(buf, drone(midi(notes[0] - 12), ln, 0.15, 280, st), st)
    # piano arpeggios
    prog = [
        ([57, 60, 64, 69, 64, 60], 0),
        ([53, 57, 60, 65, 60, 57], 8),
        ([60, 64, 67, 72, 67, 64], 16),
        ([55, 59, 62, 67, 62, 59], 24),
        ([57, 60, 64, 69, 64, 60], 32),
        ([53, 57, 60, 65, 65, 60], 40),
        ([60, 64, 67, 72, 72, 67], 48),
        ([55, 59, 62, 67, 62, 59], 54),
    ]
    for notes, st in prog:
        for i, m in enumerate(notes):
            place(buf, piano(midi(m), 4.0, 0.30, 1.0, 0.001 * (i % 3)), st + i * 1.28, pan=(-0.4 if i % 2 else 0.4))
    # melody
    mel = [(76, 2.5, 4), (72, 2.0, 9), (69, 2.5, 13), (72, 1.5, 18), (74, 2.0, 21), (72, 3.0, 25),
           (69, 2.0, 31), (67, 1.5, 35), (69, 2.5, 38), (72, 2.0, 43), (69, 3.0, 48)]
    for m, ln, st in mel:
        place(buf, piano(midi(m), ln + 2, 0.20, 0.9), st, pan=0.15)
    # rain and room tone
    rain = fft_filter(noise(int(dur * SR), 3), low=8000, high=400) * 0.035
    place(buf, rain, 0)
    buf = reverb(buf, 0.28, 2.2, 3.0, 5)
    buf = np.stack([fade(buf[:, 0], 2, 3), fade(buf[:, 1], 2, 3)], axis=1)
    save_ogg(normalize(buf, 0.8), os.path.join(MUS, "music_ch1.ogg"))


def music_ch2():
    dur = 56
    buf = np.zeros((int(dur * SR), 2))
    place(buf, drone(midi(38), dur, 0.20, 220, 3), 0)
    place(buf, drone(midi(39), dur, 0.12, 180, 4), 0, pan=-0.25)
    place(buf, pad_chord([50, 51, 57], dur, 0.07, 500, 0.006, 5), 0)
    # clock
    for t in np.arange(1.0, dur - 2, 1.0):
        place(buf, tick(0.09), t, pan=0.55)
    # heartbeat slow
    place(buf, heartbeat(52, dur, 0.30), 0)
    # dissonant piano stabs
    for t, m in [(4, 62), (10, 63), (17, 62), (24, 69), (31, 63), (38, 62), (45, 70), (50, 58)]:
        place(buf, piano(midi(m), 4.0, 0.22, 0.7, 0.002), t, pan=(-0.3 if int(t) % 2 else 0.5))
        place(buf, piano(midi(m - 1), 4.0, 0.14, 0.6, -0.002), t + 0.03, pan=0.2)
    # high whine
    t = time(dur)
    whine = np.sin(2 * math.pi * 2100 * t) * 0.012 * (0.5 + 0.5 * np.sin(2 * math.pi * 0.13 * t))
    place(buf, whine, 0, pan=0.2)
    # breathing
    breath = fft_filter(noise(5 * SR, 8), low=1400, high=300)
    be = np.minimum(1, np.arange(len(breath)) / (0.8 * SR)) * np.minimum(1, (len(breath) - np.arange(len(breath))) / (1.2 * SR))
    breath = breath * be * 0.05
    for t in (8, 20, 33, 47):
        place(buf, breath, t, pan=0.1)
    buf = reverb(buf, 0.34, 2.6, 2.8, 6)
    buf = np.stack([fade(buf[:, 0], 2.5, 3), fade(buf[:, 1], 2.5, 3)], axis=1)
    save_ogg(normalize(buf, 0.8), os.path.join(MUS, "music_ch2.ogg"))


def music_ch3():
    dur = 60
    buf = np.zeros((int(dur * SR), 2))
    place(buf, drone(midi(40), dur, 0.16, 260, 7), 0)
    place(buf, pad_chord([52, 55, 59, 64], dur, 0.07, 650, 0.005, 8), 0)
    # music box melody in E minor
    mel = [(76, 4), (79, 2), (83, 2), (81, 4), (79, 2), (76, 2), (74, 4), (76, 2), (79, 2),
           (83, 2), (86, 2), (84, 3), (83, 1), (79, 4), (76, 2), (72, 2), (74, 2), (76, 2)]
    t = 2.0
    for m, d in mel:
        place(buf, bell(midi(m), 3.0, 0.22), t, pan=(-0.2 if int(t) % 2 else 0.3))
        place(buf, bell(midi(m - 12), 4.0, 0.07), t, pan=0.0)
        t += d * 0.62
        if t > dur - 4:
            break
    # low piano answers
    for st, m in [(6, 52), (14, 55), (22, 59), (30, 52), (38, 55), (46, 47), (54, 52)]:
        place(buf, piano(midi(m), 6, 0.20, 0.7), st, pan=-0.1)
    # reversed swells
    for st in (4, 18, 34, 48):
        sw = fft_filter(noise(int(3 * SR), 30 + st), low=1500, high=200)
        env = np.linspace(0, 1, len(sw)) ** 3
        place(buf, sw * env * 0.05, st, pan=0.5)
    # footsteps in the hall
    for st in (12, 13, 23, 24, 41, 42):
        step = low_thump(0.35, 70, 0.12)
        place(buf, step, st, pan=-0.5)
    buf = reverb(buf, 0.35, 2.5, 2.6, 9)
    buf = np.stack([fade(buf[:, 0], 2, 3), fade(buf[:, 1], 2, 3)], axis=1)
    save_ogg(normalize(buf, 0.8), os.path.join(MUS, "music_ch3.ogg"))


def music_ch4():
    dur = 52
    buf = np.zeros((int(dur * SR), 2))
    # pulsing D pedal
    for i, st in enumerate(np.arange(0, dur - 1, 0.5)):
        place(buf, piano(midi(38 if i % 4 else 38), 0.45, 0.10, 0.7), st, pan=0.0)
    place(buf, drone(midi(38), dur, 0.22, 200, 11), 0)
    place(buf, pad_chord([50, 53, 56, 62], dur, 0.08, 600, 0.006, 12), 0)
    # tremolo high strings
    t = time(dur)
    trem = sum(np.sin(2 * math.pi * midi(m) * t) for m in (74, 77, 81)) * 0.016
    trem *= (0.55 + 0.45 * np.sin(2 * math.pi * 7.5 * t))
    trem *= np.minimum(1, t / 3) * np.minimum(1, (dur - t) / 3)
    place(buf, trem, 0, pan=0.2)
    # heartbeat accelerating
    place(buf, heartbeat(60, dur, 0.24), 0)
    # risers
    for st in (6, 20, 34, 46):
        place(buf, riser(3.5, 0.16, int(st)), st, pan=0.0)
    # sudden phone-ish stabs
    for st, m in [(9, 63), (17, 62), (29, 64), (38, 63), (47, 62)]:
        place(buf, piano(midi(m), 3, 0.2, 0.8), st, pan=0.45)
        place(buf, piano(midi(m + 1), 3, 0.16, 0.7), st + 0.04, pan=-0.45)
    # door knock
    for st in (13.5, 14.1, 14.7, 28, 28.5):
        place(buf, low_thump(0.25, 90, 0.28), st, pan=-0.3)
    buf = reverb(buf, 0.26, 2.0, 3.1, 13)
    buf = np.stack([fade(buf[:, 0], 2, 3), fade(buf[:, 1], 2, 3)], axis=1)
    save_ogg(normalize(buf, 0.83), os.path.join(MUS, "music_ch4.ogg"))


def music_ch5():
    dur = 64
    buf = np.zeros((int(dur * SR), 2))
    chords = [([48, 51, 55, 60], 0, 16), ([44, 48, 51, 56], 16, 16), ([51, 55, 58, 63], 32, 16), ([46, 50, 53, 58], 48, 16)]
    for notes, st, ln in chords:
        place(buf, pad_chord(notes, ln, 0.13, 700, 0.004, st), st, pan=0.0)
        place(buf, drone(midi(notes[0] - 12), ln, 0.14, 250, st), st)
    # sad piano tune
    mel = [(72, 3, 2), (75, 2, 6), (72, 2, 9), (70, 3, 12), (67, 2, 16), (72, 2, 19), (75, 3, 22),
           (77, 2, 27), (75, 2, 30), (72, 4, 33), (70, 2, 39), (67, 3, 42), (63, 4, 46), (67, 2, 52), (70, 3, 55), (72, 5, 59)]
    for m, ln, st in mel:
        place(buf, piano(midi(m), ln + 2, 0.24, 0.85), st, pan=0.1)
    # low cello line
    cello = [(48, 8, 0), (46, 8, 10), (43, 10, 22), (44, 8, 34), (48, 8, 44), (46, 10, 54)]
    for m, ln, st in cello:
        t = time(ln)
        sig = sum((1 / k) * np.sin(2 * math.pi * midi(m) * k * t + k) for k in range(1, 6))
        sig = fft_filter(sig, low=500) * np.minimum(1, t / 1.5) * np.minimum(1, (ln - t) / 2) * 0.06
        place(buf, sig, st, pan=-0.25)
    # tape hiss
    hiss = fft_filter(noise(int(dur * SR), 15), low=6000, high=600) * 0.015
    place(buf, hiss, 0)
    buf = reverb(buf, 0.3, 2.6, 2.7, 15)
    buf = np.stack([fade(buf[:, 0], 2.5, 3), fade(buf[:, 1], 2.5, 3)], axis=1)
    save_ogg(normalize(buf, 0.8), os.path.join(MUS, "music_ch5.ogg"))


def music_ch6():
    dur = 56
    buf = np.zeros((int(dur * SR), 2))
    # dissonant cluster drones
    for i, m in enumerate([38, 39, 44, 45, 50]):
        place(buf, drone(midi(m), dur, 0.10, 240 + i * 40, 20 + i), 0, pan=(-0.5 + i * 0.25))
    place(buf, pad_chord([50, 51, 56, 57, 62], dur, 0.06, 900, 0.007, 21), 0)
    # chaotic heartbeat
    place(buf, heartbeat(74, dur, 0.28), 0)
    # glitch bursts
    for st in np.arange(3, dur - 2, 4.2):
        n = int(0.5 * SR)
        g = noise(n, int(st * 10))
        g = (g > 0) * g
        g = fft_filter(g, low=7000, high=300)
        env = np.exp(-np.arange(n) / (0.12 * SR))
        place(buf, g * env * 0.26, st, pan=random.Random(int(st)).uniform(-0.7, 0.7))
    # screeching high notes
    for st in (7, 19, 31, 43, 51):
        m = random.Random(int(st)).choice([86, 87, 88, 91, 92])
        place(buf, piano(midi(m), 2.2, 0.15, 0.4, 0.01), st, pan=0.6)
    # phone ring far away
    for st in (12, 37):
        ring = phone_ring(dur=4.0)
        place(buf, ring * 0.22, st, pan=-0.65)
    # distorted low piano
    for st in (0, 8, 16, 24, 32, 40, 48):
        p = piano(midi(38), 5, 0.3, 0.5)
        p = distortion(p, 2.8)
        place(buf, p, st, pan=0.0)
    buf = reverb(buf, 0.34, 2.4, 2.5, 22)
    buf = np.stack([fade(buf[:, 0], 2, 3), fade(buf[:, 1], 2, 3)], axis=1)
    save_ogg(normalize(buf, 0.85), os.path.join(MUS, "music_ch6.ogg"))


def music_ch7():
    dur = 64
    buf = np.zeros((int(dur * SR), 2))
    prog = [([38, 50, 53, 57], 0, 16), ([46, 50, 53, 58], 16, 16), ([43, 50, 55, 58], 32, 16), ([45, 52, 57, 61], 48, 16)]
    for notes, st, ln in prog:
        place(buf, pad_chord(notes, ln, 0.16, 1100, 0.005, st), st, pan=0.0)
        place(buf, drone(midi(notes[0]), ln, 0.20, 260, st), st)
    # driving low piano ostinato
    for i, st in enumerate(np.arange(0, dur - 2, 0.38)):
        m = [38, 38, 50, 38, 43, 38, 45, 38][i % 8]
        place(buf, piano(midi(m), 0.5, 0.10, 0.7), st, pan=(-0.2 if i % 2 else 0.2))
    # epic choir-ish pad
    place(buf, pad_chord([62, 65, 69, 74], dur, 0.07, 1400, 0.006, 31), 0)
    # melody
    mel = [(74, 4, 4), (77, 2, 9), (81, 4, 12), (79, 2, 18), (77, 4, 21), (74, 2, 27), (72, 4, 30),
           (74, 3, 36), (77, 3, 40), (81, 4, 44), (82, 2, 50), (81, 3, 53), (77, 4, 57)]
    for m, ln, st in mel:
        place(buf, piano(midi(m), ln + 2, 0.22, 0.9), st, pan=0.1)
    # impacts
    for st in (0, 16, 32, 48):
        place(buf, low_thump(1.2, 45, 0.6), st)
        place(buf, riser(2.5, 0.2, int(st)), st + 14 if st < 48 else 0)
    place(buf, heartbeat(80, dur, 0.12), 0)
    buf = reverb(buf, 0.33, 3.0, 2.4, 32)
    buf = np.stack([fade(buf[:, 0], 2, 3), fade(buf[:, 1], 2, 3)], axis=1)
    save_ogg(normalize(buf, 0.88), os.path.join(MUS, "music_ch7.ogg"))


def music_entity():
    dur = 42
    buf = np.zeros((int(dur * SR), 2))
    place(buf, drone(midi(26), dur, 0.22, 140, 41), 0)
    place(buf, drone(midi(27), dur, 0.12, 120, 42), 0, pan=-0.3)
    place(buf, pad_chord([38, 39, 44], dur, 0.07, 500, 0.01, 43), 0)
    # metallic scrapes
    for st in np.arange(2, dur - 3, 3.7):
        n = int(1.6 * SR)
        sr = noise(n, int(st * 7))
        sr = fft_filter(sr, low=7000, high=1600)
        env = np.abs(np.sin(np.linspace(0, math.pi * 5, n))) ** 4 * np.exp(-np.arange(n) / (0.5 * SR))
        place(buf, sr * env * 0.20, st, pan=random.Random(int(st)).uniform(-0.6, 0.6))
    # whispers
    for st in (4, 11, 18, 26, 33, 39):
        place(buf, whisper_voice(3.2, int(st), 0.30), st, pan=random.Random(st).uniform(-0.5, 0.5))
    # heartbeat
    place(buf, heartbeat(46, dur, 0.34), 0)
    # sub hits
    for st in (0, 10, 21, 31, 40):
        place(buf, low_thump(1.0, 34, 0.55), st)
    buf = reverb(buf, 0.4, 3.0, 2.2, 44)
    buf = np.stack([fade(buf[:, 0], 2, 3), fade(buf[:, 1], 2, 3)], axis=1)
    save_ogg(normalize(buf, 0.85), os.path.join(MUS, "music_entity.ogg"))


def music_ending_truth():
    dur = 58
    buf = np.zeros((int(dur * SR), 2))
    chords = [([41, 53, 57, 60], 0, 15), ([48, 52, 55, 60], 15, 15), ([50, 53, 57, 62], 30, 14), ([46, 50, 53, 58], 44, 14)]
    for notes, st, ln in chords:
        place(buf, pad_chord(notes, ln, 0.13, 1200, 0.004, st), st, pan=0.0)
        place(buf, drone(midi(notes[0] - 12), ln, 0.11, 300, st), st)
    mel = [(65, 3, 2), (69, 2, 6), (72, 4, 9), (69, 2, 15), (65, 2, 18), (67, 3, 21), (69, 4, 25),
           (72, 2, 31), (74, 2, 34), (72, 4, 37), (69, 2, 43), (65, 3, 46), (67, 3, 50), (65, 5, 54)]
    for m, ln, st in mel:
        place(buf, piano(midi(m), ln + 2, 0.25, 1.0), st, pan=0.15)
    # light bell accents
    for st, m in [(8, 84), (20, 81), (33, 84), (45, 88)]:
        place(buf, bell(midi(m), 4, 0.10), st, pan=-0.4)
    # dawn birds subtler
    for st in (6, 17, 29, 42, 51):
        n = int(0.35 * SR)
        t = np.arange(n) / SR
        f = 2300 + 900 * np.sin(np.linspace(0, 4, n))
        b = np.sin(2 * math.pi * f * t) * np.exp(-t / 0.09) * 0.04
        place(buf, b, st, pan=0.6)
    place(buf, fft_filter(noise(int(dur * SR), 45), low=9000, high=1000) * 0.015, 0)
    buf = reverb(buf, 0.28, 2.8, 2.8, 45)
    buf = np.stack([fade(buf[:, 0], 2.5, 4), fade(buf[:, 1], 2.5, 4)], axis=1)
    save_ogg(normalize(buf, 0.8), os.path.join(MUS, "music_ending_truth.ogg"))


def music_ending_alone():
    dur = 50
    buf = np.zeros((int(dur * SR), 2))
    place(buf, drone(midi(38), dur, 0.24, 180, 51), 0)
    place(buf, pad_chord([38, 50, 53], dur, 0.09, 500, 0.008, 52), 0)
    place(buf, heartbeat(42, dur, 0.36), 0)
    # broken music box
    mel = [(74, 2), (77, 2), (81, 2), (80, 2), (77, 2), (74, 2), (72, 3), (69, 3)]
    t = 3
    for m, d in mel:
        place(buf, bell(midi(m), 3.5, 0.18, ), t, pan=-0.2)
        if random.Random(int(t * 3)).random() < 0.4:
            place(buf, bell(midi(m + 1), 3, 0.07), t + 0.04, pan=0.3)
        t += d * 0.9
    # reverse swells
    for st in (6, 22, 38):
        sw = fft_filter(noise(int(4 * SR), int(st)), low=1200, high=150) * np.linspace(0, 1, int(4 * SR)) ** 2 * 0.06
        place(buf, sw, st, pan=-0.4)
    buf = reverb(buf, 0.38, 3.2, 2.3, 53)
    buf = np.stack([fade(buf[:, 0], 2, 4), fade(buf[:, 1], 2, 4)], axis=1)
    save_ogg(normalize(buf, 0.82), os.path.join(MUS, "music_ending_alone.ogg"))


def phone_ring(dur=5.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    # old electromechanical bell: 1000/1250 Hz with 20 Hz tremolo
    ring = (np.sin(2 * math.pi * 1000 * t) * 0.25 + np.sin(2 * math.pi * 1250 * t) * 0.18)
    ring *= 0.55 + 0.45 * np.sign(np.sin(2 * math.pi * 22 * t))
    ring = fft_filter(ring, low=4000)
    pattern = ((t % 3.0) < 1.2)
    ring *= pattern
    # clicks
    for st in np.arange(0, dur, 3.0):
        i = int(st * SR)
        k = min(int(0.03 * SR), n - i)
        ring[i:i + k] += noise(k, int(st)) * 0.3 * np.exp(-np.arange(k) / (0.006 * SR))
    return ring * 0.55


def music_ending_call():
    dur = 50
    buf = np.zeros((int(dur * SR), 2))
    place(buf, drone(midi(38), dur, 0.16, 220, 61), 0)
    # two piano loops, one slightly detuned / offset (the other Ethan)
    loop1 = [(62, 2, 0), (65, 2, 2), (69, 2, 4), (65, 2, 6), (64, 2, 8), (62, 2, 10), (60, 2, 12), (62, 2, 14)]
    loop2 = [(63, 2, 0.18), (66, 2, 2.18), (70, 2, 4.18), (66, 2, 6.18), (65, 2, 8.18), (63, 2, 10.18), (61, 2, 12.18), (63, 2, 14.18)]
    for base in np.arange(0, dur - 16, 16):
        for m, ln, st in loop1:
            place(buf, piano(midi(m), 4, 0.18, 0.8), base + st, pan=-0.45)
        for m, ln, st in loop2:
            place(buf, piano(midi(m), 4, 0.15, 0.8), base + st, pan=0.45)
    # static / ring
    place(buf, fft_filter(noise(int(dur * SR), 62), low=5000, high=500) * 0.025, 0)
    for st in (9, 28, 43):
        place(buf, phone_ring(4) * 0.25, st, pan=0.6)
    # glitch impulses
    for st in np.arange(2, dur - 2, 3.3):
        n = int(0.25 * SR)
        g = noise(n, int(st * 9)) * np.exp(-np.arange(n) / (0.07 * SR))
        g = (g > 0.4) * g
        place(buf, g * 0.30, st, pan=random.Random(int(st)).uniform(-0.7, 0.7))
    place(buf, heartbeat(66, dur, 0.15), 0)
    buf = reverb(buf, 0.3, 2.2, 2.9, 62)
    buf = glitch_buffer(buf, seed=6)
    buf = np.stack([fade(buf[:, 0], 2, 3), fade(buf[:, 1], 2, 3)], axis=1)
    save_ogg(normalize(buf, 0.83), os.path.join(MUS, "music_ending_call.ogg"))


def music_ending_newgame():
    dur = 52
    buf = np.zeros((int(dur * SR), 2))
    # warped version of the menu motif
    place(buf, drone(midi(38), dur, 0.18, 240, 71), 0)
    place(buf, pad_chord([50, 53, 57, 62], dur, 0.07, 600, 0.008, 72), 0)
    mel = [(62, 3), (65, 3), (69, 3), (72, 3), (70, 3), (65, 3), (62, 4), (57, 4)]
    t = 2
    for m, d in mel:
        place(buf, bell(midi(m), 4.5, 0.17), t, pan=-0.2)
        place(buf, piano(midi(m - 12), 4.5, 0.10, 0.6), t, pan=0.3)
        t += d * 1.1
    # reversed echo of the same melody
    for i, (m, d) in enumerate(mel):
        n = int(3.0 * SR)
        p = piano(midi(m), 3.0, 0.12, 0.5)
        p = p[::-1]
        place(buf, p, dur - 3 - i * 2.8, pan=0.5)
    for st in (8, 20, 34, 45):
        place(buf, riser(2.2, 0.12, int(st)), st)
    place(buf, heartbeat(50, dur, 0.10), 0)
    place(buf, fft_filter(noise(int(dur * SR), 73), low=6000, high=800) * 0.018, 0)
    buf = reverb(buf, 0.34, 2.8, 2.7, 73)
    buf = glitch_buffer(buf, seed=17, strength=0.4)
    buf = np.stack([fade(buf[:, 0], 2, 3), fade(buf[:, 1], 2, 3)], axis=1)
    save_ogg(normalize(buf, 0.82), os.path.join(MUS, "music_ending_newgame.ogg"))


def glitch_buffer(buf, seed=0, strength=1.0):
    r = np.random.default_rng(seed)
    out = buf.copy()
    n = len(buf)
    for _ in range(int(10 * strength)):
        st = int(r.integers(0, max(1, n - SR // 2)))
        ln = int(r.integers(SR // 40, SR // 8))
        out[st:st + ln] *= r.uniform(0, 0.25)
    return out


# ---------------------------------------------------------------------------
# SFX
# ---------------------------------------------------------------------------
def sfx_rain():
    dur = 22
    n = int(dur * SR)
    baseL = fft_filter(noise(n, 101), low=12000, high=500) * 0.22
    baseR = fft_filter(noise(n, 102), low=12000, high=500) * 0.22
    # droplets
    r = random.Random(5)
    for _ in range(2200):
        i = r.randrange(n - 2000)
        ln = r.randrange(200, 1800)
        amp = r.uniform(0.005, 0.05)
        f = r.uniform(1800, 7000)
        t = np.arange(ln) / SR
        drop = np.sin(2 * math.pi * f * t) * np.exp(-t / r.uniform(0.002, 0.012)) * amp
        baseL[i:i + ln] += drop * r.uniform(0, 1)
    # low rumble
    rumble = fft_filter(noise(n, 103), low=180, high=30) * 0.08
    l = baseL + rumble
    rr = baseR + rumble
    out = stereo(l, rr)
    save_ogg(normalize(out, 0.75), os.path.join(SFX, "rain_loop.ogg"), 6)


def sfx_thunder():
    dur = 6.5
    n = int(dur * SR)
    t = np.arange(n) / SR
    crack = fft_filter(noise(n, 111), low=11000, high=900) * np.exp(-t / 0.18) * 0.7
    rumble = fft_filter(noise(n, 112), low=240, high=25) * (1 - np.exp(-t / 0.3)) * np.exp(-t / 2.4)
    rumble *= 0.55 + 0.45 * np.sin(2 * math.pi * 5 * t)
    sub = np.sin(2 * math.pi * 38 * t) * np.exp(-t / 1.4) * 0.35
    sig = crack + rumble + sub
    out = stereo(sig, np.roll(sig, 180) * 0.96)
    save_ogg(normalize(out, 0.88), os.path.join(SFX, "thunder.ogg"), 5)


def sfx_footsteps():
    dur = 3.0
    n = int(dur * SR)
    out = np.zeros((n, 2))
    for i, st in enumerate((0.05, 0.62, 1.38, 2.05)):
        th = low_thump(0.5, 62 + i * 6, 0.5)
        scuff = fft_filter(noise(int(0.22 * SR), 120 + i), low=3500, high=300) * np.exp(-np.arange(int(0.22 * SR)) / (0.04 * SR)) * 0.25
        place(out, th, st, pan=-0.3 + i * 0.2)
        place(out, scuff, st, pan=-0.3 + i * 0.2)
    save_ogg(normalize(out, 0.8), os.path.join(SFX, "footsteps.ogg"), 5)


def sfx_door_creak():
    dur = 3.2
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 160 + 260 * (t / dur) ** 0.7 + 18 * np.sin(2 * math.pi * 7 * t)
    phase = 2 * math.pi * np.cumsum(f) / SR
    tone = np.sin(phase) * 0.18 + 0.5 * np.sin(phase * 2.01) * 0.08
    rough = fft_filter(noise(n, 131), low=3000, high=200) * 0.25
    env = np.minimum(1, t / 0.15) * np.minimum(1, (dur - t) / 0.5) * (0.4 + 0.6 * np.abs(np.sin(2 * math.pi * 1.2 * t)))
    sig = (tone + rough) * env
    out = stereo(sig, np.roll(sig, 300) * 0.9)
    save_ogg(normalize(out, 0.8), os.path.join(SFX, "door_creak.ogg"), 5)


def sfx_door_slam():
    dur = 2.2
    n = int(dur * SR)
    t = np.arange(n) / SR
    hit = noise(n, 141) * np.exp(-t / 0.035) * 0.8
    th = np.sin(2 * math.pi * 48 * t) * np.exp(-t / 0.35) * 0.9
    rattle = fft_filter(noise(n, 142), low=5000, high=300) * np.exp(-t / 0.25) * 0.2
    sig = hit + th + rattle
    out = stereo(sig, np.roll(sig, 150))
    save_ogg(normalize(out, 0.9), os.path.join(SFX, "door_slam.ogg"), 5)


def sfx_phone_ring():
    out = np.stack([phone_ring(6.0), np.roll(phone_ring(6.0), 200) * 0.92], axis=1)
    save_ogg(normalize(out, 0.82), os.path.join(SFX, "phone_ring.ogg"), 6)


def sfx_phone_vibrate():
    dur = 2.0
    n = int(dur * SR)
    t = np.arange(n) / SR
    buzz = np.sin(2 * math.pi * 62 * t) * (0.5 + 0.5 * np.sign(np.sin(2 * math.pi * 28 * t)))
    buzz = fft_filter(buzz, low=300) * 0.5
    sig = buzz * ((t % 1.0) < 0.65)
    save_ogg(stereo(sig, np.roll(sig, 60)), os.path.join(SFX, "phone_vibrate.ogg"), 5)


def sfx_whisper():
    w1 = whisper_voice(3.6, 151, 0.5)
    w2 = whisper_voice(3.6, 152, 0.3)
    sig = stereo(w1, w2)
    save_ogg(normalize(sig, 0.65), os.path.join(SFX, "whisper.ogg"), 5)


def sfx_breathing():
    dur = 5.0
    n = int(dur * SR)
    t = np.arange(n) / SR
    env_in = np.clip(1 - np.abs(t - 1.1) / 1.1, 0, 1) ** 2
    env_out = np.clip(1 - np.abs(t - 3.4) / 1.3, 0, 1) ** 2
    base = fft_filter(noise(n, 161), low=1600, high=250)
    sig = base * (env_in * 0.8 + env_out * 0.6)
    save_ogg(stereo(sig, np.roll(sig, 200)), os.path.join(SFX, "breathing.ogg"), 5)


def sfx_heartbeat():
    sig = heartbeat(70, 5.5, 0.85)
    save_ogg(stereo(sig, sig * 0.98), os.path.join(SFX, "heartbeat.ogg"), 5)


def sfx_glitch():
    dur = 1.4
    n = int(dur * SR)
    t = np.arange(n) / SR
    gate = (np.sin(2 * math.pi * 17 * t) > 0).astype(float)
    sig = noise(n, 171) * gate * np.exp(-t / 0.7) * 0.6
    for _ in range(6):
        i = random.randrange(n - 3000)
        ln = random.randrange(600, 3000)
        sig[i:i + ln] *= 0.1
    sig = distortion(sig, 3)
    sig = fft_filter(sig, low=9000, high=200)
    save_ogg(stereo(sig, np.roll(sig, 100)), os.path.join(SFX, "glitch.ogg"), 5)


def sfx_jumpscare():
    dur = 3.2
    n = int(dur * SR)
    t = np.arange(n) / SR
    # dissonant stinger
    chord = sum(np.sin(2 * math.pi * midi(m) * t) for m in (50, 51, 56, 62, 63, 68)) * 0.09
    chord *= np.exp(-t / 1.0)
    impact = noise(n, 181) * np.exp(-t / 0.12) * 0.8
    sub = np.sin(2 * math.pi * 34 * t) * np.exp(-t / 0.9) * 0.6
    scream_t = time(1.3)
    f = 600 + 1400 * np.exp(-scream_t / 0.25) + 200 * np.sin(2 * math.pi * 9 * scream_t)
    scream = np.sin(2 * math.pi * np.cumsum(f) / SR) * 0.22 * np.exp(-scream_t / 0.7)
    scream += noise(len(scream_t), 182) * 0.15 * np.exp(-scream_t / 0.5)
    sig = chord + impact + sub
    sig[:len(scream)] += scream
    sig = distortion(sig, 1.8)
    out = stereo(sig, np.roll(sig, 120) * 0.97)
    save_ogg(normalize(out, 0.95), os.path.join(SFX, "jumpscare.ogg"), 6)


def sfx_static():
    dur = 3.0
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = fft_filter(noise(n, 191), low=9000, high=300) * 0.5
    sig *= 0.6 + 0.4 * np.sign(np.sin(2 * math.pi * 30 * t))
    sig = (sig > 0.12) * sig
    save_ogg(stereo(sig, np.roll(sig, 90)), os.path.join(SFX, "static.ogg"), 5)


def sfx_light_flicker():
    dur = 1.2
    n = int(dur * SR)
    t = np.arange(n) / SR
    buzz = np.sin(2 * math.pi * 120 * t) * 0.15 + noise(n, 201) * 0.1
    gate = (np.sin(2 * math.pi * 11 * t) > -0.2).astype(float)
    sig = buzz * gate * np.exp(-t / 1.0)
    save_ogg(stereo(sig, sig), os.path.join(SFX, "light_flicker.ogg"), 5)


def sfx_ui_hover():
    dur = 0.18
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = (np.sin(2 * math.pi * 900 * t) * 0.5 + np.sin(2 * math.pi * 1350 * t) * 0.2) * np.exp(-t / 0.05)
    save_ogg(stereo(sig, sig), os.path.join(SFX, "ui_hover.ogg"), 4)


def sfx_ui_click():
    dur = 0.3
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = noise(n, 211) * np.exp(-t / 0.02) * 0.4 + np.sin(2 * math.pi * 520 * t) * np.exp(-t / 0.07) * 0.3
    save_ogg(stereo(sig, sig), os.path.join(SFX, "ui_click.ogg"), 4)


def sfx_phone_notify():
    dur = 1.2
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = np.zeros(n)
    for st, m in ((0, 88), (0.18, 92)):
        i = int(st * SR)
        ln = int(0.7 * SR)
        tt = np.arange(ln) / SR
        b = np.sin(2 * math.pi * midi(m) * tt) * np.exp(-tt / 0.18) * 0.4
        sig[i:i + ln] += b[:n - i]
    save_ogg(stereo(sig, np.roll(sig, 80)), os.path.join(SFX, "phone_notify.ogg"), 5)


def sfx_tape():
    dur = 4.0
    n = int(dur * SR)
    t = np.arange(n) / SR
    hiss = fft_filter(noise(n, 221), low=7000, high=800) * 0.1
    click = np.zeros(n)
    for st in (0.1, 0.4, 2.8):
        i = int(st * SR)
        k = int(0.04 * SR)
        click[i:i + k] += noise(k, int(st * 10)) * np.exp(-np.arange(k) / (0.006 * SR)) * 0.5
    motor = np.sin(2 * math.pi * 42 * t) * 0.05 * (t < 3.6)
    sig = hiss + click + motor
    save_ogg(stereo(sig, np.roll(sig, 60)), os.path.join(SFX, "tape.ogg"), 5)


def sfx_music_box():
    mel = [(88, 0.0), (84, 0.4), (81, 0.8), (76, 1.2), (79, 2.0), (76, 2.5)]
    n = int(4.5 * SR)
    sig = np.zeros(n)
    for m, st in mel:
        b = bell(midi(m), 2.5, 0.3)
        i = int(st * SR)
        k = min(len(b), n - i)
        sig[i:i + k] += b[:k]
    save_ogg(stereo(sig, np.roll(sig, 300)), os.path.join(SFX, "music_box.ogg"), 5)


def sfx_clock_tick():
    n = int(1.2 * SR)
    sig = np.zeros(n)
    for st, a in ((0.0, 0.6), (0.5, 0.45)):
        i = int(st * SR)
        c = tick(a)
        k = min(len(c), n - i)
        sig[i:i + k] += c[:k]
    save_ogg(stereo(sig, np.roll(sig, 50)), os.path.join(SFX, "clock_tick.ogg"), 5)


def sfx_water_drip():
    dur = 2.5
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = np.zeros(n)
    for st in (0.1, 1.3):
        i = int(st * SR)
        ln = int(0.6 * SR)
        tt = np.arange(ln) / SR
        f = 1200 * np.exp(-tt / 0.05) + 300
        d = np.sin(2 * math.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.1) * 0.4
        sig[i:i + ln] += d
    save_ogg(stereo(sig, np.roll(sig, 200)), os.path.join(SFX, "water_drip.ogg"), 5)


def sfx_knife():
    dur = 0.8
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = sum(np.sin(2 * math.pi * f * t) * a * np.exp(-t / 0.25) for f, a in ((3200, 0.10), (4700, 0.07), (6100, 0.04)))
    sig += noise(n, 231) * np.exp(-t / 0.02) * 0.4
    save_ogg(stereo(sig, np.roll(sig, 20)), os.path.join(SFX, "knife.ogg"), 5)


def sfx_paper():
    dur = 1.4
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = np.zeros(n)
    for _ in range(20):
        i = random.randrange(n - 3000)
        ln = random.randrange(300, 3000)
        cr = noise(ln, random.randrange(999)) * np.exp(-np.arange(ln) / (ln / 3)) * 0.15
        sig[i:i + ln] += cr
    sig = fft_filter(sig, low=8000, high=700)
    save_ogg(stereo(sig, np.roll(sig, 30)), os.path.join(SFX, "paper.ogg"), 5)


def sfx_wind():
    dur = 8
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = fft_filter(noise(n, 241), low=900, high=60) * 0.5
    sig *= 0.3 + 0.7 * (0.5 + 0.5 * np.sin(2 * math.pi * 0.13 * t + 1.3))
    sig *= np.minimum(1, t / 2) * np.minimum(1, (dur - t) / 2)
    save_ogg(stereo(sig, np.roll(sig, 800)), os.path.join(SFX, "wind.ogg"), 5)


def sfx_door_unlock():
    dur = 1.6
    n = int(dur * SR)
    sig = np.zeros(n)
    for st, f in ((0.0, 1200), (0.15, 900), (0.55, 700), (0.7, 1300)):
        i = int(st * SR)
        k = int(0.08 * SR)
        tt = np.arange(k) / SR
        c = np.sin(2 * math.pi * f * tt) * np.exp(-tt / 0.02) * 0.4 + noise(k, int(st * 10)) * np.exp(-tt / 0.01) * 0.2
        sig[i:i + k] += c
    save_ogg(stereo(sig, sig), os.path.join(SFX, "door_unlock.ogg"), 5)


def sfx_drawer():
    dur = 1.4
    n = int(dur * SR)
    t = np.arange(n) / SR
    slide = fft_filter(noise(n, 251), low=2500, high=200) * 0.3
    env = np.minimum(1, t / 0.15) * np.minimum(1, (dur - t) / 0.2)
    sig = slide * env
    th = low_thump(0.2, 90, 0.4)
    sig[:len(th)] += th
    save_ogg(stereo(sig, np.roll(sig, 40)), os.path.join(SFX, "drawer.ogg"), 5)


def sfx_scream():
    dur = 2.2
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 500 + 900 * np.exp(-t / 0.7) + 100 * np.sin(2 * math.pi * 7 * t)
    scream = np.sin(2 * math.pi * np.cumsum(f) / SR) * 0.4
    scream += noise(n, 261) * 0.2
    scream = distortion(scream, 2.2) * np.exp(-t / 1.5)
    save_ogg(stereo(scream, np.roll(scream, 150)), os.path.join(SFX, "scream.ogg"), 5)


def build_all():
    tracks = [music_menu, music_ch1, music_ch2, music_ch3, music_ch4, music_ch5, music_ch6,
              music_ch7, music_entity, music_ending_truth, music_ending_alone,
              music_ending_call, music_ending_newgame]
    for fn in tracks:
        fn()
    sfx = [sfx_rain, sfx_thunder, sfx_footsteps, sfx_door_creak, sfx_door_slam,
           sfx_phone_ring, sfx_phone_vibrate, sfx_whisper, sfx_breathing, sfx_heartbeat,
           sfx_glitch, sfx_jumpscare, sfx_static, sfx_light_flicker, sfx_ui_hover,
           sfx_ui_click, sfx_phone_notify, sfx_tape, sfx_music_box, sfx_clock_tick,
           sfx_water_drip, sfx_knife, sfx_paper, sfx_wind, sfx_door_unlock, sfx_drawer, sfx_scream]
    for fn in sfx:
        fn()


if __name__ == "__main__":
    build_all()
