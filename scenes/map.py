import pyxel
import numpy as np

import ui
from chara import Usagi
from chara import YUSYA, MAHO_TSUKAI, SOURYO, SENSHI


def copy_ndarray(dest, dx, dy, src, sx=0, sy=0, cw=None, ch=None):
    dh, dw = dest.shape
    sh, sw = src.shape
    cw = cw or sw
    ch = ch or sh

    rx1 = max(max(-dx, 0), max(-sx, 0))
    ry1 = max(max(-dy, 0), max(-sy, 0))
    rx2 = max(max(dx + cw - dw, 0), max(sx + cw - sw, 0))
    ry2 = max(max(dy + ch - dh, 0), max(sy + ch - sh, 0))

    cw -= rx1 + rx2
    ch -= ry1 + ry2

    if cw <= 0 or ch <= 0:
        return False

    dx += rx1
    dy += ry1
    sx += rx1
    sy += ry1
    dest[dy : dy + ch, dx : dx + cw] = src[sy : sy + ch, sx : sx + cw]

    return True


class TilemapHelper:
    '''標準のタイルマップではできないことをする
    
    1. 8*8の扱いを16*16にする。
    2. タイルをX,Y座標で設定できるようにする
    '''

    def __init__(self, tilemap):
        self.tilemap = tilemap

    @staticmethod
    def set_tilemap(tilemap, x, y , data, refimg=None):
        '''
        dataを文字列ではなくて数値で渡せるように改良
        '''
        if refimg is not None:
            tilemap.refimg = refimg
        tilemap.set(x, y, data)
        
    def set_tilemap32(self, x, y, data32, refimg=None):
        "pixelは8だけどこれは16ごとにタイルを扱う"
        data = []
        for line in data32:
            list1 = ''
            list2 = ''
            for e in line:
                r0 = e[0] * 2 + (e[1] * 0x40)
                r1 = (e[0] * 2) + 1 + (e[1] * 0x40)
                r2 = e[0] * 2 + (e[1] * 0x40) + 0x20
                r3 = (e[0] * 2) + 1 + (e[1] * 0x40) + 0x20
                list1 += format(r0, 'x') + format(r1, 'x')
                list2 += format(r2, 'x') + format(r3, 'x')
            data.append(list1)
            data.append(list2)
        TilemapHelper.set_tilemap(self.tilemap, x, y, data, refimg)
        

