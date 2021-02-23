from PIL import Image, ImageFont, ImageDraw
import pyxel
import string

class Font:
    WIDTH = 1450
    def __init__(self, file, size, alphabet):
        import numpy as np
        self.file = file
        self.size = size
        self.alphabet = alphabet

        px_w, px_h = size
        # pt_w, pt_h = (int(n * 0.75) for n in meta['size']) # 96 dpi
        ## load custom font
        font = ImageFont.truetype(file, size=px_h) # it must be pt_h, but px_h brings better result
        img = Image.new('1', size=(self.WIDTH, self.WIDTH))
        draw = ImageDraw.Draw(img)
        coords = {}
        x, y = 0, 0
        for c in alphabet:
            if x + px_w > self.WIDTH:
                x = 0
                y += px_h
            draw.text((x, y), c, font=font, fill=1)
            coords[c] = (x, y)
            x += px_w
        self.coords = coords
        self.img = img
        self.data = np.array(img.getdata()).reshape(self.WIDTH, self.WIDTH)


def draw_font(img, font, col=7):
    img_bank = pyxel.image(img)
    for y in range(256):
        for x in range(256):
            img_bank.set(x, y, col if font.data[y][x] else 0) 

def text(font, x, y, s):
    w, h = font.size
    left = x

    for ch in s:
        if ch == '\n':
            x = left
            y += h
            continue

        if ch == ' ':
            x += w
            continue
        
        if ch in font.coords.keys():
            u, v = font.coords[ch]
            pyxel.blt(x, y, 0, u, v, w, h, 0)
        x += w


def update():
    pass

def draw():
    pyxel.cls(0)
    text(font, 0, 0, """
    あいうえおかきくけこ！
    今です。
    戦士です。""".strip())

pyxel.init(255, 255, caption="よくある手法で外部フォント")

fontfile = 'asset/JF-Dot-MPlus10.ttf'
letter_size = (10, 10)
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
font = Font(fontfile, letter_size, alphabet)
draw_font(0, font)
font.img.save('asset/font.png', 'png')
