import pyxel


class Charactor():
    def __init__(self):
        pass
    
    def update(self):
        pass

    def draw(self):
        pass


MAHO_TSUKAI = (
    (5, 8), # 背中
    (3, 8), # 正面
    (6, 8), # 左
    (6, 8), # 右
)

SOURYO = (
    (3, 10), # 背中
    (1, 10), # 正面
    (4, 10), # 左
    (4, 10), # 右
)

YUSYA = (
    (2, 11), # 背中
    (1, 11), # 正面
    (3, 11), # 左
    (3, 11), # 右
)

SENSHI = (
    (2, 12), # 背中
    (1, 12), # 正面
    (3, 12), # 左
    (3, 12), # 右
)


class Usagi(Charactor):
    def __init__(self, target, x, y):
        self.pos_x = x
        self.pos_y = y

        self.img = target
        self._move = False
        self._direct = 1    # 0:背面 1:正面 2:左 3:右
        self._move_px = 3   # 1フレームに動くピクセル数
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
            print("x: {}".format(self.pos_x))
            print("y: {}".format(self.pos_y))
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
        
        if pyxel.btn(pyxel.KEY_UP):
            self._direct = 0
            if self.pos_y > 0:
                self._move = True
            return pyxel.KEY_UP
        elif pyxel.btn(pyxel.KEY_DOWN):
            self._move = True
            self._direct = 1
            return pyxel.KEY_DOWN
        elif pyxel.btn(pyxel.KEY_RIGHT):
            self._direct = 3
            self._move = True
            return pyxel.KEY_RIGHT
        elif pyxel.btn(pyxel.KEY_LEFT):
            self._direct = 2
            if self.pos_x > 0:
                self._move = True
            return pyxel.KEY_LEFT
        return None

    def draw(self):
        pyxel.blt(
            self.pos_x * 16 + self._x_delta,
            self.pos_y * 16 + self._y_delta,
            0,
            self.img[self._direct][0] * 16, self.img[self._direct][1] * 16,
            (-1 if self._direct == 2 else 1) * 16, 16, 0)