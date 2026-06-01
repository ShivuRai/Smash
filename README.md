# Smash 💥

Smash is a background Windows utility that listens to your laptop's internal microphone and detects when you physically strike or slap the laptop chassis, playing a customized audio reaction while completely ignoring human speech and background noise.

## Features
- **Intelligent DSP Filtering:** Uses a 3000Hz High-Pass Filter and rolling amplitude envelopes to specifically isolate structure-borne noise (slaps) from airborne noise (talking).
- **Multiple Modes:** Pain Mode, Sexy Mode, Halo Mode, and Custom Mode.
- **System Tray Integration:** Runs silently in the background with a clean right-click menu near your clock.
- **Interruption Playback:** Hitting the laptop rapidly will instantly interrupt the previous sound so it doesn't become a messy overlapping echo.

## How to Install and Run
1. Ensure Python is installed on your system.
2. Place your sound files (`.mp3`, `.wav`) in the `assets/pain/`, `assets/sexy/`, `assets/halo/`, or `assets/custom/` folders.
3. Place an icon for the system tray as `assets/icon.png`.
4. Double click `build.bat` to compile this project into a standalone executable.
5. Run `scripts/install.bat` as Administrator to automatically start the app silently every time Windows boots.

## Adjusting Sensitivity
If you find that the app triggers when typing, or fails to trigger when slapped, you can adjust the DSP thresholds in `src/audio_listener.py`:
- `PEAK_THRESHOLD`: How loud the slap must be. Increase this number (e.g. to 20000) if typing triggers it. Decrease it if you have to hit the laptop too hard.
- `QUIET_THRESHOLD`: The baseline background volume. The app ensures it was "quiet" before the slap.

Enjoy!
