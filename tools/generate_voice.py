#!/usr/bin/env python3
import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import wave
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIALOGUE = ROOT / "dialogue.tab"
VOICE_DIR = ROOT / "game" / "audio" / "voice"
PIPER = Path(os.environ.get("PIPER_BIN", shutil.which("piper") or "/tmp/opencode/tts/piper/piper"))
MODEL_DIR = Path(os.environ.get("PIPER_MODEL_DIR", "/tmp/opencode/tts/voices"))
FFMPEG = shutil.which("ffmpeg") or "/usr/bin/ffmpeg"

VOICES = {
    "narrator": ("en_GB-northern_english_male-medium.onnx", 1.06, 0.58, 0.82),
    "ethan": ("en_US-ryan-high.onnx", 0.98, 0.7, 0.8),
    "maya": ("en_US-kristin-medium.onnx", 0.98, 0.66, 0.82),
    "iris": ("en_US-lessac-high.onnx", 1.08, 0.52, 0.72),
    "entity": ("en_US-hfc_male-medium.onnx", 1.10, 0.74, 0.92),
    "mom": ("en_GB-cori-high.onnx", 0.98, 0.62, 0.78),
    "dad": ("en_GB-alan-medium.onnx", 0.98, 0.62, 0.78),
}

ROLE_MAP = {
    "": "narrator",
    "e": "ethan",
    "m": "maya",
    "i": "iris",
    "listener": "entity",
    "stranger": "entity",
    "mom": "mom",
    "dad": "dad",
}

VOICEMAILS = [
    ("voicemail_maya", "maya", "Ethan. If you get this, don't come alone. And don't trust the hallway. I'm sorry. I should have told you what I found.", 0.98),
    ("voicemail_mom", "mom", "I'm sorry. We should have told you. The music box is the lock. Don't let him finish the call.", 0.98),
    ("voicemail_unknown", "entity", "One night left. Bring the box. Bring the girl. Bring whoever you want to lose. I will be waiting where the wall is thinnest.", 1.10),
]

TAG_RE = re.compile(r"\{[^{}]*\}")
SPACE_RE = re.compile(r"\s+")


def clean_text(text):
    text = TAG_RE.sub("", text)
    text = text.replace("—", ", ").replace("–", ", ")
    text = text.replace("“", '"').replace("”", '"')
    text = text.replace("‘", "'").replace("’", "'")
    return SPACE_RE.sub(" ", text).strip()


def load_lines():
    with DIALOGUE.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    lines = []
    seen = set()
    for row in rows:
        ident = row["Identifier"].strip()
        if not ident:
            continue
        if ident in seen:
            raise SystemExit("Duplicate voice identifier: %s" % ident)
        seen.add(ident)
        role_key = row["Character"].strip()
        role = ROLE_MAP.get(role_key)
        if role is None:
            raise SystemExit("No voice mapping for character %r (%s)" % (role_key, ident))
        text = clean_text(row["Dialogue"])
        if not text:
            continue
        lines.append((ident, role, text, row["Filename"], row["Line Number"]))
    return lines


def write_voice_id_map(lines):
    entries = {}
    for ident, _, _, filename, line_number in lines:
        location = (Path(filename).name, int(line_number))
        if location in entries:
            raise SystemExit("Duplicate voice source location: %s:%s" % location)
        entries[location] = ident

    output = ROOT / "game" / "voice_ids.rpy"
    with output.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("init -21 python:\n")
        handle.write("    VOICE_IDS_BY_LOCATION = {\n")
        for (filename, line_number), ident in sorted(entries.items()):
            handle.write("        (%r, %d): %r,\n" % (filename, line_number, ident))
        handle.write("    }\n")
    print("Wrote %d voice IDs to %s" % (len(entries), output.relative_to(ROOT)))


def piper_command(model, text_file, jsonl_file, length_scale, noise_scale, noise_w):
    return [
        str(PIPER),
        "--model", str(MODEL_DIR / model),
        "--config", str(MODEL_DIR / (model + ".json")),
        "--json-input",
        "--quiet",
        "--length_scale", str(length_scale),
        "--noise_scale", str(noise_scale),
        "--noise_w", str(noise_w),
        "--sentence_silence", "0.12",
    ], text_file, jsonl_file


def wav_duration(path):
    with wave.open(str(path), "rb") as handle:
        return handle.getnframes() / float(handle.getframerate())


def to_ogg(wav_path, ogg_path):
    command = [
        FFMPEG, "-hide_banner", "-loglevel", "error", "-y",
        "-i", str(wav_path),
        "-c:a", "libvorbis", "-q:a", "4",
        "-ar", "22050", "-ac", "1",
        str(ogg_path),
    ]
    subprocess.run(command, check=True)


