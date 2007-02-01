
from ctypes import *

class c_mng_data(Structure):
	_fields_ = [ \
			("_object", c_void_p), 
			("_buffer", c_void_p), 
			("width",  c_long), 
			("height", c_long), 
			("bytesperpixel", c_long),
			("bytesperalpha", c_long)]

	def get_object(self):
		"""\
		Gets the python object this data is associated with...
		"""
		if self._object in (0, None):
			return None
		else:
			return cast(self._object, py_object).value

	def set_object(self, value):
		self._object = py_object(value)
	object = property(get_object, set_object)

c_mng_bool   = c_byte
c_mng_ptr    = c_void_p
c_mng_handle = c_void_p

try:
	# We either use the functions in the _cmnghelper.so or use the much slower python versions.
	_mnghelper = cdll.LoadLibrary("./_mnghelper.so")

	_mnghelper.getcanvasline.argtypes = [c_mng_ptr, c_mng_handle, c_uint32]
	_mnghelper.getcanvasline.restype = c_mng_ptr
	mnggetcanvasline = _mnghelper.getcanvasline

	_mnghelper.getalphaline.argtypes = [c_mng_ptr, c_mng_handle, c_uint32]
	_mnghelper.getalphaline.restype = c_mng_ptr
	mnggetalphaline = _mnghelper.getalphaline

except OSError, e:
	print e
	print "Crap, couldn't find the helper shared library... Will have to use slower totally python method."

	MNGGETCANVASLINE = CFUNCTYPE(c_mng_ptr, c_mng_handle, c_uint32)
	def py_mnggetcanvasline(handle, line):
		data = cast(mng.mng_get_userdata(handle), py_object).value

		p = addressof(data.buffer) + (self.width*line*self.bytesperpixel)
		libc.memset(p, 0, data.width*self.bytesperpixel)

		return buffer
	mnggetcanvasline=MNGGETCANVASLINE(py_mnggetcanvasline)

	MNGGETALPHALINE = CFUNCTYPE(c_mng_ptr, c_mng_handle, c_uint32)
	def py_mnggetalphaline(handle, line):
		data = cast(mng.mng_get_userdata(handle), py_object).value

		p = addressof(data.buffer) + (data.width*data.height*data.bytesperpixel) \
									  + (data.width*line*data.bytesperalpha)
		libc.memset(p, 0, data.width*data.bytesperalpha)

		buffer = data.getalphaline(line)
		return buffer
	mnggetalphaline=MNGGETALPHALINE(py_mnggetalphaline)

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

MNGREFRESH = CFUNCTYPE(c_mng_bool, c_mng_handle, c_uint32, c_uint32, c_uint32, c_uint32)
def py_mngrefresh(handle, x, y, w, h):
	#print "mngrefresh", x, y, w, h
	data = cast(mng.mng_get_userdata(handle), py_object).value
	data.refresh((x,y), (w,h))
	return MNG_TRUE
mngrefresh=MNGREFRESH(py_mngrefresh)

