from ctypes import *

class SDL_PixelFormat(Structure):
    '''Read-only surface format structure.

    :Ivariables:
        `BitsPerPixel` : int
            Number of bits per pixel
        `BytesPerPixel` : int
            Number of bytes per pixel.  This is not necessarily 8 *
            BitsPerPixel.
        `Rloss` : int
            Number of bits lost from an 8-bit red component
        `Gloss` : int
            Number of bits lost from an 8-bit green component
        `Bloss` : int
            Number of bits lost from an 8-bit blue component
        `Aloss` : int
            Number of bits lost from an 8-bit alpha component
        `Rshift` : int
            Number of bits to shift right red component when packing
        `Gshift` : int
            Number of bits to shift right green component when packing
        `Bshift` : int
            Number of bits to shift right blue component when packing
        `Ashift` : int
            Number of bits to shift right alpha component when packing
        `Rmask` : int
            32-bit mask of red component
        `Gmask` : int
            32-bit mask of green component
        `Bmask` : int
            32-bit mask of blue component
        `Amask` : int
            32-bit mask of alpha component
        `colorkey` : int
            Packed transparent color key, if set.
        `alpha` : int
            Surface alpha, in range [0, 255]

    '''
    _fields_ = [('_palette', c_void_p),
                ('BitsPerPixel', c_ubyte),
                ('BytesPerPixel', c_ubyte),
                ('Rloss', c_ubyte),
                ('Gloss', c_ubyte),
                ('Bloss', c_ubyte),
                ('Aloss', c_ubyte),
                ('Rshift', c_ubyte),
                ('Gshift', c_ubyte),
                ('Bshift', c_ubyte),
                ('Ashift', c_ubyte),
                ('Rmask', c_uint),
                ('Gmask', c_uint),
                ('Bmask', c_uint),
                ('Amask', c_uint),
                ('colorkey', c_uint),
                ('alpha', c_ubyte)]

class SDLSurfaceStructure(Structure):
    '''Read-only surface structure.

    :Ivariables:
        `flags` : c_uint
            Pixel format used by this surface
        `format` : c_void_p
            Pixel format used by this surface
        `w` : int
            Width
        `h` : int
            Height
        `pitch` : int
            Number of bytes between consecutive rows of pixel data.  Note
            that this may be larger than the width.
        `pixels` : c_void_p
            Buffer of integers of the type given in the pixel format. 
            Each element of the array corresponds to exactly one pixel
            when ``format.BitsPerPixel`` is 8, 16 or 32; otherwise each
            element is exactly one byte.  Modifying this array has an
            immediate effect on the pixel data of the surface.  See
            `SDL_LockSurface`.
    '''
    _fields_ = [('flags', c_uint),
                ('format', POINTER(SDL_PixelFormat)),
                ('w', c_int),
                ('h', c_int),
                ('pitch', c_short),
                ('pixels', c_void_p)]

# Expand to the correct format depending on the build options
PyObject_HEAD = [
# These are only present when Py_DEBUG was defined at compile time.
#	('_ob_next', c_void_p),
#	('_ob_prev', c_void_p),
	('ob_refcnt', c_int), 
	('_typeobject', c_void_p)
]
class CPygameSurfaceStructure(Structure):
	_fields_ = PyObject_HEAD + [('surf', POINTER(SDLSurfaceStructure))]

class CPygameSurface:
	def __init__(self, surface):
		self.pointer = cast(id(surface), POINTER(CPygameSurfaceStructure))
		
		self.mapping = {}
		for name, type in self.pointer.contents.surf[0]._fields_:
			if type in (c_void_p,):
				self.mapping[name] = type

	def __getattr__(self, key):
		if hasattr(self.pointer.contents.surf[0], key):
#			if key in self.mapping:
#				return self.mapping[key](getattr(self.pointer.contents.surf[0], key))
#			else:
				return getattr(self.pointer.contents.surf[0], key)
		raise KeyError("No such key (%s) exists" % key)

__all__ = [CPygameSurface]
