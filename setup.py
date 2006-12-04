#!/usr/bin/env python

import shutil
import sys

import glob
import os.path

from setuptools import setup

from mng import version
version = ("%s.%s.%s" % version) 
print "Version is %s" % version

arguments = dict(
# Meta data
	name		= "libmng-py",
	version		= version,
	license		= "GPL",
	description	= "libmng for displaying MNG and JNG animations",
	author		= "Tim Ansell",
	author_email= "mithro@mithis.com",
	url			= "http://www.thousandparsec.net/repos/libmng-py",
# Files to include
	scripts=["mngtree.py", "mngdisplay.py", "mnginfo.py"],
	packages=[ \
		'mng',
		'mng.pygame',
		'mng.wx',
		'mng.utils',
	],
	data_files=[(".",	("LICENSE", "COPYING", "README", "TODO"))],
	zip_safe=False,
)

if sys.platform == "win32":
	arguments['data_files'].append((os.path.join("mng", "dll"), "libmng.dll"))

setup(**arguments)
