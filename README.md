# DON'T LOOK BEHIND YOU — Windows and Android release

Official Ren'Py project and React + Vite website for the 64-bit Windows desktop edition and universal Android APK.

## Build the Windows game

Use Ren'Py 8.3.7. The SDK must include its Windows x86_64 runtime files. From the SDK installation, build only the Windows `win` package:

```bash
./renpy.sh /path/to/renpy-8.3.7-sdk/launcher distribute /path/to/lyrics --destination /path/to/lyrics/release/windows --package win
```

Ren'Py writes `DontLookBehindYou-win.zip`. Rename it to `DontLookBehindYou-Windows-v1.0.1.zip` in `release/windows/`. The project already sets the game version, executable name, 1920×1080 GUI, icon, and save directory. `README.txt` is included in the generated package.

### Build on Windows

The Windows build target must be built with the Windows x86_64 runtime from the official Ren'Py 8.3.7 SDK. On a Windows build machine:

1. Download and extract the Ren'Py 8.3.7 SDK from the official Ren'Py website.
2. Open the Ren'Py Launcher and add this project directory (`lyrics`) to its project list.
3. Select the project and choose **Build Distributions**.
4. Select only the Windows 64-bit (`win`) package and build it.
5. Copy the generated `DontLookBehindYou-win.zip` to `release/windows/` and rename it `DontLookBehindYou-Windows-v1.0.1.zip`.
6. On the deployment checkout, run `npm install` and `npm run build`; the build calculates both archive checksums and copies the release files into `dist/downloads/`.
7. Launch `DontLookBehindYou.exe` on Windows 10 or 11 and verify the menus, audio, save/load, fullscreen, and windowed modes before claiming Windows runtime testing.

## Build the Android APK

Use the Ren'Py 8.3.7 SDK with RAPT, JDK 21, and Android SDK platform 35. Configure `android.json` for package `com.dontlookbehindyou.game`, version `1.0.1`, and landscape orientation. From the Ren'Py SDK directory:

```bash
export JAVA_HOME=/path/to/jdk-21
export ANDROID_HOME=/path/to/renpy-8.3.7-sdk/rapt/Sdk
export ANDROID_SDK_ROOT="$ANDROID_HOME"
SDL_VIDEODRIVER=dummy ./renpy.sh launcher android_build /path/to/lyrics --destination /path/to/lyrics/release/android
```

RAPT writes a timestamped APK. Copy the new file to the stable release name:

```bash
cp release/android/com.dontlookbehindyou.game-1.0.1-*-release.apk release/android/DontLookBehindYou-Android-v1.0.1.apk
```

Verify the package before publishing:

```bash
export PATH="/path/to/jdk-21/bin:$PATH"
/path/to/rapt/Sdk/build-tools/34.0.0/apksigner verify --verbose release/android/DontLookBehindYou-Android-v1.0.1.apk
/path/to/rapt/Sdk/build-tools/34.0.0/aapt dump badging release/android/DontLookBehindYou-Android-v1.0.1.apk
```

The release is a universal APK with `arm64-v8a`, `armeabi-v7a`, and `x86_64` native code. It uses `minSdkVersion` 21 (Android 5.0) and `targetSdkVersion` 35. Back up the generated `android.keystore` and `bundle.keystore` securely; future updates must use the same signing keys. The keystores are ignored by git.

Lint the story before building either release:

```bash
/path/to/renpy-8.3.7-sdk/renpy.sh /path/to/lyrics lint
```

## Build and run the website

Requirements: Node.js 22.12+ (or 20.19+) and npm.

```bash
npm install
npm run dev
```

The production build calculates the Windows and Android archive sizes and SHA-256 values, builds the React website, and copies both archives into `dist/downloads/`:

```bash
npm run build
npm run preview
npm run qa
```

Keep both release archives in the project when building the website. `scripts/update-release-size.mjs` derives file size and checksum from the actual files. The Vite build copies them to `/downloads/DontLookBehindYou-Windows-v1.0.1.zip` and `/downloads/DontLookBehindYou-Android-v1.0.1.apk`.

To use external file hosting, set `VITE_WINDOWS_DOWNLOAD_URL` or `VITE_ANDROID_DOWNLOAD_URL` to the direct public archive URL. Set the matching `VITE_*_FILE_SIZE` value only when the externally hosted archive is not present in the project. `VITE_GAME_VERSION` can override the displayed version.

Play Online is enabled only when `VITE_RENPY_WEB_URL` points to a working, browser-ready Ren'Py Web player. Do not point it at a ZIP, APK, or desktop executable.

## Voice acting

The game includes generated Piper voices for narration, Ethan, Maya, Iris, the Listener, Mom, and Dad. The 1,118 dialogue clips are stored under `game/audio/voice/`; `game/voice_ids.rpy` maps dialogue source locations to those clips. The voice generator rebuilds that map whenever it synthesizes audio.

Install the Piper executable and the ONNX voice models listed in `tools/generate_voice.py`, then set `PIPER_BIN` and `PIPER_MODEL_DIR` to their locations. FFmpeg must also be available on `PATH`.

```bash
python3 tools/generate_voice.py --dry-run
PIPER_BIN=/path/to/piper PIPER_MODEL_DIR=/path/to/piper-voices python3 tools/generate_voice.py
```

After editing dialogue without synthesizing audio, refresh the source map with `python3 tools/generate_voice.py --write-map-only`.

## Render Static Site

The existing `render.yaml` uses:

- Build command: `npm install && npm run build`
- Publish directory: `dist`

Connect this repository to Render as a Static Site. Both the Windows ZIP and Android APK must be committed with the repository for the built-in download URLs to work. If either archive is hosted elsewhere, configure its `VITE_*_DOWNLOAD_URL` in Render's build environment. Vite embeds `VITE_*` values during the build.

`render.yaml` serves APK files with the Android package MIME type. The download page links to the actual files included in the deployment; it never substitutes placeholder URLs.

## Player notes

- Windows is 64-bit and targets Windows 10 and Windows 11. The executable name is `DontLookBehindYou.exe`.
- Windows builds are unsigned. SmartScreen may identify the executable as an unknown publisher.
- The Android APK is self-signed for direct distribution outside Google Play. Android may require permission to install apps from the browser or file manager used to open it.
- Never tell players to disable Google Play Protect. Point them to the official SHA-256 and tell them to cancel if the package does not match.
- Android runs in landscape and is intended for Android 5.0 or newer.
- A clean-machine Windows launch and a physical Android install/full playthrough must be performed before claiming those runtimes as tested. A successful package build on Linux is not a runtime test.

## Project layout

- `game/` — Ren'Py scripts, illustrations, audio, GUI, and fonts
- `android.json` — Android package, signing, icon, and orientation settings
- `src/` — React website
- `release/windows/` — final Windows game ZIP
- `release/android/` — final Android APK
- `public/images/` — website artwork and original game illustrations
- `scripts/update-release-size.mjs` — calculates archive sizes and SHA-256 values
- `vite.config.js` — copies the release archives into the website build
