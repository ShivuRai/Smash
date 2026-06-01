@echo off
echo Installing PyInstaller just in case...
py -m pip install pyinstaller
echo Building Smash...
py -m PyInstaller --onefile --windowed --name Smash src\main.py
if exist dist\Smash.exe (
    move /Y dist\Smash.exe .
    rmdir /S /Q build
    rmdir /S /Q dist
    del Smash.spec
    echo Build complete! Smash.exe is now in the current directory.
) else (
    echo Build failed. See output above.
)
pause
