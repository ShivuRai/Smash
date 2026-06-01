import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw
import os
import threading

def create_default_icon():
    # Fallback icon if the user hasn't provided one yet
    image = Image.new('RGBA', (64, 64), (255, 255, 255, 0))
    dc = ImageDraw.Draw(image)
    dc.ellipse([0, 0, 64, 64], fill='red')
    return image

class SystemTrayApp:
    def __init__(self, playback_manager, listener):
        self.playback_manager = playback_manager
        self.listener = listener
        self.icon_path = os.path.join('assets', 'icon.ico')
        
        self.is_paused = False
        self.icon = None

    def _get_image(self):
        try:
            # Try png first, then ico
            png_path = os.path.join('assets', 'icon.png')
            if os.path.exists(png_path):
                return Image.open(png_path)
            elif os.path.exists(self.icon_path):
                return Image.open(self.icon_path)
            else:
                return create_default_icon()
        except Exception as e:
            print(f"Failed to load icon: {e}")
            return create_default_icon()

    def set_mode(self, icon, item):
        mode = str(item.text).lower().replace(" mode", "")
        self.playback_manager.set_mode(mode)

    def toggle_pause(self, icon, item):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.listener.stop()
        else:
            self.listener.start()

    def quit_app(self, icon, item):
        self.listener.cleanup()
        self.playback_manager.cleanup()
        icon.stop()

    def create_menu(self):
        modes_menu = pystray.Menu(
            item('Pain Mode', self.set_mode, checked=lambda item: self.playback_manager.get_mode() == 'pain', radio=True),
            item('Sexy Mode', self.set_mode, checked=lambda item: self.playback_manager.get_mode() == 'sexy', radio=True),
            item('Halo Mode', self.set_mode, checked=lambda item: self.playback_manager.get_mode() == 'halo', radio=True),
            item('Custom Mode', self.set_mode, checked=lambda item: self.playback_manager.get_mode() == 'custom', radio=True)
        )

        return pystray.Menu(
            item('Pause/Resume', self.toggle_pause, checked=lambda item: self.is_paused),
            item('Mode', modes_menu),
            pystray.Menu.SEPARATOR,
            item('Quit', self.quit_app)
        )

    def run(self):
        image = self._get_image()
        menu = self.create_menu()
        self.icon = pystray.Icon("Smash", image, "Smash \U0001F4A5", menu)
        self.icon.run()
