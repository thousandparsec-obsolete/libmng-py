"""
Extra functionality for accessing the C parts of Python objects.
"""

from ctypes import *

PyObject_HEAD = [
	('ob_refcnt', c_int), 
	('_typeobject', c_void_p)
]

class PyO_Structure(Structure):
	_fields_ = PyObject_HEAD

PyObject_HEAD_debug = [
# These are only present when Py_DEBUG was defined at compile time.
	('_ob_next', c_void_p),
	('_ob_prev', c_void_p),
	('ob_refcnt', c_int), 
	('_typeobject', c_void_p)
]



# Need to figure out if this is a debug build. 
# We are going to do this by looking for ob_refcnt value to be correct.

# Create a dummy object
class Dummy:
	pass

o = Dummy()
# Create a pointer to the object
pointer = cast(id(o), POINTER(PyO_Structure))

while True:
	# Currently their should be 1 reference
	if pointer.contents.ob_refcnt == 1:
		# The ref count should be equal to three after this
		o2 = o
		o3 = o
		if pointer.contents.ob_refcnt == 3:
			# Yay, but to make sure we'll delete 1 refrence
			o3 = None

			# The ref count should be equal to two now
			if pointer.contents.ob_refcnt == 2:
				# Yay!

				# Check the basic size of the object is equal to the object.__basicsize__
				if sizeof(PyO_Structure) == object.__basicsize__:
					__all__ = [PyObject_HEAD]
					break

	# Maybe we are a debug build
	PyO_Structure.__feilds__ = PyObject_HEAD_debug

	# Currently their should be 1 reference
	if pointer.contents.ob_refcnt == 1:
		# The ref count should be equal to three after this
		o2 = o
		o3 = o
		if pointer.contents.ob_refcnt == 3:
			# Yay, but to make sure we'll delete 1 refrence
			o3 = None

			# The ref count should be equal to two now
			if pointer.contents.ob_refcnt == 2:
				# Check the basic size of the object is equal to the object.__basicsize__
				if sizeof(PyO_Structure) == object.__basicsize__:
					print "Debug Python Build"
					# Yay!
					PyObject_HEAD = PyObject_HEAD_debug
					__all__ = [PyObject_HEAD]
					break
	
	raise RuntimeError("Could not figure out PyObject_HEAD")
