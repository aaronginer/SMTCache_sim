# script to list all tgids for specified filter

# deprecated

import sys
from collections import OrderedDict

assert len(sys.argv) > 1

file_name = sys.argv[1]
benchmark = "" if len(sys.argv) < 3 else sys.argv[2]

must_contain = {
    "app":  ["http-nio"],
    "db": ["ib_log_writer"],
    "file": ["smbd"],
    "stream": ["ffserver"],
    "web": ["apache2"]
}

must_not_contain = {
    "mail": ["http-nio", "ib_log_writer", "smbd", "ffserver", "apache2"]
}

trace_file = open(file_name, "r")

tgid_dict = {}

black_list = ["kworker", "migration", "swapper", "ksoftirq"]

for line in trace_file:    
    if line[0] == '#':
        continue
    
    
    line_split = line.replace("\t", "").replace("\n", "").replace("\r", "").split(',')
    
    tgid = int(line_split[2])

    thread_name = line_split[4]

    if any(banned in thread_name for banned in black_list):
        continue

    if tgid not in tgid_dict:
        tgid_dict[tgid] = set()

    tgid_dict[tgid].add(thread_name)

trace_file.close()

ordered_tgid_dict = OrderedDict(sorted(tgid_dict.items()))

def print_dict():
    for tgid in ordered_tgid_dict:
        print(tgid)
        print("threads: {threads}".format(threads=ordered_tgid_dict[tgid]))

def filter_dict(tgid_dict):
    tgid_list = []

    if benchmark in must_not_contain:
        for tgid in tgid_dict:
            found = False
            for thread_name in tgid_dict[tgid]:
                if any(banned in thread_name for banned in must_not_contain[benchmark]):
                    found = True

            if not found:
                tgid_list.append(tgid)

    if benchmark in must_contain:
        for tgid in tgid_dict:
            found = False
            for thread_name in tgid_dict[tgid]:
                if any(required in thread_name for required in must_contain[benchmark]):
                    found = True

            if found:
                tgid_list.append(tgid)

    if benchmark not in must_contain and benchmark not in must_not_contain:
        for tgid in tgid_dict:
            tgid_list.append(tgid)

    return tgid_list

filtered_list = filter_dict(tgid_dict)

print(" ".join([str(e) for e in filtered_list]))