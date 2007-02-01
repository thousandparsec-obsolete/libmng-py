
from ctypes import *

import pygame
from SDL_Surface import CPygameSurface

from mng import MNG as OriginalMNG
from mng.constants import *

RED, GREEN, BLUE, ALPHA = range(0, 4)

class MNG(OriginalMNG):
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
		OriginalMNG.__init__(self, file, format)

	def processheader(self, width, height):
		self.initalized = True

		# Create a buffer which the library will output to
		self.image = pygame.surface.Surface((width, height)).convert(self.info.masks)
		if self.bitsperpixel != self.image.get_bitsize():
			raise RuntimeError("Created surface (%s) does not have correct bitsize (%s)." % \
				(self.image.get_bitsize(), self.bitsperpixel))
		self.buffer = CPygameSurface(self.image).pixels

		OriginalMNG.processheader(self, width, height)

	def nextframe(self, force=False):
		if self.getticks() > self.delay or force:
			self.display_resume()
		return self.delay, self.image

