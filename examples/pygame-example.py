import pygame
screen = pygame.display.set_mode((300, 300), 0, 16) 
screen.fill((255,0, 0))

import sys

from mng.pygame import MNG
s = pygame.Surface((1,1)).convert_alpha()

a1 = MNG("barren-alpha-full.mng", s)
a2 = MNG("barren-alpha-1bit.mng", s)

def input(events): 
	for event in events: 
		if event.type == pygame.QUIT: 
			sys.exit(0) 
		else: 
			print event 

a1.play()
a2.play()

while True: 
	screen.fill((0,255,0))

	delay, image = a1.nextframe()
	screen.blit(image, (0,0))
	delay, image = a2.nextframe()
	screen.blit(image, (129,0))

	pygame.display.flip()
	input(pygame.event.get())
