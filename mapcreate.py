import random
import math

from PIL import Image, ImageDraw
from scipy.spatial import distance


SIZE = 256

SEA = 0
SAND = 1
GRASS = 2
HILL = 3
MOUNTAIN = 4


BIOMES = (SEA, SAND, GRASS, HILL, MOUNTAIN)
WEIGHT1 = ( 0,  5,  0, 40, 55)
WEIGHT2 = ( 5,  5, 25, 40, 25)
WEIGHT3 = ( 5,  0, 50, 25, 20)
WEIGHT4 = (10, 10, 70,  0,  0)
WEIGHT5 = (40, 40, 20,  0,  0)

COLORS = {
    SEA: (0x00, 0x00, 0xFF),
    SAND: (0xFA, 0xEB, 0xD7),
    GRASS: (0x00, 0xFF, 0x00),
    HILL: (0xD2, 0xB4, 0x8C),
    MOUNTAIN: (0xC0, 0xC0, 0xC0),
}


def create_biome(size):
    height = width = size
    matrix = [[0] * width for i in range(height)]
    # for row in range(len(matrix)//5, len(matrix) - len(matrix)//5):
    #     for col in range(len(matrix[row])//5, len(matrix[row]) - len(matrix[row])//5):
    #         matrix[row][col] = random.choice(BIOMES)

    for i in range(36):
        print(f"box生成:{i}/36")
        b_h = int(random.uniform(height * 0.15, height * 0.25))
        b_w = int(random.uniform(width * 0.15, width * 0.25))
        p_h = int(random.uniform(height * 0.2, height * 0.8))
        p_w = int(random.uniform(width * 0.2, width * 0.8))
        for row in range(p_h-b_h//2, p_h+b_h//2):
            for col in range(p_w-b_w//2, p_w+b_w//2):
                d = int(distance.euclidean((col, row), (size//2, size//2)))
                r = d / (size // 2)
                if r < 0.2:
                    w = WEIGHT1
                elif r < 0.4:
                    w = WEIGHT2
                elif r < 0.6:
                    w = WEIGHT3
                elif r < 0.8:
                    w = WEIGHT4
                elif r < 1.0:
                    w = WEIGHT5
                matrix[row][col] = random.choices(BIOMES, weights=w)[0]

    for i in range(100):
        print(f"地形重ね:{i}/100")
        for row in range(1, len(matrix)-1):
            for col in range(1, len(matrix[row])-1):
                case = random.choice(range(4))
                if case == 0: matrix[row][col] = matrix[row][col-1]
                elif case == 1: matrix[row][col] = matrix[row][col+1]
                elif case == 2: matrix[row][col] = matrix[row-1][col]
                elif case == 3: matrix[row][col] = matrix[row+1][col]
    return matrix


img = Image.new('RGB', (SIZE, SIZE), 'blue')
draw = ImageDraw.Draw(img)


for row, cols in enumerate(create_biome(SIZE)):
    for col, color in enumerate(cols):
        img.putpixel((col, row), COLORS[color])

img.show()