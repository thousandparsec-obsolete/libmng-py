"""\
mngdisplay.py <options> <filename>

Tries to displays a mng using a different options.

	-t sdl			Use pygame (ctypes of C version)
	-t pygame		Alias of the above
	-t pygameC		Use the C version of pygame
	-t pygameT		Use the ctypes version of pygame

	-t wx			Use wx
"""


if __name__ == "__main__":
	import sys

	type = None
	for i in range(0, len(sys.argv)):
		arg = sys.argv[i]
		if arg == "-t":
			type = sys.argv[i+1]
			break

	while type == None:
		# Try for pygame
		try:
			import pygame
			type = "pygame"
			break
		except ImportError, e:
			pass

		# O well, maybe wx?
		try:
			import wx
			type = "wx"
			break
		except ImportError, e:
			pass

		break

	if type == "sdl":
		type = "pygame"

	print type
		

