
from ctypes import *

import pygame
screen = pygame.display.set_mode((640, 480), 16, 16) 
pygame.display.set_caption('Battle Viewer') 
screen.fill((255,255,255))

s1 = pygame.surface.Surface((100,100))

from SDL_Surface import CPygameSurface
s = CPygameSurface(s1)

print s.flags
print s.format
print s.w
print s.h
print s.pitch
print s.pixels
