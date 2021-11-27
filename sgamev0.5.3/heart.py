import pygame
from CONST import *

class Heart(pygame.Rect):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.h = 32
        self.w = 32