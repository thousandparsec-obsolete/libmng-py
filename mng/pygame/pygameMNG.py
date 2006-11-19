
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

import pygame

from mng import MNG
from constants import *

RED, GREEN, BLUE, ALPHA = range(0, 4)

class pygameMNG(MNG):
	"""\
	Displays a MNG on a SDL (pygame) surface
	"""
	def __init__(self, file, surface=None):
		# Figure out the best fileformat for the library to output
		if surface is None:
			info = pygame.display.Info()
		else:
			class info:
				pass
			info = info()
			info.bitsize = surface.get_bitsize()
			info.masks = surface.get_masks()
			info.shifts = surface.get_shifts()

		print info.bitsize, info.masks, info.shifts	
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
		self.sdlformat = sdlformat
		MNG.__init__(self, file, format)
		print self.bitsperpixel, self.buffer_size	

#		def processheader(self, width, height):
#			print "SDL processheader", self, self.sdlformat
#			self.initalized = True
#			# Create a buffer which the library will output to
#			self.buffer_size = width*height*self.bitsperpixel/8
#			self.image	 	 = pygame.surface.Surface((width, height), pygame.SRCALPHA)

	def nextframe(self):
#			# Lock the surface
#			self.image.lock()
#			print self.getticks(), self.delay
#			if self.getticks() > self.delay:
#				print "calling display_resume"
#				mng.mng_display_resume(self.mng_handle)
#			self.image.unlock()
#			return d, self.image
		d, buffer = MNG.nextframe(self)
		return d, pygame.image.frombuffer(buffer, self.size, "RGBA") #self.sdlformat)

if __name__ == "__main__":
	import sys
	if len(sys.argv) > 1:
		import pygame
		screen = pygame.display.set_mode((640, 480), 16, 32) 
		pygame.display.set_caption('Battle Viewer') 
		screen.fill((255,255,255))

		a = pygameMNG(sys.argv[1], screen)
		print "sigtype\t\t\t",			a.sigtype
		print "type\t\t\t",				a.type
		print "width\t\t\t",			a.width
		print "height\t\t\t",			a.height
		print "ticks\t\t\t",			a.ticks
		print "framecount\t\t",			a.framecount
		print "layercount\t\t",			a.layercount
		print "playtime\t\t",			a.playtime
		print "simplicity\t\t",			a.simplicity
		print "bitdepth\t\t",			a.bitdepth
		print "colortype\t\t",			a.colortype
		print "compression\t\t",		a.compression
		print "filter\t\t\t",			a.filter
		print "interlace\t\t",			a.interlace
		print "alphabitdepth\t\t",		a.alphabitdepth
		print "alphacompression\t",		a.alphacompression
		print "alphafilter\t\t",		a.alphafilter
		print "alphainterlace\t\t",		a.alphainterlace

		def input(events): 
			for event in events: 
				if event.type == pygame.QUIT: 
					sys.exit(0) 
				else: 
					print event 

		while True: 
			delay, image = a.nextframe()
			screen.blit(image, (0,0))
			pygame.display.flip()
			input(pygame.event.get())

