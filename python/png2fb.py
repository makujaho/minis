#!/usr/bin/python2

# converts a picture to framebuffer.

import sys

try:
	infile = sys.argv[1]
	outfile = sys.argv[2]
except:
	print "Usage: %s <input> <output>" % ( sys.argv[0], )
	print
	print "    <input>: any existing image file, e.g. a PNG,"
	print "             preferably 640x480"
	print
	print "   <output>: output filename - raw data to dump to"
	print "             /dev/fb/0, assuming you got the image"
	print "             dimensions right"
	print
	sys.exit(1)

import Image
im = Image.open( infile )
im2 = im.convert( "RGB" )
data = im2.getdata()

fp = open( outfile, "wb" )
for (r,g,b) in data:
	assert r >= 0 and r <= 255
	assert g >= 0 and g <= 255
	assert b >= 0 and b <= 255
	r /= 8
	g /= 4
	b /= 8
	assert r >= 0 and r <= 31
	assert g >= 0 and g <= 63
	assert b >= 0 and b <= 31
	value = r*2048+g*32+b
	assert value >= 0 and value <= 65535
	fp.write( chr(value%256)+chr(value/256) )

