import pyxel
from scene_manager import SceneManager


class App:
    def __init__(self):
        pyxel.init(255, 224)
        self.scene_manager = SceneManager()
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.scene_manager.update()
    
    def draw(self):
        self.scene_manager.draw()

App()