class Scene:
    def __init__(self):
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
    k = (0,6) # 草
    u = (1,6) # 海
    w = (4,6) # 木の上
    m = (5,6) # 木の中
    f = (6,6) # 木下
    data = [
        [k,k,k,k,k,k,k,k,k,k,k,k,u,u,u,u],
        [k,k,k,k,k,k,k,k,k,k,k,u,u,u,k,k],
        [k,k,k,k,k,k,k,k,k,k,k,u,u,k,k,k],
        [k,k,k,k,k,k,k,k,k,k,k,u,k,k,k,k],
        [k,k,k,k,k,k,k,k,k,k,k,k,k,k,k,k],
        [k,k,k,k,k,k,k,k,k,k,k,k,k,k,k,k],
        [w,w,w,w,w,w,w,k,k,w,w,w,w,w,w,w],
        [m,m,m,m,m,m,m,k,k,m,m,m,m,m,m,m],
        [f,f,f,f,f,f,f,k,k,f,f,f,f,f,f,f],
        [k,k,k,k,k,k,k,k,k,k,k,k,k,k,k,k],
        [k,k,k,k,k,k,k,k,k,k,k,k,k,k,k,k],
        [k,k,k,k,k,k,k,k,k,k,k,k,k,k,k,k],
        [k,k,k,k,k,k,k,k,k,k,k,k,k,k,k,k],
        [k,k,k,k,k,k,k,k,k,k,k,k,k,k,k,k],
    ]
    CANMOVE = (k,)

    def __init__(self):
        import os
        pyxel.image(0).load(0, 0, os.path.join(os.getcwd(), 'asset/system.bmp'))

        # うさぎたち
        self.yusya = Usagi(YUSYA, 2, 4)
        self.soryo = Usagi(SOURYO, 2, 3)
        self.maho_tsukai = Usagi(MAHO_TSUKAI, 2, 2)
        self.senshi = Usagi(SENSHI, 2, 1)
        self.usagii = [
            self.yusya,
            self.soryo,
            self.maho_tsukai,
            self.senshi,
        ]
        #self.target = 0
        self.direct_history = [
            self.usagii[0]._direct,  # privateアクセス良くない
            self.usagii[0]._direct,
            self.usagii[0]._direct,
        ]

        # タイルマップ
        kusa = [[(0,6) for r in range(16)] for v in range(14)]
        self.tilemap_base = TilemapHelper(pyxel.tilemap(0))
        self.tilemap_over = TilemapHelper(pyxel.tilemap(1))
        self.tilemap_base.set_tilemap32(0, 0, kusa, 0)
        self.tilemap_over.set_tilemap32(0, 0, self.data, 0)

        # メッセージ
        self.messagebox = ui.MessageBox(pyxel, 5, 174, 245, 48)
        self.messagebox.put('''みずにははいれないようになりました。'''
        )
        self.messagebox.put('''きもはいれないようになりました''')

        self.messagebox.put('''つぎはマウスでせんたくしたばしょに
        じどうてきにいどうするようにします。''')

        pyxel.mouse(True)
        self.buttons = []
        #self.buttons = [
        #    ui.MessageButton(pyxel, 50, 50, "たたかう", None),
        #    ui.MessageButton(pyxel, 150, 50, "にげる", None)
        #]

    def update(self):
        # スペース押したらメッセージを進める
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.messagebox.next()
        
        # うさぎを切り替えて動かすテスト
        #if pyxel.btnp(pyxel.KEY_C):
        #    self.target += 1

        # mapの先が進めなければ移動させない
        can_move = False
        if pyxel.btn(pyxel.KEY_UP):
            if self.data[self.usagii[0].pos_y - 1][self.usagii[0].pos_x] in self.CANMOVE:
                can_move = True
        elif pyxel.btn(pyxel.KEY_DOWN):
            if self.data[self.usagii[0].pos_y + 1][self.usagii[0].pos_x] in self.CANMOVE:
                can_move = True
        elif pyxel.btn(pyxel.KEY_RIGHT):
            if self.data[self.usagii[0].pos_y][self.usagii[0].pos_x + 1] in self.CANMOVE:
                can_move = True
        elif pyxel.btn(pyxel.KEY_LEFT):
            if self.data[self.usagii[0].pos_y][self.usagii[0].pos_x - 1] in self.CANMOVE:
                can_move = True
        
        if can_move:
            # これはドラクエ歩きのサンプル
            # 1匹だけ入力可にする
            if self.usagii[0].input() and self.usagii[0]._move:
                self.usagii[1]._move = True
                self.usagii[1]._direct = self.direct_history[-1]
                self.usagii[2]._move = True
                self.usagii[2]._direct = self.direct_history[-2]
                self.usagii[3]._move = True
                self.usagii[3]._direct = self.direct_history[-3]
                self.direct_history.append(self.usagii[0]._direct)

        # うさぎたちの位置を全部更新する
        [usagi.update() for usagi in self.usagii]

        [button.update() for button in self.buttons]

    def draw_map_mouse_rect(self):
        if (0 <= pyxel.mouse_x <= 255) and (0 <= pyxel.mouse_y <= 224):
            x = pyxel.mouse_x // 16
            y = pyxel.mouse_y // 16
            if self.data[y][x] in self.CANMOVE:
                pyxel.rect(x * 16, y * 16, 16, 16, 6)
            else:
                pyxel.rect(x * 16, y * 16, 16, 16, 8)

    def draw(self):
        pyxel.cls(0)

        # ベース
        pyxel.bltm(0, 0, 0, 0, 0, 32, 32, 0)
        # タイルを重ねて立体にする
        pyxel.bltm(0, 0, 1, 0, 0, 32, 32, 0)

        # うさぎたちを描く
        [usagi.draw() for usagi in self.usagii]

        # マウスの位置を書く
        self.draw_map_mouse_rect()

        # メッセージボックスを描く
        self.messagebox.draw()

        [button.draw() for button in self.buttons]
    