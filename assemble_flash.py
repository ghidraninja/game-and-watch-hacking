#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser(description='Combine a flash image, an XOR-stream and a modified ROM into a flashable image.')
parser.add_argument('flash', nargs=1, type=argparse.FileType('rb'))
parser.add_argument('xor_key', nargs=1, type=argparse.FileType('rb'))
parser.add_argument('patched_rom', nargs=1, type=argparse.FileType('rb'))
parser.add_argument('flash_out', nargs=1, type=argparse.FileType('wb'))
parser.add_argument('--length', '-l', type=int, default=40*1024)
args = parser.parse_args()

LEN=args.length
ram_dump = args.patched_rom[0].read(LEN)


if len(ram_dump) != args.length:
    print("Adding Padding")
    ram_dump = ram_dump + (b"\x00" * (args.length - len(ram_dump)))

xor_key = args.xor_key[0].read()

flash_start = args.flash[0].read(0x1e60)
flash_content = args.flash[0].read(LEN)
flash_end = args.flash[0].read()

if len(xor_key) != len(ram_dump):
    print("FAILED, XOR key has wrong size.")
    sys.exit(-1)

def xor(b1, b2):
    result = bytearray()
    for b1, b2 in zip(b1, b2):
        result.append(b1 ^ b2)
    return result

xored_content = xor(ram_dump, xor_key)

args.flash_out[0].write(flash_start)
args.flash_out[0].write(xored_content)
args.flash_out[0].write(flash_end)

print("\n**********************")
print(  "New flash image ready!")
print("**********************")


