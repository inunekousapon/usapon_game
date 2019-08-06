import pyxel
import ui


class BaseState:
    def __init__(self, scene):
        self.scene = scene
        self.messagebox = ui.MessageBox(pyxel, 5, 174, 245, 48)
        self.messagebox.put('''うさぽんゲーム　Ｖ１．００
        ''')
        self.messagebox.showall()
        self.buttons = [
            ui.MessageButton(pyxel, 50, 30, "あたらしくはじめる", ui.UIEvent(self, self.startgame_event)),
            ui.MessageButton(pyxel, 50, 70, "つづきからはじめる", ui.UIEvent(self, self.continuegame_event)),
            ui.MessageButton(pyxel, 50, 110, "オプション", ui.UIEvent(self, self.option_event))
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
            ui.MessageButton(pyxel, 30, 60, "ふつう", ui.UIEvent(self, self.yes_event, mode=1)),
            ui.MessageButton(pyxel, 100, 60, "むずかしい", ui.UIEvent(self, self.yes_event, mode=2)),
            ui.MessageButton(pyxel, 190, 60, "むり", ui.UIEvent(self, self.yes_event, mode=3)),
            ui.MessageButton(pyxel, 105, 110, "もどる", ui.UIEvent(self, self.cancel_event)),
        ]
        self.messagebox = ui.MessageBox(pyxel, 5, 174, 245, 48)
        self.messagebox.put('''なんいどをせんたくしてください。
        ふつう：さいしょからなかまをやとうことができます。
        むずかしい：モンスターがつよく、しょじきんがすくないです。
        むり：モンスターがとてもつよく、しょじきんがありません。''')
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
