#!/usr/bin/env python3

from PIL import Image
import argparse

# Get arguments
parser = argparse.ArgumentParser()
parser.add_argument('rom', nargs=1, type=argparse.FileType('rb'))
parser.add_argument('--offset', '-l', type=int, default=4)
parser.add_argument('--width', '-w', type=int, default=100)
args = parser.parse_args()

rom = args.rom[0]
rom.seek(args.offset)
im = Image.new('RGBA', (args.width, 1024))

for y in range(0, 1024):
  for x in range(0, args.width):
    try:
      data = rom.read(4)
      im.putpixel( (x, y), (data[0], data[1], data[2], 255) ) 
    except:
      im.putpixel( (x, y), (0,0,0, 255) ) 

im.show()
