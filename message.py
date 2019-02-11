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

    def draw(self):
        self.pyxel.rect(self.x, self.y, self.x + self.width, self.y + self.height, MessageBox.BACKGROUND)
        self.pyxel.rectb(self.x, self.y, self.x + self.width, self.y + self.height, MessageBox.COLOR)

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