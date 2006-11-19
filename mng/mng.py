
import time

from ctypes import *
libc = cdll.LoadLibrary("libc.so.6")
libc.calloc.restype = c_void_p
libc.calloc.argtypes = [c_int, c_int]
libc.fread.restype = c_uint32
libc.fread.argtypes = [c_void_p, c_uint32, c_uint32, c_void_p]
pythonapi.PyFile_AsFile.restype = c_void_p

from constants import *
mng = cdll.LoadLibrary("libmng.so.1.1.0.9")
mng.mng_initialize.restype = c_void_p

#mng_version_text = c_byte.in_dll(mng, "mng_version_text")
#print mng_version_text, repr(mng_version_text)
#mng_version_so = c_uint8.in_dll(mng, "mng_version_so")
#print mng_version_so
#mng_version_dll = c_uint8.in_dll(mng, "mng_version_dll")
#print mng_version_dll
#mng_version_major = c_uint8.in_dll(mng, "mng_version_major")
#print mng_version_major

c_mng_bool   = c_byte
c_mng_ptr    = c_void_p
c_mng_handle = c_void_p

##############################################################################
# Memory allocation and dummy functions
#
# FIXME: Should be able to remove these some how?
##############################################################################
MNGALLOC = CFUNCTYPE(c_mng_ptr, c_int)
def py_mngalloc(i):
	p = libc.calloc(1, i)
	return p
mngalloc = MNGALLOC(py_mngalloc)

MNGFREE = CFUNCTYPE(None, c_mng_ptr, c_int)
def py_mngfree(ptr, i):
	libc.free(ptr)
	return
mngfree = MNGFREE(py_mngfree)

MNGOPENSTREAM = CFUNCTYPE(c_mng_bool, c_mng_handle)
def py_mngopenstream(handle):
	return MNG_TRUE
mngopenstream = MNGOPENSTREAM(py_mngopenstream)

MNGCLOSESTREAM = CFUNCTYPE(c_mng_bool, c_mng_handle)
def py_mngclosestream(handle):
	return MNG_TRUE
mngclosestream = MNGCLOSESTREAM(py_mngclosestream)
##############################################################################


##############################################################################
# Supply data to the library from a file.
#
# FIXME: This should be changed to support any filetype object (IE StringIO)
##############################################################################
MNGREADDATA = CFUNCTYPE(c_mng_bool, c_mng_handle, c_mng_ptr, c_uint, POINTER(c_uint32))
def py_mngreaddata(handle, buffer, iSize, iRead):
	#print "mngreaddata", iSize
	data = cast(mng.mng_get_userdata(handle), py_object).value

	iRead[0] = libc.fread(buffer, 1, iSize, pythonapi.PyFile_AsFile(py_object(data.file)))
	return MNG_TRUE
mngreaddata=MNGREADDATA(py_mngreaddata)

MNGGETTICKS = CFUNCTYPE(c_uint32, c_mng_handle)
def py_mnggetticks(handle):
	#print "mnggetticks"
	data = cast(mng.mng_get_userdata(handle), py_object).value
	return data.getticks()
mnggetticks=MNGGETTICKS(py_mnggetticks)

MNGSETTIMER = CFUNCTYPE(c_mng_bool, c_mng_handle, c_uint32)
def py_mngsettimer(handle, msec):
	#print "mngsettimer", msec
	data = cast(mng.mng_get_userdata(handle), py_object).value
	data.settimer(msec)
	return MNG_TRUE
mngsettimer=MNGSETTIMER(py_mngsettimer)

MNGPROCESSHEADER = CFUNCTYPE(c_mng_bool, c_mng_handle, c_uint32, c_uint32)
def py_mngprocessheader(handle, width, height):
	#print "mngprocessheader", width, height
	data = cast(mng.mng_get_userdata(handle), py_object).value
	data.processheader(width, height)
	return MNG_TRUE
mngprocessheader=MNGPROCESSHEADER(py_mngprocessheader)

MNGGETCANVASLINE = CFUNCTYPE(c_mng_ptr, c_mng_handle, c_uint32)
def py_mnggetcanvasline(handle, line):
	#print "mnggetcanvasline", line
	data = cast(mng.mng_get_userdata(handle), py_object).value

	buffer = data.getcanvasline(line)
	return buffer
mnggetcanvasline=MNGGETCANVASLINE(py_mnggetcanvasline)

MNGREFRESH = CFUNCTYPE(c_mng_bool, c_mng_handle, c_uint32, c_uint32, c_uint32, c_uint32)
def py_mngrefresh(handle, x, y, w, h):
	#print "mngrefresh", x, y, w, h
	data = cast(mng.mng_get_userdata(handle), py_object).value
	data.refresh((x,y), (w,h))
	return MNG_TRUE
