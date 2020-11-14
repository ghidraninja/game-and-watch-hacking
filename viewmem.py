#!/usr/bin/env python3

from PIL import Image, ImageColor
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('rom', nargs=1, type=argparse.FileType('rb'))
parser.add_argument('--offset', '-l', type=int, default=4)
parser.add_argument('--width', '-w', type=int, default=100)
args = parser.parse_args()

import time

args.rom[0].seek(args.offset)
width = args.width
im = Image.new('RGBA', (args.width,1024)) # create the Image of size 1 pixel 

for y in range(0, 1024):
    for x in range(0, width):
        try:
            data = args.rom[0].read(4)
            im.putpixel( (x, y), (data[0], data[1], data[2], 255) ) 
        except:
            im.putpixel( (x, y), (0,0,0, 255) ) 
            
im.show()
