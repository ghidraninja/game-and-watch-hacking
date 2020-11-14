#!/usr/bin/env python3

import argparse
import sys

parser = argparse.ArgumentParser(description='Extract XOR-key from flash dump & RAM dump.')
parser = argparse.ArgumentParser()
parser.add_argument('flash', nargs=1, type=argparse.FileType('rb'))
parser.add_argument('ram_dump', nargs=1, type=argparse.FileType('rb'))
parser.add_argument('xor_key', nargs=1, type=argparse.FileType('wb'))
parser.add_argument('--length', '-l', type=int, default=40*1024)
args = parser.parse_args()


LEN=args.length
ram_dump = args.ram_dump[0].read(LEN)
# Start of ROM in flash
args.flash[0].seek(0x1e60)
flash = args.flash[0].read(LEN)

def xor(b1, b2):
    result = bytearray()
    for b1, b2 in zip(b1, b2):
        result.append(b1 ^ b2)
    return result

args.xor_key[0].write(xor(ram_dump, flash))

print(f"XOR stream successfully written!")



