import os

import pyxel
from PIL import Image

from scene_manager import SceneManager
from font import Font
from network import Network


class App:
    def __init__(self):
        pyxel.init(256, 224, palette=[
            0x000000,
            0x1D2B53,
            0x7E2553,
            0x008751,
            0xAB5236,
            0x5F574F,
            0xC2C3C7,
            0xFFF1E8,
            0xFF004D,
            0xFFA300,
            0xFFEC27,
            0x00E436,
            0x29ADFF,
            0x83769C,
            0xFF77A8,
            0xFFCCAA])
        pyxel.image(0).load(0, 0, os.path.join(os.getcwd(), 'asset/system_neko.bmp'))
        im = Image.open(os.path.join(os.getcwd(), 'asset/font.png'))
        rgb_im = im.convert('RGB')
        self.font = Font(rgb_im)
        self.scene_manager = SceneManager(self)
        self.network = Network()
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.scene_manager.update()
    
    def draw(self):
        self.scene_manager.draw()

App()