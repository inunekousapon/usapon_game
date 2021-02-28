import pyxel
import ui


class BaseState:
    def __init__(self, scene, app):
        self.app = app
        self.scene = scene
        self.messagebox = ui.MessageBox(pyxel, self.app.font, 5, 174, 245, 48)
        self.messagebox.put('うさぽんゲーム（仮）', pyxel.COLOR_ORANGE)
        self.messagebox.put('ｖ０．０．４')
        self.buttons = [
            ui.MessageButton(pyxel, self.app.font, 20, 40, "始める", ui.UIEvent(self, self.startgame_event)),
        ]

    def update(self):
        [button.update() for button in self.buttons]

    def draw(self):
        pyxel.cls(0)
        # メッセージボックスを描く
        self.messagebox.draw()
        [button.draw() for button in self.buttons]

    def startgame_event(self, event):
        self.scene.set_state(UpdateState)

    def continuegame_event(self, event):
        print("つづきからはじめる")

    def option_event(self, event):
        print("おぷしょん")


class UpdateState:
    def __init__(self, scene, app):
        self.app = app
        self.scene = scene
        self.select_mode = 0  # 0:none 1:easy 2:normal 3:hard
        self.buttons = [
            ui.MessageButton(pyxel, self.app.font, 30, 60, "文字に色がついたよ", ui.UIEvent(self, self.yes_event, mode=2)),
            ui.MessageButton(pyxel, self.app.font, 105, 110, "戻る", ui.UIEvent(self, self.cancel_event)),
        ]
        self.messagebox = ui.MessageBox(pyxel, self.app.font, 5, 174, 245, 48)
        self.messagebox.put('文字', pyxel.COLOR_PEACH)
        self.messagebox.put('に色を付けることができるようになりました！！')
        self.messagebox.put('\nこんな', pyxel.COLOR_LIME)
        self.messagebox.put('こんな', pyxel.COLOR_LIGHTBLUE)
        self.messagebox.put('こんな', pyxel.COLOR_PURPLE)
        self.messagebox.put('こんな', pyxel.COLOR_RED)
        self.messagebox.put('こんな', pyxel.COLOR_YELLOW)
        self.messagebox.put('文字を書くことができます！できまーす！')

    def update(self):
        if self.select_mode:
            return self.select_mode
        [button.update() for button in self.buttons]
    
    def draw(self):
        pyxel.cls(0)

        # メッセージボックスを描く
        self.messagebox.draw()
        [button.draw() for button in self.buttons]

    def yes_event(self, event, **kwargs):
        self.select_mode = kwargs['mode']

    def cancel_event(self, event):
        self.scene.set_state(BaseState)


class TitleScene:
    def __init__(self, app):
        pyxel.mouse(True)
        self.app = app
        self.state = BaseState(self, self.app)

    def set_state(self, state_cls):
        self.state = state_cls(self, self.app)

    def update(self):
        return self.state.update()

    def draw(self):
        return self.state.draw()
