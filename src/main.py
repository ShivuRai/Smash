import os
import sys

# Ensure the working directory is the one containing the assets, even when run via pyinstaller or from another location
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
else:
    application_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.chdir(application_path)

from audio_listener import AudioListener
from playback import PlaybackManager
from system_tray import SystemTrayApp

def main():
    print(f"Starting Smash from {os.getcwd()}...")
    
    # Initialize components
    playback_manager = PlaybackManager(base_dir="assets")
    
    # We pass the playback_manager.play_reaction method as the callback for the DSP listener
    listener = AudioListener(callback=playback_manager.play_reaction)
    
    # Start listening
    listener.start()
    
    # Setup and run system tray (this is a blocking call and keeps the main thread alive)
    tray_app = SystemTrayApp(playback_manager, listener)
    tray_app.run()
    
    print("Smash exited.")

if __name__ == "__main__":
    main()
