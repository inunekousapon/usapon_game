from scenes.title import TitleScene
from scenes.map import TestScene


class SceneManager:
    SCENES = [TitleScene, TestScene]

    def __init__(self, app):
        self.app = app
        self.index = 0
        self.current = SceneManager.SCENES[self.index](self.app)

    def update(self):
        if self.current.update():
            self.next_scene()

    def draw(self):
        self.current.draw()

    def next_scene(self):
        self.index += 1
        self.current = SceneManager.SCENES[self.index](self.app)
