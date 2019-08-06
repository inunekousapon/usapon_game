import sys


# 表示文字情報(画像と合わせること)
CHARS = '''０１２３４５６７８９、。，．・：；？！　
ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ
ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ
ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただ
ちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむ
めもゃやゅゆょよらりるれろゎわゐゑをん
ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダ
チヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミム
メモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶ
ー―‐／＼〜‖｜…‥‘’“”（）〔〕［］｛｝〈〉《》「」『』【】'''

CHAR_POS = {}
for line_no, line in enumerate(CHARS.split('\n')):
    for index, char in enumerate(line):
        CHAR_POS[char] = (index * 8, line_no * 8)

def display_text(pyxel, x, y, txt):
    for index, s in enumerate(txt):
        if not s in CHAR_POS:
            s = '？'
        pyxel.blt(x + (index * 8), y, 0, CHAR_POS[s][0], CHAR_POS[s][1], 8, 8, 0)


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
    COLOR = 7
    BACKGROUND = 0

    def __init__(self, pyxel, x, y, width, height):
        self.pyxel = pyxel
        self.x = x              # ボックスの左
        self.y = y              # ボックスの上
        self.width = width      # 横幅
        self.height = height    # 高さ
        self.padding_x = 4      # 線からの横padding
        self.padding_y = 4      # 線からの縦padding
        self.queue = []         # ここに積まれている分、文字列を表示する
        self.message = ''       # 今、表示しているメッセージ
        self.frame_count = sys.maxsize  # 最大値入れておいて何がなんでも表示しない

    def put(self, txt):
        'txtに入れた文字列を表示する文字列に登録する'
        self.queue.append(txt)

    def next(self):
        '次に表示する文字列を見せる'
        if self.queue:
            self.frame_count = self.pyxel.frame_count
            self.message = self.queue.pop(0)

    def showall(self):
        if self.queue:
            self.frame_count = -999
            self.message = self.queue.pop(0)

    def draw(self):
        self.pyxel.rect(self.x, self.y, self.width, self.height, MessageBox.BACKGROUND)
        self.pyxel.rectb(self.x, self.y, self.width, self.height, MessageBox.COLOR)

        # 1フレームずつ表示する文字列の長さを変えていく
        str_count = self.pyxel.frame_count - self.frame_count
        if self.message:
            lines = self.message.split('\n')
            for index, line in enumerate(lines):
                line = line.strip()
                display_text(self.pyxel, self.x + self.padding_x, self.y + self.padding_y + index * 10, line[:str_count])
                str_count -= len(line)
                if str_count <= 0:
                    break


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
    def __init__(self, pyxel, x, y, message, callback):
        super().__init__(pyxel, x, y, len(message)* 8, 8, callback)
        self.message = message
        self.padding_x = 8      # 線からの横padding
        self.padding_y = 8      # 線からの縦padding

    def draw(self):
        self.pyxel.rect(self.x, self.y, self.width + (self.padding_x * 2), self.height + (self.padding_y * 2), self.color)
        self.pyxel.rectb(self.x, self.y, self.width + (self.padding_x * 2), self.height + (self.padding_y * 2), Button.BORDER_COLOR)
        if self.message:
            display_text(self.pyxel, self.x + self.padding_x, self.y + self.padding_y, self.message)
