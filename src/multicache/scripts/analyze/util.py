from concurrent.futures import thread
from symbol import eval_input
import matplotlib.pyplot as plt
import json
import numpy as np
import os
import scipy

def check_missing(data, events):
    do_assert = False
    is_in_data = True
    for e in events:
        if do_assert:
            assert e in data
        elif not e in data:
            is_in_data = False
            break
    return is_in_data

# input: array of dictionaries containing hit and miss values
def load_miss(data_array, thread_filter=None):
    hits = 0
    misses = 0

    for data in data_array:
        process_dict = data["processes"]
        for process in process_dict:
            process_data = process_dict[process]

            if not check_missing(process_data, ["miss", "hit"]):
                continue

            if thread_filter is not None:
                thread_dict = process_data[process]["threads"]
                for thread in thread_dict:
                    if thread_dict[thread]["name"] not in thread_filter:
                        continue
                    hits += thread_dict[thread]["hit"]
                    misses += thread_dict[thread]["miss"]
            else:
                hits += process_data["hit"]
                misses += process_data["miss"]

    total = hits + misses
    return 0 if total == 0 else misses / total, total > 0

# input: array of dictionaries containing hit and miss values
def fb_hit(data_array, thread_filter=None):
    fb_hits = 0
    hits = 0
    misses = 0

    for data in data_array:
        process_dict = data["processes"]
        for process in process_dict:
            process_data = process_dict[process]

            if not check_missing(process_data, ["miss", "hit", "fbhit"]):
                continue

            if thread_filter is not None:
                thread_dict = process_data[process]["threads"]
                for thread in thread_dict:
                    if thread_dict[thread]["name"] not in thread_filter:
                        continue
                    fb_hits += process_data["fbhit"]
                    hits += thread_dict[thread]["hit"]
                    misses += thread_dict[thread]["miss"]
            else:
                fb_hits += process_data["fbhit"]
                hits += process_data["hit"]
                misses += process_data["miss"]

    total = hits + misses + fb_hits

    return 0 if total == 0 else fb_hits / total, total > 0

def load_miss_all(data_array, thread_filter=None):
    fb_hits = 0
    hits = 0
    misses = 0

    for data in data_array:
        process_dict = data["processes"]
        for process in process_dict:
            process_data = process_dict[process]

            if not check_missing(process_data, ["miss", "hit", "fbhit"]):
                continue

            if thread_filter is not None:
                thread_dict = process_data[process]["threads"]
                for thread in thread_dict:
                    if thread_dict[thread]["name"] not in thread_filter:
                        continue
                    fb_hits += process_data["fbhit"]
                    hits += thread_dict[thread]["hit"]
                    misses += thread_dict[thread]["miss"]
            else:
                fb_hits += process_data["fbhit"]
                hits += process_data["hit"]
                misses += process_data["miss"]

    total = hits + misses + fb_hits

    return 0 if total == 0 else misses / total, total > 0

def eviction_rate(data_array, thread_filter=None):
    scheds = 0
    evictions = 0

    for data in data_array:
        process_dict = data["processes"]
        for process in process_dict:
            process_data = process_dict[process]

            if not check_missing(process_data, ["sched", "evictions"]):
                continue

            if thread_filter is not None:
                thread_dict = process_data[process]["threads"]
                for thread in thread_dict:
                    if thread_dict[thread]["name"] not in thread_filter:
                        continue
                    scheds += thread_dict[thread]["sched"]
                    evictions += thread_dict[thread]["evictions"]
            else:
                scheds += process_data["sched"]
                evictions += process_data["evictions"]

    return 0 if scheds == 0 else evictions / scheds, scheds > 0

def inst_per_switch(data_array, thread_filter=None):
    scheds = 0
    inst = 0

    for data in data_array:
        process_dict = data["processes"]
        for process in process_dict:
            process_data = process_dict[process]

            if not check_missing(process_data, ["sched", "inst"]):
                continue

            if thread_filter is not None:
                thread_dict = process_data["threads"]
                for thread in thread_dict:
                    if thread_dict[thread]["name"] not in thread_filter:
                        continue
                    scheds += thread_dict[thread]["sched"]
                    inst += thread_dict[thread]["inst"]
            else:
                scheds += process_data["sched"]
                inst += process_data["inst"]

    return 0 if scheds == 0 else inst / scheds, inst > 0

