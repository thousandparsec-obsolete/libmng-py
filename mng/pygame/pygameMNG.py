
from ctypes import *

import pygame
from SDL_Surface import CPygameSurface

from mng import MNG
from constants import *

RED, GREEN, BLUE, ALPHA = range(0, 4)

class pygameMNG(MNG):
	"""\
	Displays a MNG on a SDL (pygame) surface
	"""
	def __init__(self, file, surface=None):
		# Figure out the best fileformat for the library to output
		class info:
			def __str__(self):
				return "<Info b:%s m:%s s:%s l:%s>" % (self.bitsize, self.masks, self.shifts, self.losses)

		info = info()
		if surface is None:
			i = pygame.display.Info()
			info.masks = i.masks
			info.shifts = i.shifts
			info.losses = i.losses

			info.bitsize = i.bitsize
			# FIXME: Sometimes the screen info lies
			if info.masks[-1] == 0:
				info.bitsize -= 8
		else:
			info.bitsize = surface.get_bitsize()
			info.masks   = list(surface.get_masks())
			info.shifts  = surface.get_shifts()
			info.losses  = surface.get_losses()

		print info
		self.info = info

		if info.bitsize == 32:
			if info.masks[ALPHA] == 0:
				# No alpha (padding byte) 
				if info.shifts[BLUE] == 0:
					format = MNG_CANVAS_BGRX8
					sdlformat = "BGRX"
				else:
					# Red first
					print "No matching mng canvas for sdl pixel format. Colors may be wrong."
					format = MNG_CANVAS_BGRX8
					sdlformat = "BGRX"
			else:
				# Real alpha
				if info.shifts[BLUE] == 0:
					# Blue first
					format = MNG_CANVAS_BGRA8
					sdlformat = "BGRA"
				else:
					# Red first
					format = MNG_CANVAS_RGBA8
					sdlformat = "RGBA"
		elif info.bitsize == 24:
			if info.masks[ALPHA] == 0:
				# No alpha here should mean true rgb24bit
				if info.shifts[BLUE] == 0:
					# Blue first
					format = MNG_CANVAS_BGR8
					sdlformat = "BGR"
				else:
					# Red first
					format = MNG_CANVAS_RGB8
					sdlformat = "RGB"
			else:
				# If there is an alpha and we are in 24 bpp, this must mean rgb5658
				if info.shifts[BLUE] == 0:
					# Blue first
					format = MNG_CANVAS_BGRA565
					sdlformat = "BGRA"
				else:
					# Red first
					format = MNG_CANVAS_RGBA565
					sdlformat = "RGBA"
		elif info.bitsize == 16:
			if info.shifts[BLUE] == 0:
				# Blue first
				format = MNG_CANVAS_BGR565
				sdlformat = "RGB"
			else:
				# Red first
				format = MNG_CANVAS_RGB565
				sdlformat = "RGB"
		else:
			raise RuntimeError("Unable to figure out the best format for this video file.")

		print "Detected image format to be", NAMESPERPIXEL[format], sdlformat
		MNG.__init__(self, file, format)

	def getcanvasline(self, line):
		p = self.buffer + (self.width*line*self.bitsperpixel/8)
		return p

	def processheader(self, width, height):
		self.initalized = True

		# Create a buffer which the library will output to
		self.image = pygame.surface.Surface((width, height)).convert(self.info.masks)
		if self.bitsperpixel != self.image.get_bitsize():
			raise RuntimeError("Created surface (%s) does not have correct bitsize (%s)." % \
				(self.image.get_bitsize(), self.bitsperpixel))
		self.buffer = CPygameSurface(self.image).pixels

		MNG.processheader(self, width, height)

	def nextframe(self, force=False):
		if self.getticks() > self.delay or force:
			# FIXME: Would memset be faster?
			self.image.fill((0,0,0,0)) 
			self.display_resume()
		return self.delay, self.image

if __name__ == "__main__":
	import sys

	if len(sys.argv) > 1:
		import pygame
		screen = pygame.display.set_mode((800, 600), 0, 16) 
		pygame.display.set_caption('Battle Viewer') 
		screen.fill((255,0, 0))

		p = pygame.image.load("../../temp/barren/barren1_000.png").convert_alpha()

		print
#		s1 = pygame.surface.Surface((100,100), pygame.SRCALPHA).convert_alpha()
#		print "Original BitsPerPixel", s1.get_bitsize()
#		a1 = pygameMNG(sys.argv[1], s1)
		print "---------------------------------------------------------"
		print
#		s2 = pygame.surface.Surface((100,100)).convert()
#		print "Original BitsPerPixel", s2.get_bitsize()
#		a2 = pygameMNG(sys.argv[1], s2)
#		print "---------------------------------------------------------"
#		print
		a1 = pygameMNG(sys.argv[1], p)
#		print "---------------------------------------------------------"
#		print

		print "sigtype\t\t\t",			a1.sigtype
		print "type\t\t\t",				a1.type
		print "width\t\t\t",			a1.width
		print "height\t\t\t",			a1.height
		print "ticks\t\t\t",			a1.ticks
		print "framecount\t\t",			a1.framecount
		print "layercount\t\t",			a1.layercount
		print "playtime\t\t",			a1.playtime
		print "simplicity\t\t",			a1.simplicity
		print "bitdepth\t\t",			a1.bitdepth
		print "colortype\t\t",			a1.colortype
		print "compression\t\t",		a1.compression
		print "filter\t\t\t",			a1.filter
		print "interlace\t\t",			a1.interlace
		print "alphabitdepth\t\t",		a1.alphabitdepth
		print "alphacompression\t",		a1.alphacompression
		print "alphafilter\t\t",		a1.alphafilter
		print "alphainterlace\t\t",		a1.alphainterlace

		def input(events): 
			for event in events: 
				if event.type == pygame.QUIT: 
					sys.exit(0) 
				else: 
					print event 

		while True: 
			screen.fill((0,255,0))

			delay, image = a1.nextframe()
			screen.blit(image, (0,0))
			screen.blit(p, (129, 0))

			pygame.display.flip()
			input(pygame.event.get())

