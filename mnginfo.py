#! /usr/bin/env python
"""\
Displays information about the MNG file.
"""
if __name__ == "__main__":
	import sys
	import os.path

	if len(sys.argv) != 2 or sys.argv[1] in ("--help", "-h"):
		print __doc__

	fn = sys.argv[1]
	if not os.path.exists(fn):
		print "No such file found...."
		sys.exit(1)
	
	try:
		from mng import MNG
	except ImportError, e:
		print e
		print "The libmng library doesn't appear to work :/"
		sys.exit(1)

	a1 = MNG(sys.argv[1])
	print "filename\t\t",			fn
	print "filesize\t\t",			os.path.getsize(fn), "bytes"
	print "---------------------------------------"
	print "sigtype\t\t\t",			a1.sigtype
	print "type\t\t\t",				a1.type
	print "width\t\t\t",			a1.width, "pixels"
	print "height\t\t\t",			a1.height, "pixels"
	print "ticks\t\t\t",			a1.ticks
	print "framecount\t\t",			a1.framecount
	print "layercount\t\t",			a1.layercount
	print "playtime\t\t",			a1.playtime
	print "simplicity\t\t",			a1.simplicity
	print "bitdepth\t\t",			a1.bitdepth
	print "colortype\t\t",			a1.colortype
	print "compression\t\t",		a1.compression
	print "filter\t\t\t",			a1.filter
	print "interlace\t\t",			a1.interlace
	print "alphabitdepth\t\t",		a1.alphabitdepth
	print "alphacompression\t",		a1.alphacompression
	print "alphafilter\t\t",		a1.alphafilter
	print "alphainterlace\t\t",		a1.alphainterlace

