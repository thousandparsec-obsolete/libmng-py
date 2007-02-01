"""\

"""

from ctypes.util import find_library
from ctypes import *
pythonapi.PyFile_AsFile.restype = c_void_p

# Try and find a libc library and libmng
import sys
if sys.platform == 'win32':
	# Find a libc like library
	libc = cdll.msvcrt

	# Look in the dll directory
	import os.path
	lib = os.path.join(os.dirname(__file__), "dll", "libmng.dll")
else:
	libc = cdll.LoadLibrary(find_library("c"))
	lib = find_library("mng")

if lib is None:
	raise RuntimeError("Was not able to find a libmng library which I can use.")

# libmng constants...
from constants import *
import mnghelper

mng = cdll.LoadLibrary(lib)
mng.mng_initialize.restype = c_void_p

mng.mng_version_text.restype = c_char_p
mng_version_text	= mng.mng_version_text()

mng.mng_version_so.restype = c_uint8
mng_version_so		= mng.mng_version_so()

mng.mng_version_dll.restype = c_uint8
mng_version_dll		= mng.mng_version_dll()

mng.mng_version_major.restype = c_uint8
mng.mng_version_minor.restype = c_uint8
mng.mng_version_release.restype = c_uint8
mng_version = (mng.mng_version_major(), mng.mng_version_minor(), mng.mng_version_release())

import time