mngrefresh=MNGREFRESH(py_mngrefresh)

_marker = []
class MNG:
	def __init__(self, file, output=MNG_CANVAS_RGBA8):
		"""\
		MNG(file, output)

		file   - A file object which can be accessed with the C API (no subclasses or similar)
		output - 
		"""
		self.file   = open(file, 'rb')
		self.output = output

		# Initalise the library
		mng_handle = c_void_p(mng.mng_initialize(py_object(self), mngalloc, mngfree, None))

		# Setup the callbacks
		# Dummy callback
		if mng.mng_setcb_openstream(mng_handle, mngopenstream) != 0 or \
				mng.mng_setcb_closestream(mng_handle, mngclosestream) != 0:
			raise RuntimeError("Unable to setup dummy callback for the MNG Library")

		# Callback for data
		if mng.mng_setcb_readdata(mng_handle, mngreaddata) != 0:
			raise RuntimeError("Unable to setup readdata callback for the MNG Library")

		# Callback telling how long has progressed
		if mng.mng_setcb_gettickcount(mng_handle, mnggetticks) != 0:
			raise RuntimeError("Unable to setup tickcount callback for the MNG Library")

		# Called when the library stops doing work, gives the amount of time till the library needs to be called again
		if mng.mng_setcb_settimer(mng_handle, mngsettimer) != 0:
			raise RuntimeError("Unable to setup settimer callback for the MNG Library")

		# Called when the header is processed :P
		if mng.mng_setcb_processheader(mng_handle, mngprocessheader) != 0:
			raise RuntimeError("Unable to setup processheader callback for the MNG Library")
	
		# Called to find the canvas location
		if mng.mng_setcb_getcanvasline(mng_handle, mnggetcanvasline) != 0:
			raise RuntimeError("Unable to setup getcanvasline callback for the MNG Library")

		# Called to find the location for a background
		#getbkgdline

		# Called to tell the system where the library has updated the canvas 
		if mng.mng_setcb_refresh(mng_handle, mngrefresh) != 0:
			raise RuntimeError("Unable to setup refresh callback for the MNG Library")

		self.mng_handle = mng_handle

		self.time = time.time()*1000
		self.delay = 0

		# Get the 
		mng.mng_readdisplay(self.mng_handle)

	def bitsperpixel(self):
		return BITSPERPIXEL[self.output]
	bitsperpixel = property(bitsperpixel)

	def size(self):
		"""
		Size of the image in width, height format.
		"""
		return (self.width, self.height)
	size = property(size)

	def __getattr__(self, key, default=_marker):
		f = "mng_get_" + key
		if hasattr(mng, f):
			return getattr(mng, f)(self.mng_handle)
		f = "mng_get_image" + key
		if hasattr(mng, f):
			return getattr(mng, f)(self.mng_handle)
		if default is _marker:
			raise KeyError("No such key %s" % key)

	def processheader(self, width, height):
		"""\
		Called when the header is processed.

		Should set self.initalized to true.
		Should create a buffer to store the image data in.
		Should call mng.mng_set_canvasstyle(self.mng_handle, self.output)
		"""
		print "MNG processheader"
		self.initalized = True

		# Create a buffer which the library will output to
		self.buffer_size = width*height*self.bitsperpixel/8
		self.buffer 	 = c_buffer(self.buffer_size)

		# Set the output style of the library
		mng.mng_set_canvasstyle(self.mng_handle, self.output)

	def settimer(self, msec):
		#print self, "settimer", msec
		self.delay = self.getticks()+msec
		pass

	def refresh(self, pos, size):
		#print self, "refresh", pos, size
		pass

	def getticks(self):
		return int(time.time()*1000-self.time)

	def getcanvasline(self, line):
		return addressof(self.buffer) + (self.width*line*self.bitsperpixel/8)

	def nextframe(self):
		"""\
		Gets the next frame.

		(<delay>, <frame>)
		"""
		print self.getticks(), self.delay
		if self.getticks() > self.delay:
			print "calling display_resume"
			mng.mng_display_resume(self.mng_handle)
		return self.delay, self.buffer

	def __str__(self):
		return "<MNG %s (%i, %i)>" % (hex(id(self)), self.width, self.height)

try:
	import pygame

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
			return d, pygame.image.frombuffer(string_at(buffer, self.buffer_size), self.size, self.sdlformat)

except ImportError:
	pass

## Note that the code could be made a lot more user-friendly by using 
## mng_getlasterror to display more details in case libmng reports an error.
if __name__ == "__main__":
	import sys
	if len(sys.argv) > 1:
		import pygame
		screen = pygame.display.set_mode((640, 480), 16, 16) 
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
	else:
		print "\n\nUsage: mngtree <file.mng>\n"
	sys.exit(0)

