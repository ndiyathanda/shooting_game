import pygame
from CONST import *

class Blow(pygame.Rect):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.h = 12
        self.w = 12
