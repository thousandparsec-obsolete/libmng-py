
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

MNGREADDATA = CFUNCTYPE(c_mng_bool, c_mng_handle, c_mng_ptr, c_uint, POINTER(c_uint32))
def py_mngreaddata(handle, buffer, iSize, iRead):
	data = cast(mng.mng_get_userdata(handle), py_object).value

	iRead[0] = libc.fread(buffer, 1, iSize, pythonapi.PyFile_AsFile(py_object(data['file'])))
	return MNG_TRUE
mngreaddata=MNGREADDATA(py_mngreaddata)

MNGITERCHUNK = CFUNCTYPE(c_mng_bool, c_mng_handle, c_mng_handle, c_uint32, c_uint32)
def py_mngiterchunk(handle, hChunk, iChunktype, iChunkseq):
	data = cast(mng.mng_get_userdata(handle), py_object).value

	aCh = range(0, 4)
	aCh[0] = chr((iChunktype >> 24) & 0xFF)
	aCh[1] = chr((iChunktype >> 16) & 0xFF)
	aCh[2] = chr((iChunktype >>  8) & 0xFF)
	aCh[3] = chr((iChunktype      ) & 0xFF)

	if iChunktype in (MNG_UINT_MEND, MNG_UINT_IEND, MNG_UINT_ENDL):
		data['indent'] -= 2
	print "%s%s" % (" "*data['indent'], "".join(aCh))
	
	if iChunktype in (MNG_UINT_MHDR, MNG_UINT_IHDR, MNG_UINT_JHDR,
			MNG_UINT_DHDR, MNG_UINT_BASI, MNG_UINT_LOOP):
		data['indent'] += 2;

	return MNG_TRUE
mngiterchunk=MNGITERCHUNK(py_mngiterchunk)

def dumptree(file):
	data = {'file': open(file, 'rb'), 'indent': 2}
	
	handle = mng.mng_initialize(py_object(data), mngalloc, mngfree, None)

	if mng.mng_setcb_openstream(handle, mngopenstream) != 0 or \
			mng.mng_setcb_closestream(handle, mngclosestream) != 0:
		raise RuntimeError("Unable to setup dummy callback for the MNG Library")

	if mng.mng_setcb_readdata(handle, mngreaddata) != 0:
		raise RuntimeError("Unable to setup readdata callback for the MNG Library")

	mng.mng_read(handle)

	print "Starting dump of %s.\n" % file
	if mng.mng_iterate_chunks(handle, 0, mngiterchunk) != 0:
		print "Cannot iterate the chunks."
	print "\nDone."

## Note that the code could be made a lot more user-friendly by using 
## mng_getlasterror to display more details in case libmng reports an error.
if __name__ == "__main__":
	import sys
	if len(sys.argv) > 1:
		dumptree(sys.argv[1])
	else:
		print "\n\nUsage: mngtree <file.mng>\n"
	sys.exit(0)

