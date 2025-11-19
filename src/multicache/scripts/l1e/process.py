from concurrent.futures import thread
import matplotlib.pyplot as plt
import numpy as np
from thread import Thread
from pmc_functions import *
import json

export_black_list = ["kworker", "migration", "swapper", "ksoftirq"]

class Process:
    def __init__(self, tgid, start_time):
        self.tgid = tgid
        
        self.events = np.zeros(8)
        
        self.sched_count_total = 0
        
        self.start_time = start_time
        self.current_time = 0
        self.time_scheduled = 0

        self.pid_thread = {}

    def get_tgid(self):
        return self.tgid

    def add_deltas(self, time, time_delta, pid, thread_name, events_delta, graph_data):

        if pid not in self.pid_thread:
            self.pid_thread[pid] = Thread(thread_name, pid)
        
        self.pid_thread[pid].add_deltas(time, time_delta, events_delta, graph_data)
        self.events = np.add(self.events, events_delta)
            
        self.current_time = time
        self.sched_count_total += 1
        self.time_scheduled += time_delta

    def print_results(self):        
        print("")
        
        print("TGID: {:<8} - L1_MISS={:<10} - L1_HIT={:<10} - ALL_LOADS={:<10} - ALL_STORES={:<10} - L1D.REPLACEMENT={:<10} - L2_ALL_RFO={:<10} - LOAD_MISS={:<6}% - REPLACEMENT_RATE={:<6}% - TOTAL_MISS={:<6}% - SCHED={:<6}".format(self.tgid, self.events[0], self.events[1], self.events[2], self.events[3], self.events[4], self.events[5], load_miss(self.events), replacement_rate(self.events), total_miss(self.events), self.sched_count_total))        
        
        for thread in self.pid_thread.values():
            thread.print_results()
            
        print("")

    def export(self, core_idx, export_path, event_list, process_dict, graph_data):
        # check for blacklisted threadnames
        # for thread in self.pid_thread.values():
        #    if any(banned in thread.get_name() for banned in export_black_list):
        #        return
        
        p_dict = {
            "sched": self.sched_count_total,
            "start_time": self.start_time,
            "end_time": self.current_time,
            "time": self.time_scheduled
        }

        for idx in range(len(event_list)):
            p_dict[event_list[idx]] = self.events[idx]
        
        thread_dict = {}

        for thread in self.pid_thread.values():
            thread.export(core_idx, export_path, event_list, thread_dict, graph_data)

        p_dict["threads"] = thread_dict

        process_dict[self.tgid] = p_dict