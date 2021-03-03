import string


class Font:
    def __init__(self, font_img):
        self.font_img = font_img
        self.img_data = self.font_img.getdata()
        self.size = (10, 10)
        self.image_size = (1450, 1450)
        ascii_chars = string.punctuation + string.digits + string.ascii_letters
        記号１ = r"　、。，．・：；？！゛゜´｀¨＾‾＿ヽヾゝゞ〃仝々〆〇ー—‐／＼〜‖｜…‥‘’“”（）〔〕［］｛｝〈〉《》「」『』【】＋−±×÷＝≠＜＞≦≧∞∴♂♀°′″℃￥＄￠￡％＃＆＊＠§☆★○●◎◇"
        記号２ = "".join(chr(c) for c in range(ord('◆'), ord('◯')+1))+"ー"
        全角数字 = "".join(chr(c) for c in range(ord('０'), ord('９')+1))
        全角英大文字 = "".join(chr(c) for c in range(ord('Ａ'), ord('Ｚ')+1))
        全角英小文字 = "".join(chr(c) for c in range(ord('ａ'), ord('ｚ')+1))
        ひらがな = "".join(chr(c) for c in range(ord('ぁ'), ord('ゔ')+1))+"ー"
        カタカナ = "".join(chr(c) for c in range(ord('ァ'), ord('ヶ')+1))+"ー"
        漢字 = "".join(chr(c) for c in range(ord('亜'), ord('龠') + 1))
        alphabet = ascii_chars + 記号１ + 記号２ + 全角数字 + 全角英大文字 + 全角英小文字 + ひらがな + カタカナ + 漢字
        self.char_pos = {}
        for i, s in enumerate(alphabet):
            self.char_pos[s] = (
                self.size[0] * i % self.image_size[0],
                (((self.size[1] * i) // self.image_size[1]) * self.size[1]) + 1
            )

    def display_text(self, pyxel, x, y, txt):
        for index, s in enumerate(txt):
            if not s in self.char_pos:
                s = '？'
            for i in range(10):
                for j in range(9):
                    r,g,b = self.font_img.getpixel((self.char_pos[s][0]+i, self.char_pos[s][1]+j))
                    if r == g == b == 255:
                        pyxel.pset(x + (index * 10) + i, y + j, pyxel.COLOR_WHITE)

    def display_color_text(self, pyxel, x, y, tc):
        for index, (s, color) in enumerate(tc):
            if not s in self.char_pos:
                s = '？'
            for i in range(10):
                for j in range(9):
                    r,g,b = self.img_data[(self.char_pos[s][1] + j) * self.image_size[0] + self.char_pos[s][0] + i]
                    if r == g == b == 255:
                        pyxel.pset(x + (index * 10) + i, y + j, color)

    def color_text_flipflop(self, image, x, y, tc):
        for index, (s, color) in enumerate(tc):
            if not s in self.char_pos:
                s = '？'
            for i in range(10):
                for j in range(9):
                    r,g,b = self.img_data[(self.char_pos[s][1] + j) * self.image_size[0] + self.char_pos[s][0] + i]
                    if r == g == b == 255:
                        image.data[y + j][x + (index * 10) + i] = color
