import pygame
from CONST import *

class Player(pygame.Rect):
    def __init__(self):
        self.x = 0
        self.y = 150
        self.h = 32
        self.w = 32
        self.hp = 3

    def check_player(self):
        if self.y<=0:
            self.y = 10
        if self.y>=180:
            self.y = 160