_marker = []
class MNG(object):
	PLAY    = 0
	PAUSING = 1
	PAUSED  = 2

	def __init__(self, file, output=MNG_CANVAS_RGBA8, read=True):
		"""\
		MNG(file, output)

		file   - A file object which can be accessed with the C API (no subclasses or similar)
		output - 
		"""
		print "__init__", file, output, read
		self.file   = open(file, 'rb')
		self.output = output
		self.state  = self.PAUSED

		# Initalise the library

		# Allocate the Data Structure store..
		self.mnghelper = mnghelper.c_mng_data()
		self.mnghelper.object = self
		self.mnghelper.buffer = None
		self.mnghelper.width, self.mnghelper.height = (0,0)
		if isinstance(BITSPERPIXEL[output], (tuple, list)):
			self.mnghelper.bytesperpixel = BITSPERPIXEL[output][0]/8
			self.mnghelper.bytesperalpha = BITSPERPIXEL[output][1]/8
		else:
			self.mnghelper.bytesperpixel = BITSPERPIXEL[output]/8
			self.mnghelper.bytesperalpha = 0

		mng_handle = c_void_p(mng.mng_initialize(byref(self.mnghelper), mnghelper.mngalloc, mnghelper.mngfree, None))

		# Setup the callbacks
		# Dummy callback
		if mng.mng_setcb_openstream(mng_handle, mnghelper.mngopenstream) != 0 or \
				mng.mng_setcb_closestream(mng_handle, mnghelper.mngclosestream) != 0:
			raise RuntimeError("Unable to setup dummy callback for the MNG Library")

		# Callback for data
		if mng.mng_setcb_readdata(mng_handle, mnghelper.mngreaddata) != 0:
			raise RuntimeError("Unable to setup readdata callback for the MNG Library")

		# Callback telling how long has progressed
		if mng.mng_setcb_gettickcount(mng_handle, mnghelper.mnggetticks) != 0:
			raise RuntimeError("Unable to setup tickcount callback for the MNG Library")

		# Called when the library stops doing work, gives the amount of time till the library needs to be called again
		if mng.mng_setcb_settimer(mng_handle, mnghelper.mngsettimer) != 0:
			raise RuntimeError("Unable to setup settimer callback for the MNG Library")

		# Called when the header is processed :P
		if mng.mng_setcb_processheader(mng_handle, mnghelper.mngprocessheader) != 0:
			raise RuntimeError("Unable to setup processheader callback for the MNG Library")
	
		# Called to find the canvas location
		if mng.mng_setcb_getcanvasline(mng_handle, mnghelper.mnggetcanvasline) != 0:
			raise RuntimeError("Unable to setup getcanvasline callback for the MNG Library")

		# Called to find the canvas location
		if mng.mng_setcb_getalphaline(mng_handle, mnghelper.mnggetalphaline) != 0:
			raise RuntimeError("Unable to setup getalphaline callback for the MNG Library")

		# Called to find the location for a background

		# Called to tell the system where the library has updated the canvas 
		if hasattr(self, "refresh"):
			refresh = mnghelper.mngrefresh
		else:
			refresh = mnghelper.mngrefresh_dummy
		if mng.mng_setcb_refresh(mng_handle, refresh) != 0:
			raise RuntimeError("Unable to setup refresh callback for the MNG Library")

		self.mng_handle = mng_handle

		if read:
			self.read()

	def init(self):
		self.time = time.time()
		self.delay = 0

	def read(self):
		self.init()

		# Read in the data.
		mng.mng_readdisplay(self.mng_handle)

	def bytesperpixel(self):
		return self.mnghelper.bytesperpixel
	bytesperpixel = property(bytesperpixel)

	def bytesperalpha(self):
		return self.mnghelper.bytesperalpha
	bytesperalpha = property(bytesperalpha)

	def bytesperboth(self):
		return self.bytesperpixel+self.bytesperalpha
	bytesperboth = property(bytesperboth)

	def get_width(self):
		return self.mnghelper.width
	width = property(get_width)
	def get_height(self):
		return self.mnghelper.height
	hieght = property(get_height)

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
		raise KeyError("No such key %s" % key)

	def processheader(self, width, height):
		"""\
		Called when the header is processed.

		Should set self.initalized to true.
		Should create a buffer to store the image data in.
		Should call mng.mng_set_canvasstyle(self.mng_handle, self.output)
		"""
		print "MNG processheader", width, height

		self.mnghelper.width  = width
		self.mnghelper.height = height
		self.mnghelper.buffer_size = width*height*self.bytesperboth
		if not hasattr(self, 'initalized') or not self.initalized:
			self.initalized = True
	
			# Create a buffer which the library will output to
			self.buffer 	      = c_buffer(self.buffer_size)
			self.mnghelper.buffer = addressof(self._buffer)

		print self.mnghelper
		print id(self), id(self.mnghelper.object)
		print self.mnghelper.buffer
		print self.mnghelper.buffer_size
		print (self.mnghelper.width, self.mnghelper.height)
		print self.mnghelper.bytesperpixel
		print self.mnghelper.bytesperalpha

		# Set the output style of the library
		mng.mng_set_canvasstyle(self.mng_handle, self.output)

	def settimer(self, msec):
		self.delay = self.getticks()+msec

	def getticks(self):
		return int((time.time()-self.time)*1000)

	def display_resume(self):
		"""\
		*Internal Function*
		
		Called to update/move to the next frame.
		"""
		if self.state == self.PLAY:
			mng.mng_display_resume(self.mng_handle)
		else:
			self.state = self.PAUSED
			mng.mng_display_freeze(self.mng_handle)

	def nextframe(self):
		"""\
		Gets the next frame.

		(<delay>, <frame>)
		"""
		#print "nextframe"
		if self.getticks() > self.delay:
			self.display_resume()
		return self.delay-self.getticks(), string_at(self.buffer, self.buffer_size)

	def __str__(self):
		return "<MNG %s (%i, %i)>" % (hex(id(self)), self.width, self.height)

	def pause(self):
		"""\
		Pause the current animation.
		"""
		if self.state != self.PAUSED:
			self.state = self.PAUSING
			
			while self.getticks() < self.delay:
				pass
			self.display_resume()

	def reset(self):
		"""\
		Resets the animation to the start.
		"""
		if self.state == self.PAUSED:
#			print "Resetting!"
			mng.mng_display_reset(self.mng_handle)
#			mng.mng_display_goframe(self.mng_handle, 0)
#			mng.mng_display_gotime(self.mng_handle, 0)
		else:
			raise IOError("The animation has to be paused before you can stop it.")

	def resume(self):
		"""\
		Starts an animation (stopped or never started).
		"""
		print "resume"
		self.state = self.PLAY

		self.init()
		self.display_resume()
	play = resume
	
## Note that the code could be made a lot more user-friendly by using 
## mng_getlasterror to display more details in case libmng reports an error.
