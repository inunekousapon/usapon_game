import pyxel
from scene import TestScene
    

class App:
    def __init__(self):
        pyxel.init(255, 224)

        self.scene = TestScene()
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.scene.update()
    
    def draw(self):
        self.scene.draw()

App()