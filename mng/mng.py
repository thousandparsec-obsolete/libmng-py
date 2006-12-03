"""\

"""

from ctypes.util import find_library
from ctypes import *
pythonapi.PyFile_AsFile.restype = c_void_p

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

# Setup the libc
libc.calloc.restype = c_void_p
libc.calloc.argtypes = [c_int, c_int]
libc.fread.restype = c_uint32
libc.fread.argtypes = [c_void_p, c_uint32, c_uint32, c_void_p]

from constants import *
mng = cdll.LoadLibrary(lib)
mng.mng_initialize.restype = c_void_p

mng.mng_version_text.restype = c_char_p
mng_version_text	= mng.mng_version_text()
print mng_version_text

mng.mng_version_so.restype = c_uint8
mng_version_so		= mng.mng_version_so()
print mng_version_so

mng.mng_version_dll.restype = c_uint8
mng_version_dll		= mng.mng_version_dll()
print mng_version_dll

mng.mng_version_major.restype = c_uint8
mng.mng_version_minor.restype = c_uint8
mng.mng_version_release.restype = c_uint8
mng_version = (mng.mng_version_major(), mng.mng_version_minor(), mng.mng_version_release())
print mng_version

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

import time

_marker = []
class MNG:
	def __init__(self, file, output=MNG_CANVAS_RGBA8, read=True):
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

		if read:
			self.read()

	def read(self):
		self.time = time.time()*1000
		self.delay = 0

		# Read in the data.
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
		print "MNG processheader", width, height
		if hasattr(self, 'initalized') and not self.initalized:
			self.initalized = True
	
			# Create a buffer which the library will output to
			self.buffer_size = width*height*self.bitsperpixel/8
			self.buffer 	 = c_buffer(self.buffer_size)

		# Set the output style of the library
		mng.mng_set_canvasstyle(self.mng_handle, self.output)

	def settimer(self, msec):
		self.delay = self.getticks()+msec

	def refresh(self, pos, size):
		#print self, "refresh", pos, size
		pass

	def getticks(self):
		return int(time.time()*1000-self.time)

	def getcanvasline(self, line):
		return addressof(self.buffer) + (self.width*line*self.bitsperpixel/8)

	def display_resume(self):
		"""\
		*Internal Function*
		
		Called to update/move to the next frame.
		"""
		mng.mng_display_resume(self.mng_handle)

	def nextframe(self, force=False):
		"""\
		Gets the next frame.

		(<delay>, <frame>)
		"""
		#print self.getticks(), self.delay
		if self.getticks() > self.delay or force:
			self.display_resume()
		return self.delay, string_at(self.buffer, self.buffer_size)

	def __str__(self):
		return "<MNG %s (%i, %i)>" % (hex(id(self)), self.width, self.height)

	def stop(self):
		"""\
		Stops the current animation.
		"""
		mng.mng_display_freeze(self.mng_handle)

	def resume(self):
		"""\
		Resumes a stopped animation.
		"""
		mng.mng_display_resume(self.mng_handle)
		

## Note that the code could be made a lot more user-friendly by using 
## mng_getlasterror to display more details in case libmng reports an error.
