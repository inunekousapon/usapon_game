import sys
from collections import deque


class UIEvent:
    def __init__(self, owner, callback, **kwargs):
        self.owner = owner
        self.callback = callback
        self.kwargs = kwargs

    def call(self, *args, **kwargs):
        kwargs.update(self.kwargs)
        self.callback(self.owner, **kwargs)


class MessageBox:
    'メッセージボックスを表示する'
    BORDER_COLOR = 7
    BACKGROUND = 0
    STRING_COLOR = 7
    LINES = 4
    STRING_NUM = 23

    def __init__(self, pyxel, font, x, y, width, height):
        self.font = font
        self.pyxel = pyxel
        self.x = x              # ボックスの左
        self.y = y              # ボックスの上
        self.width = width      # 横幅
        self.height = height    # 高さ
        self.padding_x = 2      # 線からの横padding
        self.padding_y = 4      # 線からの縦padding
        self.queue = deque()    # ここに積まれている分、文字列を表示する
        self.message = []       # 今、表示しているメッセージ
        self.pre_message = None

    def put(self, txt, color=STRING_COLOR):
        'txtに入れた文字列を表示する文字列に登録する'
        self.queue.extend([(c, color) for c in txt])
        lines = []
        line = deque()
        for c in self.queue:
            if c[0] == '\n':
                lines.append(line.copy())
                line.clear()
                continue
            line.append(c)
            if len(line) > self.STRING_NUM:
                lines.append(line.copy())
                line.clear()
                continue
        else:
            lines.append(line.copy())
        self.message = lines[-4:]
        
    def next(self):
        pass

    def showall(self):
        pass

    def draw(self):
        self.pyxel.rect(self.x, self.y, self.width, self.height, MessageBox.BACKGROUND)
        self.pyxel.rectb(self.x, self.y, self.width, self.height, MessageBox.BORDER_COLOR)

        if self.message:
            if self.pre_message != self.message:
                self.pre_message = self.message
                for i in range(256):
                    for j in range(256):
                        self.pyxel.image(2).data[i][j] = 0
                for index, line in enumerate(self.message):
                    self.font.color_text_flipflop(self.pyxel.image(2), 0, index * 10, line)
            self.pyxel.blt(self.x + self.padding_x, self.y + self.padding_y, 2, 0, 0, self.width - self.padding_x * 2, self.height - self.padding_y * 2)


class MouseEvent:
    def __init__(self, x, y, key):
        self.x = x
        self.y = y
        self.key = key


class Button:
    BORDER_COLOR = 7

    def __init__(self, pyxel, x, y , width, height, callback):
        self.pyxel = pyxel
        self.x = x              # ボックスの左
        self.y = y              # ボックスの上
        self.width = width      # 横幅
        self.height = height    # 高さ
        self.padding_x = 4      # 線からの横padding
        self.padding_y = 4      # 線からの縦padding
        self.color = 0
        self.default_color = 0
        self.hover_color = 5
        self.callback = callback

    def update(self):
        if (self.x <= self.pyxel.mouse_x <= self.x + self.width + (self.padding_x * 2) and
            self.y <= self.pyxel.mouse_y <= self.y + self.height + (self.padding_y * 2)):
            self.color = self.hover_color
            if self.callback and self.pyxel.btn(self.pyxel.MOUSE_LEFT_BUTTON):
                self.callback.call(MouseEvent(self.pyxel.mouse_x, self.pyxel.mouse_y, self.pyxel.MOUSE_LEFT_BUTTON))
        else:
            self.color = self.default_color

    def draw(self):
        pass


class MessageButton(Button):
    def __init__(self, pyxel, font, x, y, message, callback):
        super().__init__(pyxel, x, y, len(message)* 10, 10, callback)
        self.font = font
        self.message = message
        self.padding_x = 8      # 線からの横padding
        self.padding_y = 8      # 線からの縦padding

    def draw(self):
        self.pyxel.rect(self.x, self.y, self.width + (self.padding_x * 2), self.height + (self.padding_y * 2), self.color)
        self.pyxel.rectb(self.x, self.y, self.width + (self.padding_x * 2), self.height + (self.padding_y * 2), Button.BORDER_COLOR)
        if self.message:
            self.font.display_text(self.pyxel, self.x + self.padding_x, self.y + self.padding_y, self.message)
