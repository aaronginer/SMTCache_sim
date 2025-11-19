#!/usr/bin/python3

import os
import sys
from tokenize import String
from core import Core
import numpy as np
import math

import argparse
from datetime import datetime

import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="Parse an l1e trace")
requiredArgs = parser.add_argument_group("Required arguments")
requiredArgs.add_argument("-c", "--cores", type=int, help="Number of logical cores", required=True)
requiredArgs.add_argument("-f", "--file", help="Trace file name", required=True)

optionalArgs = parser.add_argument_group("Optional arguments")

optionalArgs.add_argument("-t", "--target_tgid", type=int, action="extend", nargs="+", help="Select TGID of target to watch")
optionalArgs.add_argument("-T", "--target_core", type=int, action="extend", nargs="+", help="Select core to watch")
optionalArgs.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")
optionalArgs.add_argument("-e", "--export", action="store_true", help="Export process information")
optionalArgs.add_argument("-p", "--export_path", help="Enter path to export data to")
optionalArgs.add_argument("-E", "--events", action="extend", nargs="+", help="Enter events in their order in the trace (miss, hit, all_loads, all_stores, replacement, l2_rfo)")
optionalArgs.add_argument("-g", "--graph_data", action="store_true", help="Export the graph data of threads of selected export tgids")
args = parser.parse_args(sys.argv[1:])

target_tgid = args.target_tgid
target_core = args.target_core
cores = args.cores if args.cores is not None else 8
trace_file_name = args.file
debug = args.debug
do_export = args.export
export_path = args.export_path
graph_data = args.graph_data
events_list = args.events

## sanity checks
assert trace_file_name is not None
assert (not (events_list is None and do_export is True)) and "export is dependent on valid events_list"
assert target_core is None or any([t < cores for t in target_core])

## parse
core_objects = [Core(i) for i in range(cores)]
trace_file = open(trace_file_name, "r")

min_time = None
max_time = None
line_nr = 0

for line in trace_file:
    line_nr += 1
    
    if line[0] == '#':
        continue
    
    
    line_split = line.replace("\t", "").replace("\n", "").replace("\r", "").split(',')

    time_split = line_split[0].split(".")
    time_micro = int(time_split[0]) * 1000000 + int(time_split[1])
    time = time_micro / 1000000
    
    if min_time is None:
        min_time = time
    
    max_time = time
    
    thread = int(line_split[1])
    core_idx = thread % cores
    
    if target_core is not None and core_idx not in target_core:
        continue
    
    tgid = int(line_split[2])
    pid = int(line_split[3])
    thread_name = line_split[4]
    
    events = np.zeros(8)
    
    for idx in range(5, 13):
        if len(line_split) <= idx:
            break
        
        events[idx-5] = int(line_split[idx], 16) 

    core_objects[core_idx].add_deltas(time, tgid, pid, thread_name, events, graph_data)

trace_file.close()   
    
    
def export(export_path, graph_data):
    if export_path is None:
        export_path = ""

    if len(export_path) > 0 and export_path[-1] == '/':
        export_path = export_path[:-1]

    export_path = export_path + os.path.splitext(trace_file_name)[0]

    if not os.path.exists(export_path):
        os.mkdir(export_path)

    for core in core_objects:
        core.export(export_path, events_list, graph_data)

for core in core_objects:
    if target_core is None or core.get_nr() in target_core:
        pass
        # print(f"\nCore: {core.get_nr()}\n")
        
        # core.print_results(target_tgid)
                
if do_export:
    export(export_path, graph_data)
