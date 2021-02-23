import os

import pyxel
from PIL import Image

from scene_manager import SceneManager
from font import Font


class App:
    def __init__(self):
        pyxel.init(255, 224)
        pyxel.image(0).load(0, 0, os.path.join(os.getcwd(), 'asset/system.bmp'))
        im = Image.open(os.path.join(os.getcwd(), 'asset/font.png'))
        rgb_im = im.convert('RGB')
        self.font = Font(rgb_im)
        self.scene_manager = SceneManager(self)
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.scene_manager.update()
    
    def draw(self):
        self.scene_manager.draw()

App()