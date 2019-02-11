import pyxel
import numpy as np

from pyxel.tilemap import copy_ndarray

from message import MessageBox
from chara import Usagi
from chara import YUSYA, MAHO_TSUKAI, SOURYO, SENSHI


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
        copy_ndarray(tilemap._data, x, y, np.array(data))
    
    def set_tilemap32(self, x, y, data32, refimg=None):
        "pixelは8だけどこれは16ごとにタイルを扱う"
        data = []
        for line in data32:
            list1 = []
            list2 = []
            for e in line:
                r0 = e[0] * 2 + (e[1] * 0x40)
                r1 = (e[0] * 2) + 1 + (e[1] * 0x40)
                r2 = e[0] * 2 + (e[1] * 0x40) + 0x20
                r3 = (e[0] * 2) + 1 + (e[1] * 0x40) + 0x20
                list1.append(r0)
                list1.append(r1)
                list2.append(r2)
                list2.append(r3)
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

    def __init__(self):
        pyxel.image(0).load(0, 0, 'asset/system.bmp')

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
        self.messagebox = MessageBox(pyxel, 5, 174, 245, 48)
        self.messagebox.put('''メッセージは　スペースキーを　おすと　つぎのぶんしょうを
        みることができるよ！！'''
        )
        self.messagebox.put('''こんなふうにね！！
        
        はやくいろいろためさないといけない。'''
        )

    def update(self):
        # スペース押したらメッセージを進める
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.messagebox.next()
        
        # うさぎを切り替えて動かすテスト
        #if pyxel.btnp(pyxel.KEY_C):
        #    self.target += 1

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

    def draw(self):
        pyxel.cls(0)

        # ベース
        pyxel.bltm(0, 0, 0, 0, 0, 32, 32, 0)
        # タイルを重ねて立体にする
        pyxel.bltm(0, 0, 1, 0, 0, 32, 32, 0)

        # うさぎたちを描く
        [usagi.draw() for usagi in self.usagii]

        # メッセージボックスを描く
        self.messagebox.draw()
    