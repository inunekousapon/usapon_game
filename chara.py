from dataclasses import dataclass
from typing import Tuple

import pyxel


class Charactor():
    def __init__(self):
        pass
    
    def update(self):
        pass

    def draw(self):
        pass


@dataclass
class CharactorImages:
    stand_images: Tuple[Tuple[int, int]]
    work_images: Tuple[Tuple[Tuple[int, int]]]

YUSYA = (
    (2, 5), # 背中
    (1, 5), # 正面
    (3, 5), # 左
    (3, 5), # 右
)

MAGICIAN = CharactorImages(
    stand_images=(
        (1, 3), # 背中
        (0, 3), # 正面
        (2, 3), # 左
        (2, 3), # 右
    ),
    work_images=(
        ((6,3), (7,3)), # 背中
        ((4,3), (5,3)), # 正面
        ((8,3), (9,3)), # 左
        ((8,3), (9,3)), # 右
    )
)

CLERIC = CharactorImages(
    stand_images=(
        (1, 4), # 背中
        (0, 4), # 正面
        (2, 4), # 左
        (2, 4), # 右
    ),
    work_images=(
        ((6,4), (7,4)), # 背中
        ((4,4), (5,4)), # 正面
        ((8,4), (9,4)), # 左
        ((8,4), (9,4)), # 右
    )
)

HERO = CharactorImages(
    stand_images=(
        (1, 5), # 背中
        (0, 5), # 正面
        (2, 5), # 左
        (2, 5), # 右
    ),
    work_images=(
        ((6,5), (7,5)), # 背中
        ((4,5), (5,5)), # 正面
        ((8,5), (9,5)), # 左
        ((8,5), (9,5)), # 右
    )
)

FIGHTER = CharactorImages(
    stand_images=(
        (1, 6), # 背中
        (0, 6), # 正面
        (2, 6), # 左
        (2, 6), # 右
    ),
    work_images=(
        ((6,6), (7,6)), # 背中
        ((4,6), (5,6)), # 正面
        ((8,6), (9,6)), # 左
        ((8,6), (9,6)), # 右
    )
)


class Usagi(Charactor):
    def __init__(self, map_scene, target, x, y):
        self.map_scene = map_scene
        self.pos_x = x
        self.pos_y = y

        self.target = target
        self._move = False
        self._direct = 1    # 0:背面 1:正面 2:左 3:右
        self._move_px = 2   # 1フレームに動くピクセル数
        self._move_delta = 0    # 移動したピクセル数
        self._x_delta = 0       # 移動した横方向のピクセル数
        self._y_delta = 0       # 移動した縦方向のピクセル数

    def move(self):
        self._move_delta += self._move_px
        if self._move_delta > 16:
            self._move = False
            self._move_delta = 0
            if self._direct == 0:
                self.pos_y -= 1
            elif self._direct == 1:
                self.pos_y += 1
            elif self._direct == 2:
                self.pos_x -= 1
            elif self._direct == 3:
                self.pos_x += 1
        if self._direct == 0:
            self._y_delta = -1 * self._move_delta
        elif self._direct == 1:
            self._y_delta = self._move_delta
        elif self._direct == 2:
            self._x_delta = -1 * self._move_delta
        elif self._direct == 3:
            self._x_delta = self._move_delta

    def update(self):
        if self._move:
            self.move()
            return

    def input(self):
        if self._move:
            return None
        
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
            self._direct = 0
            if self.map_scene.data[self.pos_y - 1][self.pos_x] not in self.map_scene.CANMOVE:
                return None
            if self.pos_y > 0:
                self._move = True
            return pyxel.KEY_UP
        elif pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            self._direct = 1
            if self.map_scene.data[self.pos_y + 1][self.pos_x] not in self.map_scene.CANMOVE:
                return None
            self._move = True
            return pyxel.KEY_DOWN
        elif pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self._direct = 3
            if self.map_scene.data[self.pos_y][self.pos_x + 1] not in self.map_scene.CANMOVE:
                return None
            self._move = True
            return pyxel.KEY_RIGHT
        elif pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self._direct = 2
            if self.map_scene.data[self.pos_y][self.pos_x - 1] not in self.map_scene.CANMOVE:
                return None
            if self.pos_x > 0:
                self._move = True
            return pyxel.KEY_LEFT
        return None

    def draw(self):
        image = self.target.stand_images[self._direct]
        if self._move_delta > 0:
            if self._direct in (0, 1):
                image = self.target.work_images[self._direct][self.pos_y % 2]
            else:
                image = self.target.work_images[self._direct][self.pos_x % 2]

        pyxel.blt(
            8 * 16,
            5 * 16,
            0,
            image[0] * 16, image[1] * 16,
            (-1 if self._direct == 2 else 1) * 16, 16, 0
        )
