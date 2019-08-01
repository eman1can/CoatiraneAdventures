import math, random, sys
import pygame
from pygame.locals import *
from PIL import Image, ImageTk


# exit the program
# def events():
#     for event in pygame.event.get():
#         if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
#             pygame.quit()
#             sys.exit()


# # define display surface
# W, H = 500, 500
# HW, HH = W / 2, H / 2
# AREA = W * H
#
# # initialise display
# pygame.init()
# CLOCK = pygame.time.Clock()
# DS = pygame.display.set_mode((W, H))
# pygame.display.set_caption("code.Pylet - Sprite Sheets")
# FPS =60
# SpriteFPS = 10
#
# # define some colors
# BLACK = (0, 35, 0, 255)
# WHITE = (255, 255, 255, 255)


class spritesheet:
    def __init__(self, filename, cols, rows):
        pygame.init()
        DS = pygame.display.set_mode((500, 500))

        #self.sheet = pygame.image.load(filename).convert_alpha()

        self.cols = cols
        self.rows = rows
        self.totalCellCount = cols * rows

        #self.rect = self.sheet.get_rect()
        #w = self.cellWidth = self.rect.width / cols
        #h = self.cellHeight = self.rect.height / rows
        # for index in range(self.totalCellCount):
        #     print("Index:" + str(index))
        #     print("Column: " + str(math.floor(index % cols)))
        #     print("Row: " + str(math.floor(index / cols)))
        #
        # self.cells = list([(math.floor(index % cols) * w, math.floor(index / cols) * h, 64, 64) for index in range(self.totalCellCount)])


    def draw(self, surface, cellIndex, x, y):
        #print(str(self.cells[cellIndex]))
        surface.create_image(x, y, image = self.sheet, tags = "sprite")
        surface.tag_raise("sprite")
        #surface.blit(self.sheet, (250 + x, 250 + y), self.cells[cellIndex])
        print("drawn")


# s = spritesheet("res/sprites.png", 13, 21) # 118
# Walk left 118-126
# Walk forwards 132-139
# Walk right 152-144
# index = 118
# index2 = 132
# index3 = 145
# index4 = 104
# main loop
# while True:
#     events()
#     if (index == 126):
#         index = 118
#     if (index2 == 139):
#         index2 = 132
#     if (index3 == 152):
#         index3 = 144
#     if (index4 == 113):
#         index4 = 104
#     s.draw(DS, index % s.totalCellCount, -50, 0)
#     s.draw(DS, index2 % s.totalCellCount, 0, 0)
#     s.draw(DS, index3 % s.totalCellCount, 50, 0)
#     s.draw(DS, index4 % s.totalCellCount, 0, -100)
#     print("Sprite " + str(index))
#     index += 1
#     index2 += 1
#     index3 += 1
#     index4 += 1
#
#     pygame.display.update()
#     CLOCK.tick(SpriteFPS)
#     DS.fill(BLACK)
