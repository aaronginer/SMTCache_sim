from array import array
import numpy as np
from pmc_functions import *
import matplotlib.pyplot as plt
import os

class Thread:
    def __init__(self, name, pid):
        self.pid = pid
        self.name = name
        
        self.events = np.zeros(8)
        self.sched = 0
        self.total_time = 0
        
        self.time_event = {}

    def get_events(self):
        return self.events

    def get_pid(self):
        return self.pid

    def get_name(self):
        return self.name

    def get_sched(self):
        return self.sched

    def get_total_time(self):
        return round(self.total_time, 4)
        
    def add_deltas(self, time, time_delta, events_delta, graph_data):
        self.total_time += time_delta
        self.events = np.add(self.events, events_delta)
        self.sched += 1

        if graph_data:
            self.time_event[time] = events_delta
        
    def print_results(self):
        print("")
        print(" - PID: {:<8} NAME: {:<20}".format(self.pid, self.name))
        time_sec = self.total_time / (self.sched)
        time_ms = time_sec * 1000
        print("        Average schedule time: {0:.20f}s / {1:.20f}ms".format(time_sec, time_ms))
        print("        L1_MISS={:<10} - L1_HIT={:<10} - ALL_LOADS={:<10} - ALL_STORES={:<10} - L1D.REPLACEMENT={:<10} - L2_ALL_RFO={:<10} - LOAD_MISS={:<6}% - REPLACEMENT_RATE={:<6}% - TOTAL_MISS={:<6}% - SCHED={:<6}".format(self.events[0], self.events[1], self.events[2], self.events[3], self.events[4], self.events[5], load_miss(self.events), replacement_rate(self.events), total_miss(self.events), self.sched))
        print("")

    def export(self, core_idx, export_path, event_list, thread_dict, graph_data):
        t_dict = {}
        for idx in range(len(event_list)):
            t_dict[event_list[idx]] = self.events[idx]
        t_dict["name"] = self.name
        t_dict["sched"] = self.sched
        t_dict["time"] = self.total_time

        thread_dict[self.pid] = t_dict

        if graph_data:
            csv_file = export_path + "/" + str(self.pid) + "_core" + str(core_idx) + ".csv"

            file = open(csv_file, "a")

            file.write("time,"+",".join(event_list)+"\n")

            for t in self.time_event:
                evts = self.time_event[t]
                file.write(str(t)+","+",".join([str(int(evts[idx])) for idx in range(min(len(event_list), len(evts)))])+"\n")

            file.close()