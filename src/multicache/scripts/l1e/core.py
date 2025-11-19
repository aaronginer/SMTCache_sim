from process import Process
import math
import numpy as np
from pmc_functions import *
import json

class Core:
    def __init__(self, nr):
        self.nr = nr
        
        self.processes = {}
        self.prev_events = np.array([None] * 8)
        
        self.events = np.zeros(8)
        
        self.prev_time = 0

    def add_deltas(self, time, tgid, pid, thread_name, events, graph_data):
        
        if None not in self.prev_events:
            if tgid not in self.processes:
                self.processes[tgid] = Process(tgid, time)

            events_delta = np.subtract(events, self.prev_events)
            
            self.processes[tgid].add_deltas(time, time - self.prev_time, pid, thread_name, events_delta, graph_data)
            
            self.events = np.add(self.events, events_delta)
            
        self.prev_time = time
        self.prev_events = events

    def get_nr(self):
        return self.nr

    def print_results(self, target_tgid):
        print("LOAD_MISS={:<6}% - STORE_MISS={:<6}% - REPLACEMENT_RATE={:<6}% - TOTAL_MISS={:<6}%\n".format(load_miss(self.events), store_miss(self.events), replacement_rate(self.events), total_miss(self.events)))
        
        for process in self.processes.values():
            if target_tgid is None or process.tgid in target_tgid:
                process.print_results()

    def export(self, export_path, events_list, graph_data):
        core_dict = {}
        process_dict = {}
        for process in self.processes.values():
            process.export(self.nr, export_path, events_list, process_dict, graph_data)

        core_dict["processes"] = process_dict

        if len(process_dict) > 0:
            json_obj = json.dumps(core_dict, indent=4)

            json_file = export_path + "/core" + str(self.nr) + ".json"

            file = open(json_file, "w")

            file.write(json_obj)

            file.close()