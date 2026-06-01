import os
import random
import pygame

class PlaybackManager:
    def __init__(self, base_dir="assets"):
        self.base_dir = base_dir
        self.modes = ["pain", "sexy", "halo", "custom"]
        self.current_mode = "pain"
        
        # Initialize pygame mixer for audio playback
        # We use a frequency of 44100, 16-bit, 2 channels, and a small buffer to reduce latency
        pygame.mixer.pre_init(44100, -16, 2, 512)
        pygame.mixer.init()

    def set_mode(self, mode):
        if mode in self.modes:
            self.current_mode = mode
            print(f"Mode set to: {mode}")

    def get_mode(self):
        return self.current_mode

    def _get_random_sound_from_dir(self, directory):
        full_path = os.path.join(self.base_dir, directory)
        if not os.path.exists(full_path):
            return None
        
        files = [f for f in os.listdir(full_path) if f.lower().endswith(('.mp3', '.wav', '.ogg'))]
        if not files:
            return None
            
        return os.path.join(full_path, random.choice(files))

    def play_reaction(self):
        sound_file = self._get_random_sound_from_dir(self.current_mode)

        if sound_file and os.path.exists(sound_file):
            try:
                sound = pygame.mixer.Sound(sound_file)
                # Force play on channel 0 exclusively. This ensures any currently playing sound is immediately stopped before the new one starts.
                pygame.mixer.Channel(0).play(sound)
            except Exception as e:
                print(f"Error playing sound {sound_file}: {e}")
        else:
            print(f"No valid sound found for mode: {self.current_mode} in folder {os.path.join(self.base_dir, self.current_mode)}")

    def cleanup(self):
        pygame.mixer.quit()
