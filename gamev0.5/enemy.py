import pygame
from CONST import *

class Enemy(pygame.Rect):
    def __init__(self,x,y,type):
        self.x = x
        self.y = y
        self.h = 32
        self.w = 32
        self.type = str(type)
        self.direction = 'left'

    def move(self):
        self.x -= ENEMY_SPEED
