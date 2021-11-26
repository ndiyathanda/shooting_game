import pygame
from CONST import *

class Boss(pygame.Rect):
    def __init__(self,x,y,hp):
        self.x = x
        self.y = y
        self.h = 64
        self.w = 64
        self.hp = 10

    def move(self):
        self.x -= BOSS_SPEED