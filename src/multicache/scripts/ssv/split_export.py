#!/usr/bin/python3

import json
import sys
import os
import copy

assert len(sys.argv) > 1 and "need to specify folder"

folder_name = sys.argv[1]

assert os.path.isdir(folder_name) and "no valid folder path specified"
assert folder_name[-1] == "/" and "missing trailing / for folder path"

must_contain = {
    "app":  ["http-nio"],
    "db": ["ib_log_writer"],
    "file": ["smbd", "cleanupd"],
    "stream": ["ffserver"],
    "web": ["apache2"],
    "mail": ["qmgr", "master", "proxymap", "trivial-rewrite", "smtpd", "tlsmgr", "local"]
}

must_contain_exact = {
    "app":  [],
    "db": [],
    "file": [],
    "stream": [],
    "web": [],
    "mail": ["cleanup"]
}

black_list = ["kworker", "migration", "swapper", "ksoftirq"]

filtered_dict = {
    "app": [],
    "db": [],
    "file": [],
    "mail": [],
    "stream": [],
    "web": []
}

files = os.listdir(folder_name)
files = [file for file in files if ".json" in file]

cpc = None

for file_name in files:
    file = open(folder_name + file_name, "r")
    core_dict = json.load(file)
    process_dict = core_dict["processes"]

    # to update global core values
    del core_dict["no_evict_streak_sum"]
    del core_dict["sched_kernel"]

    cpc = core_dict["num_caches"]

    for benchmark in must_contain:
        core_dict_copy = copy.deepcopy(core_dict)
        process_dict_copy = core_dict_copy["processes"]

        sched_time = 0
        sched = 0
        evictions = 0

        for process in process_dict:
            valid = False
            threads = process_dict[process]["threads"]
            thread_names = []
            for thread in threads:
                thread_names.append(threads[thread]["name"])

            for thread_name in thread_names:
                if any(required in thread_name for required in must_contain[benchmark]):
                    valid = True
                if any(exact == thread_name for exact in must_contain_exact[benchmark]):
                    valid = True

            if not valid:
                del process_dict_copy[process]
            else:
                sched_time += process_dict[process]["sched_time"]
                sched += process_dict[process]["sched"]
                evictions += process_dict[process]["evictions"]

        core_dict_copy["sched_time"] = sched_time
        core_dict_copy["sched"] = sched
        core_dict_copy["evictions"] = evictions

        if len(process_dict_copy) > 0:
            filtered_dict[benchmark].append((file_name, core_dict_copy))

    file.close()

for benchmark in filtered_dict:
    if len(filtered_dict[benchmark]) <= 0:
        continue

    filter_folder_name = folder_name[:-1]
    split_path = filter_folder_name.split("/")
    filter_folder_name = filter_folder_name.replace(split_path[-1], "filter=" + benchmark + "_" + split_path[-1]) + "/"

    try:
        os.mkdir(filter_folder_name)
    except:
        print("Folder already existed")

    for file_name, core_dict in filtered_dict[benchmark]:
        core_file = open(filter_folder_name + file_name, "w")
        json_obj = json.dumps(core_dict, indent=4)

        core_file.write(json_obj)

        core_file.close()