def loads_per_switch(data_array, thread_filter=None):
    scheds = 0
    loads = 0

    for data in data_array:
        process_dict = data["processes"]
        for process in process_dict:
            process_data = process_dict[process]

            if not check_missing(process_data, ["load_all", "inst"]):
                continue

            if thread_filter is not None:
                thread_dict = process_data[process]["threads"]
                for thread in thread_dict:
                    if thread_dict[thread]["name"] not in thread_filter:
                        continue
                    scheds += thread_dict[thread]["sched"]
                    loads += thread_dict[thread]["load_all"]
            else:
                scheds += process_data["sched"]
                loads += process_data["load_all"]

    return 0 if scheds == 0 else loads / scheds, loads > 0

def avg_sched_time(data_array, thread_filter=None):
    scheds = 0
    time = 0

    for data in data_array:
        process_dict = data["processes"]
        for process in process_dict:
            process_data = process_dict[process]

            check_missing(process_data, ["sched", "time"])

            if thread_filter is not None:
                thread_dict = process_data[process]["threads"]
                for thread in thread_dict:
                    if thread_dict[thread]["name"] not in thread_filter:
                        continue
                    scheds += thread_dict[thread]["sched"]
                    time += thread_dict[thread]["time"]
            else:
                scheds += process_data["sched"]
                time += process_data["time"]

    return 0 if scheds == 0 else time / scheds * 1000, time > 0

def processes_spawned(data_array):
    processes = 0
    for data in data_array:
        processes += len(data["processes"])

    return processes, True

def dist(stat_array):
    mean = np.mean(stat_array)
    std = np.std(stat_array)

    return mean, std

def time_passed(data_array):
    for data in data_array:
        check_missing(data, ["start_time", "end_time"])

    time_total = 0
    for data in data_array:
        time_total += data["end_time"] - data["start_time"]

    return time_total / len(data_array)

def time(data_array):
    for data in data_array:
        check_missing(data, ["time"])

    time_total = 0
    for data in data_array:
        time_total += data["time"]

    return time_total / len(data_array)

def get_folders(parent_folder_path):
    folders = [folder.path for folder in os.scandir(parent_folder_path) if folder.is_dir()]
    folders.sort()
    return folders

# https://www.adamsmith.haus/python/answers/how-to-sort-two-lists-together-in-python

def trim_lists(stats):
    std = np.std(stats)
    mean = np.mean(stats)

    # outliers = values further away than 2 times the standard deviation from the mean
    stats = [e for e in stats if abs(mean - e) <= 2*std]
    return stats

# read all json files in the subfolders of the given parent folder
def get_folder_data(parent_folder_path, statistic, filter=None, thread_filter=None):
    stat_array = []

    folders_dict = {}

    for folder_name in get_folders(parent_folder_path):
        if filter is None and "filter" in folder_name:
            continue
        elif filter is not None and "filter="+filter not in folder_name:
            continue

        folders_dict[folder_name] = {}
        
        files = os.listdir(folder_name)
        files = [file for file in files if ".json" in file]

        data_array = []

        for file_name in files:
            path = folder_name + "/" + file_name

            data_file = open(path, "r")

            data = json.load(data_file)
            data_array.append(data)

            folders_dict[folder_name][file_name] = data

            data_file.close()

        stat, valid = 0, False
        if statistic == "lmr":
            stat, valid = load_miss(data_array, thread_filter)
        elif statistic == "fb":
            stat, valid = fb_hit(data_array, thread_filter)
        elif statistic == "lma":
            stat, valid = load_miss_all(data_array, thread_filter)
        elif statistic == "er":
            stat, valid = eviction_rate(data_array, thread_filter)
        elif statistic == "ips":
            stat, valid = inst_per_switch(data_array, thread_filter)
        elif statistic == "lps":
            stat, valid = loads_per_switch(data_array, thread_filter)
        elif statistic == "time":
            stat, valid = avg_sched_time(data_array, thread_filter)
        elif statistic == "ps":
            stat, valid = processes_spawned(data_array)

        if valid:
            stat_array.append(stat)
        
    return stat_array, folders_dict

def get_central_tendency_type(dict, allow_missing=True):
    try:
        return dict["central_tendency"]
    except:
        assert allow_missing
        return "a_mean"

def central_tendency(stat_array, type):
    if type == "a_mean":
        return np.mean(stat_array)
    elif type == "median":
        return np.median(stat_array)
    elif type == "g_mean":
        return scipy.stats.mstats.gmean(stat_array)

    assert False