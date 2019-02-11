import pyxel
import ui


class TitleScene:
    def __init__(self):
        pyxel.image(0).load(0, 0, 'asset/system.bmp')

        # メッセージ
        self.messagebox = ui.MessageBox(pyxel, 5, 174, 245, 48)
        self.messagebox.put('''うさぽんゲーム　Ｖ１．００
        ''')
        self.messagebox.next()

        pyxel.mouse(True)
        self.buttons = [
            ui.MessageButton(pyxel, 50, 30, "あたらしくはじめる"),
            ui.MessageButton(pyxel, 50, 70, "つづきからはじめる"),
            ui.MessageButton(pyxel, 50, 110, "オプション")
        ]

    def update(self):
        # スペース押したらメッセージを進める
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.messagebox.next()

        [button.update() for button in self.buttons]


    def draw(self):
        pyxel.cls(0)

        # メッセージボックスを描く
        self.messagebox.draw()

        [button.draw() for button in self.buttons]