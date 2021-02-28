import pyxel
import numpy as np

import ui
from chara import Usagi
from chara import YUSYA


class Scene:
    def __init__(self, app):
        # ロード処理
        pass

    def draw(self):
        # シーン内のブツを描画する
        pass

    def update(self):
        # 処理を行う
        pass

    def change_scene(self, next_scene, anim):
        # シーンを切り替える
        pass


class TestScene(Scene):

    # うさぎを切り替えて動かす用
    # TARGET=(0, 1, 2, 3) 

    # とりあえず直値でタイルを指定
    k = (0,0) # 草
    u = (1,0) # 海
    w = (4,0) # 木の上
    m = (5,0) # 木の中
    f = (6,0) # 木下
    h = (7,0) # 丘
    b = (8,0) # 山
    s = (9,0) # 砂
    CANMOVE = (k,s,h)

    MAP2DATA = {
        "0": u,
        "1": s,
        "2": k,
        "3": h,
        "4": b,
    }

    def __init__(self, app):
        self.app = app

        # マップの読み込み
        with open('asset/map.data', "r") as fp:
            self.data = []
            for line in fp:
                row = []
                for c in line:
                    if c == '\n':
                        break
                    row.append(self.MAP2DATA[c])
                self.data.append(row)

        # うさぎ
        self.you = Usagi(self, YUSYA, 350, 350)

        # メッセージ
        self.messagebox = ui.MessageBox(pyxel, self.app.font, 5, 174, 245, 48)
        self.messagebox.put('''きもちぃぃーーーーー！！！'''
        )

        pyxel.mouse(True)
        self.buttons = []

    def update(self):
        # スペース押したらメッセージを進める
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.messagebox.next()
    
        self.you.input()
        self.you.update()

        [button.update() for button in self.buttons]

    def draw_map(self):
        for y, row in enumerate(self.data[self.you.pos_y - 6:self.you.pos_y + 10], start=-1):
            for x, col in enumerate(row[self.you.pos_x - 9:self.you.pos_x + 9], start=-1):
                pyxel.blt(
                    x * 16 - self.you._x_delta,
                    y * 16 - self.you._y_delta,
                    0,
                    col[0] * 16,
                    col[1] * 16,
                    16,
                    16,
                    0)

    def draw(self):
        pyxel.cls(0)

        # マップを描く
        self.draw_map()

        # うさぎたちを描く
        self.you.draw()
        
        # メッセージボックスを描く
        self.messagebox.draw()

        [button.draw() for button in self.buttons]
    