import pyxel
import ui


class BaseState:
    def __init__(self, scene):
        self.scene = scene
        self.messagebox = ui.MessageBox(pyxel, 5, 174, 245, 48)
        self.messagebox.put('''うさぽんゲーム（かり）　Ｖ０．０１''')
        self.messagebox.showall()
        self.buttons = [
            ui.MessageButton(pyxel, 20, 40, "はじめる", ui.UIEvent(self, self.startgame_event)),
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
    def __init__(self, scene):
        self.scene = scene
        self.select_mode = 0  # 0:none 1:easy 2:normal 3:hard
        self.buttons = [
            ui.MessageButton(pyxel, 50, 60, "ＰＹＸＥＬ　Ｖ１．４１にたいおう", ui.UIEvent(self, self.yes_event, mode=2)),
            ui.MessageButton(pyxel, 105, 110, "もどる", ui.UIEvent(self, self.cancel_event)),
        ]
        self.messagebox = ui.MessageBox(pyxel, 5, 174, 245, 48)
        self.messagebox.put('''タイルマップのしょりをかえました。
        がぞうのいろがかわってしまったきがします。
        リリースノートをよんでしゅうせいしないとだめですね。。
        また、いどうできないちけいにはいけないようにしました。''')
        self.messagebox.showall()

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
    def __init__(self):
        import os
        pyxel.image(0).load(0, 0, os.path.join(os.getcwd(), 'asset/system.bmp'))
        pyxel.mouse(True)
        self.state = BaseState(self)

    def set_state(self, state_cls):
        self.state = state_cls(self)

    def update(self):
        return self.state.update()

    def draw(self):
        return self.state.draw()