def synthesize_group(role, items, force, workdir):
    model, length_scale, noise_scale, noise_w = VOICES[role]
    pending = []
    for ident, text in items:
        ogg = VOICE_DIR / (ident + ".ogg")
        if force or not ogg.exists():
            pending.append((ident, text, ogg))
    if not pending:
        print("  %s: up to date (%d lines)" % (role, len(items)))
        return 0, 0.0

    jsonl = workdir / (role + ".jsonl")
    with jsonl.open("w", encoding="utf-8") as handle:
        for ident, text, ogg in pending:
            wav = workdir / (ident + ".wav")
            handle.write(json.dumps({"text": text, "output_file": str(wav)}, ensure_ascii=False) + "\n")

    command, _, _ = piper_command(model, None, None, length_scale, noise_scale, noise_w)
    with jsonl.open("rb") as handle:
        subprocess.run(command, stdin=handle, check=True)

    total_seconds = 0.0
    missing = []
    for index, (ident, text, ogg) in enumerate(pending, 1):
        wav = workdir / (ident + ".wav")
        if not wav.exists():
            missing.append(ident)
            continue
        total_seconds += wav_duration(wav)
        to_ogg(wav, ogg)
        wav.unlink()
        if index % 100 == 0:
            print("  %s: %d/%d" % (role, index, len(pending)))
    if missing:
        raise SystemExit("%s: missing WAV output for %d lines (first: %s)" % (role, len(missing), missing[0]))
    print("  %s: generated %d lines (%.1f minutes)" % (role, len(pending), total_seconds / 60.0))
    return len(pending), total_seconds


def synthesize_voicemails(force, workdir):
    pending = []
    for ident, role, text, length_scale in VOICEMAILS:
        ogg = VOICE_DIR / (ident + ".ogg")
        if force or not ogg.exists():
            pending.append((ident, role, text, length_scale, ogg))
    if not pending:
        print("  voicemail: up to date")
        return 0, 0.0

    grouped = defaultdict(list)
    for ident, role, text, length_scale, ogg in pending:
        grouped[role].append((ident, text, length_scale, ogg))

    total_seconds = 0.0
    for role, items in grouped.items():
        model = VOICES[role][0]
        jsonl = workdir / ("voicemail_%s.jsonl" % role)
        with jsonl.open("w", encoding="utf-8") as handle:
            for ident, text, length_scale, ogg in items:
                wav = workdir / (ident + ".wav")
                handle.write(json.dumps({"text": text, "output_file": str(wav)}, ensure_ascii=False) + "\n")
        command = [
            str(PIPER),
            "--model", str(MODEL_DIR / model),
            "--config", str(MODEL_DIR / (model + ".json")),
            "--json-input", "--quiet",
            "--length_scale", str(items[0][2]),
            "--noise_scale", "0.66", "--noise_w", "0.82",
            "--sentence_silence", "0.18",
        ]
        with jsonl.open("rb") as handle:
            subprocess.run(command, stdin=handle, check=True)
        for ident, text, length_scale, ogg in items:
            wav = workdir / (ident + ".wav")
            if not wav.exists():
                raise SystemExit("Missing voicemail WAV: %s" % wav)
            total_seconds += wav_duration(wav)
            to_ogg(wav, ogg)
            wav.unlink()
    print("  voicemail: generated %d lines (%.1f minutes)" % (len(pending), total_seconds / 60.0))
    return len(pending), total_seconds


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--skip-voicemail", action="store_true")
    parser.add_argument("--write-map-only", action="store_true")
    args = parser.parse_args()

    if not DIALOGUE.exists():
        raise SystemExit("Dialogue table not found: %s" % DIALOGUE)

    lines = load_lines()
    if args.write_map_only:
        write_voice_id_map(lines)
        return

    counts = Counter(role for _, role, _, _, _ in lines)
    print("Loaded %d voice lines from %s" % (len(lines), DIALOGUE.name))
    for role in VOICES:
        print("  %-9s %4d" % (role, counts[role]))
    if args.dry_run:
        return

    if not PIPER.exists():
        raise SystemExit("Piper not found: %s (set PIPER_BIN to the Piper executable)" % PIPER)
    if not MODEL_DIR.is_dir():
        raise SystemExit("Piper model directory not found: %s (set PIPER_MODEL_DIR)" % MODEL_DIR)

    write_voice_id_map(lines)
    VOICE_DIR.mkdir(parents=True, exist_ok=True)
    workdir = Path(tempfile.mkdtemp(prefix="dontlook_voice_", dir="/tmp/opencode"))
    total_files = 0
    total_seconds = 0.0
    try:
        for role in VOICES:
            items = [(ident, text) for ident, r, text, _, _ in lines if r == role]
            if not items:
                continue
            print("Synthesizing %s..." % role)
            generated, seconds = synthesize_group(role, items, args.force, workdir)
            total_files += generated
            total_seconds += seconds
        if not args.skip_voicemail:
            print("Synthesizing voicemail...")
            generated, seconds = synthesize_voicemails(args.force, workdir)
            total_files += generated
            total_seconds += seconds
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    ogg_count = len(list(VOICE_DIR.glob("*.ogg")))
    print("Generated %d files (%.1f minutes). Voice directory now has %d OGG files." % (total_files, total_seconds / 60.0, ogg_count))


if __name__ == "__main__":
    sys.exit(main())
