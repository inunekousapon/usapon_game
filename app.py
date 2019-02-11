import pyxel
from scenes import title
    

class App:
    def __init__(self):
        pyxel.init(255, 224)

        self.scene = title.TitleScene()
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        self.scene.update()
    
    def draw(self):
        self.scene.draw()

App()