#!/usr/bin/env python3

import argparse

# Get arguments
parser = argparse.ArgumentParser()
parser.add_argument('flash',    nargs=1, type=argparse.FileType('rb'))
parser.add_argument('ram_dump', nargs=1, type=argparse.FileType('rb'))
parser.add_argument('xor_key',  nargs=1, type=argparse.FileType('wb'))
parser.add_argument('--length', '-l', type=int, default=40*1024)
args = parser.parse_args()

args.flash[0].seek(0x1E60)  # ROM file starts here for some reason

flash    = args.flash   [0].read(args.length)
ram_dump = args.ram_dump[0].read(args.length)
xor_key  = args.xor_key [0]

def xor(s1, s2):
  """XOR 2 byte streams together"""
  assert(len(s1) == len(s2))
  return bytearray([
    b1 ^ b2
    for b1, b2 in zip(s1, s2)
  ])

xor_key.write(xor(ram_dump, flash))
