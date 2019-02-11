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
            ui.MessageButton(pyxel, 50, 30, "あたらしくはじめる", ui.UIEvent(self.startgame_event)),
            ui.MessageButton(pyxel, 50, 70, "つづきからはじめる", ui.UIEvent(self.continuegame_event)),
            ui.MessageButton(pyxel, 50, 110, "オプション", ui.UIEvent(self.option_event))
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
        self.buttons = [
            ui.MessageButton(pyxel, 30, 60, "ふつう", ui.UIEvent(self.yes_event)),
            ui.MessageButton(pyxel, 100, 60, "むずかしい", ui.UIEvent(self.yes_event)),
            ui.MessageButton(pyxel, 190, 60, "むり", ui.UIEvent(self.yes_event)),
            ui.MessageButton(pyxel, 105, 110, "もどる", ui.UIEvent(self.cancel_event)),
        ]
        self.messagebox = ui.MessageBox(pyxel, 5, 174, 245, 48)
        self.messagebox.put('''なんいどをせんたくしてください。
        ふつう：さいしょからなかまをやとうことができます。
        むずかしい：モンスターがつよく、しょじきんがすくないです。
        むり：モンスターがとてもつよく、しょじきんがありません。''')
        self.messagebox.showall()

    def update(self):
        [button.update() for button in self.buttons]
    
    def draw(self):
        pyxel.cls(0)

        # メッセージボックスを描く
        self.messagebox.draw()
        [button.draw() for button in self.buttons]

    def yes_event(self, event):
        pass

    def cancel_event(self, event):
        self.scene.set_state(BaseState)


class TitleScene:
    def __init__(self):
        pyxel.image(0).load(0, 0, 'asset/system.bmp')
        pyxel.mouse(True)
        self.state = BaseState(self)

    def set_state(self, state_cls):
        self.state = state_cls(self)

    def update(self):
        self.state.update()

    def draw(self):
        self.state.draw()
