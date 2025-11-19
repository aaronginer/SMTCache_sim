#!/usr/bin/python3

from concurrent.futures import process
import sys
from urllib.parse import ParseResult
from core import *
from processor import Processor
import os

import argparse

# ARGS PARSING
parser = argparse.ArgumentParser(description="Parse a scheduling trace")
parser.add_argument("-t", "--target_tgid", type=int, action="extend", nargs="+", help="Select TGID of target to watch")
parser.add_argument("-T", "--target_core", type=int, action="extend", nargs="+", help="Select core to watch")
parser.add_argument("-l", "--lc", type=int, help="Number of logical cores")
parser.add_argument("-p", "--pc", type=int, help="Number of physical cores")
parser.add_argument("-c", "--cpc", type=int, help="Caches per core")
parser.add_argument("-f", "--file", help="Trace file name")
parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
parser.add_argument("-i", "--pinfo", action="store_true", help="Enable program stats output")
parser.add_argument("-e", "--export", action="store_true", help="Export process information")
args = parser.parse_args(sys.argv[1:])

physical_cores = args.pc
logical_cores = args.lc
caches_per_core = args.cpc
trace_file = args.file
do_export = args.export

############# If any of these are true, the program is aborted ###############

# sanity checks
if caches_per_core <= 1:
    print("Minimum number of caches: 2")
    exit(-1)

if not logical_cores % physical_cores == 0:
    print("Invalid number of logical cores: l-cores % p-cores must equal 0")
    exit(-1)

if args.target_core is not None and all(core > physical_cores for core in args.target_core):
    print("Target core number exceeds number of physical cores")
    exit(-1)

if int(logical_cores / physical_cores) > caches_per_core - 1:
    print("There must be at least one cache per hyperthread")
    exit(-1)

try:
    file = open(trace_file, "r")  # if not pipe else None
    print("Reading file: " + trace_file)
except FileNotFoundError:
    print("Invalid trace file.")
    exit(-1)

processor = Processor(physical_cores, caches_per_core, int(logical_cores / physical_cores), args.debug, file is None)
processor.parse_trace_file(file, args.target_core)
processor.print_results(args.target_tgid, args.target_core, args.pinfo)

file.close()

def export(trace_file):
    processor.export(trace_file)
                
if do_export:
    export(trace_file)
