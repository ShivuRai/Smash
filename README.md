# Smash 💥

Smash is a Windows tray utility that listens to the default microphone for short, loud impacts and plays a sound from the selected folder. Detection uses a 31-tap high-pass FIR filter, a recent quiet-window check, and a 750 ms cooldown. Results depend on your microphone, room noise, and sensitivity settings; speech and typing may still trigger it.

## Features

- Four selectable sound folders: Pain, Sexy, Halo, and Custom.
- Tray menu to switch modes, pause listening, and quit.
- New reactions replace audio playing on the dedicated mixer channel.
- Runs locally; the current code does not send microphone audio to a server.

## Requirements

- Windows and Python with `py` available.
- A working default microphone and audio output.
- Dependencies listed in `requirements.txt`.

## Run from source

1. Clone this repository and open a terminal in its root.
2. Run `py -m pip install -r requirements.txt`.
3. Add your own licensed `.mp3`, `.wav`, or `.ogg` files to `assets/pain/`, `assets/sexy/`, `assets/halo/`, or `assets/custom/`. Empty folders produce no sound.
4. Run `py src/main.py`. Use the tray icon to switch modes or quit.

The app looks for `assets/icon.png` or `assets/icon.ico`; if neither exists, it draws a default red icon.

## Build a Windows executable

Run `build.bat` from the repository root. It installs PyInstaller and builds `Smash.exe` beside the script. Keep your `assets` folders beside the executable. To start it on login, run `scripts/install.bat`; this adds an entry under your **current user's** Windows Run key. `scripts/uninstall.bat` removes that entry and stops the process. Administrator access is not required for this per-user startup entry.

## Sensitivity and limitations

Edit `PEAK_THRESHOLD` and `QUIET_THRESHOLD` in `src/audio_listener.py` before building. A larger peak threshold makes triggering harder. Detection is heuristic, not a reliable distinction between a chassis impact and other loud sounds. The current implementation logs start and trigger events to `smash_debug.log` and may remain in the tray if microphone initialization fails; check that log if no reactions play. Avoid striking hardware hard enough to damage it.

## Contributing

Please open an issue with your Windows version, microphone type, reproduction steps, and relevant error text (remove any personal information first). Pull requests should explain the change and how it was tested. Linux support has been requested but is not implemented.

## Media and licensing

The repository currently contains bundled audio clips whose redistribution rights have not been verified. **Do not assume the audio assets are available under a software license.** A code-only distribution with user-supplied or expressly licensed sounds is being prepared. Do not redistribute the bundled clips as part of a release without confirming their rights.
