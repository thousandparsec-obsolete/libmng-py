
from ctypes import *

class c_mng_data(Structure):
	_fields_ = [ \
			("_object",       c_void_p), 
			("buffer",        c_void_p), 
			("buffer_size",   c_int), 
			("height",        c_int), 
			("width",         c_int), 
			("bytesperpixel", c_int),
			("bytesperalpha", c_int)]

	def get_object(self):
		"""\
		Gets the python object this data is associated with...
		"""
		if self._object in (0, None):
			return None
		else:
			return cast(self._object, py_object).value

	def set_object(self, value):
		self._object = cast(id(value), c_void_p)
	object = property(get_object, set_object)
c_mng_data_p = POINTER(c_mng_data)

# Try and find a libc library and libmng
import sys
from ctypes.util import find_library
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

pythonapi.PyFile_AsFile.restype = c_void_p

# Setup the libc
libc.calloc.restype = c_void_p
libc.calloc.argtypes = [c_int, c_int]
libc.fread.restype = c_uint32
libc.fread.argtypes = [c_void_p, c_uint32, c_uint32, c_void_p]

# libmng constants...
from mng.constants import *

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

mng.mng_get_userdata.restype = c_mng_data_p

c_mng_bool   = c_byte
c_mng_ptr    = c_void_p
c_mng_handle = c_void_p

try:
	import os.path
	path = os.path.join(os.path.split(__file__)[0], "_mnghelper.so")
	print path

	# We either use the functions in the _cmnghelper.so or use the much slower python versions.
	_mnghelper = cdll.LoadLibrary(path)

	_mnghelper.getcanvasline.argtypes = [c_mng_ptr, c_mng_handle, c_uint32]
	_mnghelper.getcanvasline.restype = c_mng_ptr
	mnggetcanvasline = _mnghelper.getcanvasline

	_mnghelper.getalphaline.argtypes = [c_mng_ptr, c_mng_handle, c_uint32]
	_mnghelper.getalphaline.restype = c_mng_ptr
	mnggetalphaline = _mnghelper.getalphaline

	mngalloc = _mnghelper.mngalloc
	mngfree  = _mnghelper.free
	mngrefresh_dummy = _mnghelper.mngrefresh_dummy

except OSError, e:
	print e
	print "Crap, couldn't find the helper shared library... Will have to use slower totally python method."

	MNGGETCANVASLINE = CFUNCTYPE(c_mng_ptr, c_mng_handle, c_uint32)
	def py_mnggetcanvasline(handle, line):
		#print "py_mnggetcanvasline", line
		data = mng.mng_get_userdata(handle).contents

		p = data.buffer + (data.width*line*data.bytesperpixel)
		libc.memset(p, 0, data.width*data.bytesperpixel)

		return p
	mnggetcanvasline=MNGGETCANVASLINE(py_mnggetcanvasline)

	MNGGETALPHALINE = CFUNCTYPE(c_mng_ptr, c_mng_handle, c_uint32)
	def py_mnggetalphaline(handle, line):
		data = mng.mng_get_userdata(handle).contents

		p = data.buffer + (data.width*data.height*data.bytesperpixel) \
									  + (data.width*line*data.bytesperalpha)
		libc.memset(p, 0, data.width*data.bytesperalpha)

		return p
	mnggetalphaline=MNGGETALPHALINE(py_mnggetalphaline)

	##############################################################################
	# Memory allocation and dummy functions
	#
	# FIXME: Should be able to remove these some how?
	##############################################################################
	MNGALLOC = CFUNCTYPE(c_mng_ptr, c_int)
	def py_mngalloc(i):
		#print "py_mngalloc", i
		p = libc.calloc(1, i)
		return p
	mngalloc = MNGALLOC(py_mngalloc)

	MNGFREE = CFUNCTYPE(None, c_mng_ptr, c_int)
	def py_mngfree(ptr, i):
		#print "py_mngfree", ptr, i
		libc.free(ptr)
		return
	mngfree = MNGFREE(py_mngfree)

	MNGREFRESHDUMMY = CFUNCTYPE(c_mng_bool, c_mng_handle, c_uint32, c_uint32, c_uint32, c_uint32)
	def py_mngrefresh_dummy(handle, x, y, w, h):
		return MNG_TRUE
	mngrefresh_dummy=MNGREFRESHDUMMY(py_mngrefresh_dummy)

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
	data = mng.mng_get_userdata(handle).contents.object

	iRead[0] = libc.fread(buffer, 1, iSize, pythonapi.PyFile_AsFile(py_object(data.file)))
	return MNG_TRUE
mngreaddata=MNGREADDATA(py_mngreaddata)

MNGGETTICKS = CFUNCTYPE(c_uint32, c_mng_handle)
def py_mnggetticks(handle):
	#print "mnggetticks"
	data = mng.mng_get_userdata(handle).contents.object
	return data.getticks()
mnggetticks=MNGGETTICKS(py_mnggetticks)

MNGSETTIMER = CFUNCTYPE(c_mng_bool, c_mng_handle, c_uint32)
def py_mngsettimer(handle, msec):
	#print "mngsettimer", msec
	data = mng.mng_get_userdata(handle).contents.object
	data.settimer(msec)
	return MNG_TRUE
mngsettimer=MNGSETTIMER(py_mngsettimer)

MNGPROCESSHEADER = CFUNCTYPE(c_mng_bool, c_mng_handle, c_uint32, c_uint32)
def py_mngprocessheader(handle, width, height):
	#print "mngprocessheader", width, height
	data = mng.mng_get_userdata(handle).contents.object
	data.processheader(width, height)
	return MNG_TRUE
mngprocessheader=MNGPROCESSHEADER(py_mngprocessheader)

MNGREFRESH = CFUNCTYPE(c_mng_bool, c_mng_handle, c_uint32, c_uint32, c_uint32, c_uint32)
def py_mngrefresh(handle, x, y, w, h):
	#print "mngrefresh", x, y, w, h
	data = mng.mng_get_userdata(handle).contents.object
	data.refresh((x,y), (w,h))
	return MNG_TRUE
mngrefresh=MNGREFRESH(py_mngrefresh)

