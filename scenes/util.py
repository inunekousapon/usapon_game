import pyxel
import numpy as np
from pyxel.tilemap import copy_ndarray


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