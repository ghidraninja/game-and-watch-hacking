#!/usr/bin/env python3

import argparse

# Get arguments
parser = argparse.ArgumentParser()
parser.add_argument('flash',       nargs=1, type=argparse.FileType('rb'))
parser.add_argument('xor_key',     nargs=1, type=argparse.FileType('rb'))
parser.add_argument('patched_rom', nargs=1, type=argparse.FileType('rb'))
parser.add_argument('flash_out',   nargs=1, type=argparse.FileType('wb'))
parser.add_argument('--length', '-l', type=int, default=40*1024)
args = parser.parse_args()

patched = args.patched_rom[0].read(args.length)

# Pad the patched ROM to be the length specified in the command line
if len(patched) != args.length:
  print("Adding Padding")
  patched += b"\x00" * (args.length - len(ram_dump))

xor_key = args.xor_key[0].read()

# Deconstruct the original flash file
flash_start   = args.flash[0].read(0x1E60)
flash_content = args.flash[0].read(args.length)  # Never used. Consider seeking instead
flash_end     = args.flash[0].read()

def xor(s1, s2):
  """XOR 2 byte streams together"""
  assert(len(s1) == len(s2))
  return bytearray([
    b1 ^ b2
    for b1, b2 in zip(s1, s2)
  ])

# Reconstruct the modified flash file
args.flash_out[0].write(flash_start)
args.flash_out[0].write(xor(patched, xor_key))
args.flash_out[0].write(flash_end)
