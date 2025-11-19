import subprocess
import os
import sys
import time
import argparse

timeout = 5
core_piping = "3"

parser = argparse.ArgumentParser(description="Record scheduling trace")

parser.add_argument("--parse", action="store_true", help="Parse file after recording")
parser.add_argument("--core", help="Program target core")
parser.add_argument("--exec", help="Program to execute, use ''")
parser.add_argument("--program", help="Program name")
args = parser.parse_args(sys.argv[1:])

core_exec = args.core if args.core is not None else "0"
taskset_cmd = ["taskset", "-c", core_exec]

if args.exec is not None:
    print("Executing program...")
    try:
        subprocess.Popen(taskset_cmd + args.exec.split(" "), stdout=subprocess.DEVNULL)
    except Exception:
        print("Program execution not possible")

time.sleep(1)

target_tgid = ""

if args.program is not None:
    print("Getting program TGIDs...")
    stream = os.popen("pidof " + args.program)
    tgids = stream.read().replace("\n", "")
    target_tgid = " --target_tgid " + tgids
    print("Got TGIDS: " + tgids)

print("Piping trace...")

file_name = "trace_file.x"
file_num = 1
while os.path.isfile(file_name):
        file_name = file_name[:(-2 if file_num == 1 else -3)] + str(file_num) + ".x"
        file_num += 1

os.system("taskset -c " + core_piping + " timeout " + str(timeout) + " cat /sys/kernel/debug/tracing/trace_pipe > " + file_name)

print("Piping trace successful")

if args.program is not None:
    os.system("killall " + args.program)

cmd = "python3 parse_trace.py --file " + file_name + target_tgid + (" --target_core " + core_exec if args.exec is not None else "")

if args.parse:
    print("Executing: \'"+ cmd + "\'")
    os.system(cmd)