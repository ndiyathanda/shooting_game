import pygame
from CONST import *

class Projectile(pygame.Rect):
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.h = 12
        self.w = 12
        self.type=str(type)

    def move(self):
        if self.type == "1" or self.type == "3":
            self.x += PROJECTILE_SPEED
        else:
            self.x -= PROJECTILE_SPEED
