"""\
mngdisplay.py <options> <filename>

Tries to displays a mng using a different options.

	-t sdl			Use pygame (ctypes of C version)
	-t pygame		Alias of the above
	-t pygameC		Use the C version of pygame
	-t pygameT		Use the ctypes version of pygame

	-t wx			Use wx
"""


if __name__ == "__main__":
	import sys

	type = None
	for i in range(0, len(sys.argv)):
		arg = sys.argv[i]
		if arg == "-t":
			type = sys.argv[i+1]
			break

	while type == None:
		# Try for pygame
		try:
			import pygame
			type = "pygame"
			break
		except ImportError, e:
			pass

		# O well, maybe wx?
		try:
			import wx
			type = "wx"
			break
		except ImportError, e:
			pass

		break

	if type == "sdl":
		type = "pygame"

	print type
	if type == "pygame":
		import pygame
		screen = pygame.display.set_mode((600, 600), 0, 16) 
		from mng.pygame import MNG

		def input(events): 
			for event in events: 
				if event.type == pygame.QUIT: 
					sys.exit(0) 
				else: 
					print event 

		s = pygame.Surface((1,1)).convert_alpha()
		a = MNG(sys.argv[-1], s)
		while True: 
			screen.fill((0,255,0))

			delay, image = a.nextframe()
			screen.blit(image, (0,0))
			pygame.display.flip()
			input(pygame.event.get())


