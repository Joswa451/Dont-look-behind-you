# DON'T LOOK BEHIND YOU — Windows release

Official Ren'Py project and existing React + Vite website for the 64-bit Windows desktop edition.

## Build the Windows game

Use Ren'Py 8.3.7. The SDK must include its Windows x86_64 runtime files. From the SDK installation, build only the Windows `win` package:

```bash
./renpy.sh /path/to/renpy-8.3.7-sdk/launcher distribute /path/to/lyrics --destination /path/to/lyrics/release/windows --package win
```

Ren'Py writes `DontLookBehindYou-win.zip`. Rename it to `DontLookBehindYou-Windows-v1.0.0.zip` in `release/windows/`. The project already sets the game version, executable name, 1920×1080 GUI, icon, and save directory. `README.txt` is included in the generated package.

### Build on Windows

The Windows build target must be built with the Windows x86_64 runtime from the official Ren'Py 8.3.7 SDK. On a Windows build machine:

1. Download and extract the Ren'Py 8.3.7 SDK from the official Ren'Py website.
2. Open the Ren'Py Launcher and add this project directory (`lyrics`) to its project list.
3. Select the project and choose **Build Distributions**.
4. Select only the Windows 64-bit (`win`) package and build it.
5. Copy the generated `DontLookBehindYou-win.zip` to `release/windows/` and rename it `DontLookBehindYou-Windows-v1.0.0.zip`.
6. On the deployment checkout, run `npm install` and `npm run build`; the build calculates the archive checksum and copies the ZIP into `dist/downloads/`.
7. Launch `DontLookBehindYou.exe` on Windows 10 or 11 and verify the menus, audio, save/load, fullscreen, and windowed modes before claiming Windows runtime testing.

Lint the story before building:

```bash
/path/to/renpy-8.3.7-sdk/renpy.sh /path/to/lyrics lint
```

The official Windows distribution bundles the Ren'Py runtime, Python runtime, required libraries, and archived game content. Players extract the ZIP and double-click `DontLookBehindYou.exe`; they do not need a development environment.

## Build and run the website

Requirements: Node.js 22.12+ (or 20.19+) and npm.

```bash
npm install
npm run dev
```

The production build command calculates the Windows ZIP size and SHA-256, builds the React website, and copies the ZIP into `dist/downloads/`:

```bash
npm run build
npm run preview
npm run qa
```

Keep `release/windows/DontLookBehindYou-Windows-v1.0.0.zip` in the project when building the website. `scripts/update-release-size.mjs` derives file size and checksum from that actual archive. The Vite build copies the archive to the URL `/downloads/DontLookBehindYou-Windows-v1.0.0.zip`.

To use external file hosting, set `VITE_WINDOWS_DOWNLOAD_URL` to the direct public archive URL. Set `VITE_WINDOWS_FILE_SIZE` only when the externally hosted archive is not present in the project. `VITE_GAME_VERSION` can override the displayed version.

## Render Static Site

The existing `render.yaml` uses:

- Build command: `npm install && npm run build`
- Publish directory: `dist`

Connect this repository to Render as a Static Site. The Windows ZIP must be committed with the repository for the built-in download URL to work. If the archive is hosted elsewhere, configure `VITE_WINDOWS_DOWNLOAD_URL` in Render's build environment. Vite embeds `VITE_*` values during the build.

## Windows player notes

- The game is 64-bit and targets Windows 10 and Windows 11.
- The executable name is `DontLookBehindYou.exe`.
- The release is not digitally signed. SmartScreen may identify it as an unknown publisher.
- The ZIP includes `README.txt` with extraction steps and troubleshooting guidance.
- Archive integrity can be checked on Linux with `unzip -t release/windows/DontLookBehindYou-Windows-v1.0.0.zip`.
- A Windows 10/11 clean-machine launch and full playthrough must be performed on Windows before claiming Windows compatibility as tested. A successful package build on Linux is not a Windows runtime test.

## Project layout

- `game/` — Ren'Py scripts, illustrations, audio, GUI, and fonts
- `src/` — existing React website
- `release/windows/` — final Windows game ZIP
- `public/images/` — website artwork and original game illustrations
- `scripts/update-release-size.mjs` — calculates the ZIP size and SHA-256
- `vite.config.js` — copies the real release ZIP into the website build
