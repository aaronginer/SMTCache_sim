from process_data import *
import json

KERNEL = '0000000000000000'


class CoreData:
    def __init__(self):
        self.cache_evictions = 0
        self.cache_accesses = 0
        self.cache_accesses_kernel = 0

        # average schedule duration
        self.prev_sched_time = 0
        self.total_sched_time = 0

        self.tgid_process_map = {}

        # average time to eviction calculation
        self.tgid_access_streak_map = {}
        self.access_streak_sum = 0

    def sched(self, is_kernel, tgid, pid, name, time):
        time_delta = 0
        if self.prev_sched_time != 0:
            time_delta = time - self.prev_sched_time
            self.total_sched_time += time_delta
        self.prev_sched_time = time

        if tgid not in self.tgid_access_streak_map:
            self.tgid_access_streak_map[tgid] = 0

        if tgid not in self.tgid_process_map:
            self.tgid_process_map[tgid] = ProcessData(tgid)

        self.tgid_process_map[tgid].acc(name, pid, time_delta)

        if not is_kernel:
            self.cache_accesses += 1
        else:
            self.cache_accesses_kernel += 1

    def reuse(self, tgid):
        self.tgid_process_map[tgid].reuse()

    def inc_access_streak(self, caches):
        for tgid in caches:
            if tgid is not None:
                self.tgid_access_streak_map[tgid] += 1

    def evict(self, tgid):
        self.cache_evictions += 1
        self.tgid_process_map[tgid].evict()
        self.access_streak_sum += self.tgid_access_streak_map[tgid]
        self.tgid_access_streak_map[tgid] = 0

    def print_generic_results(self, pinfo, core):
        eviction_rate = 0 if self.cache_accesses == 0 else round(self.cache_evictions / self.cache_accesses * 100, 2)
        avg_tbs_ms = 0 if self.cache_accesses == 0 else round(self.total_sched_time / self.cache_accesses * 1000, 5)
        avg_tte_sc = "-" if self.cache_evictions == 0 else round(self.access_streak_sum / self.cache_evictions, 5)
        avg_tte_ms = "-" if avg_tte_sc == "-" else round(avg_tte_sc * avg_tbs_ms, 5)
        # "need new cache on return"
        avg_nncr = 0 if self.cache_accesses == 0 else round(
            sum(self.tgid_process_map[tgid].get_reuse_counter() if self.tgid_process_map[tgid].get_reuse_counter() >= 0 else 0 
            for tgid in self.tgid_process_map.keys()) / self.cache_accesses * 100, 5)

        print("Core: " + str(core))
        print(" - Accesses: " + str(self.cache_accesses) + " - Evictions: " + str(self.cache_evictions))
        print(" - Eviction rate: " + str(eviction_rate) + "%")
        print(" - Avg time between switches: " + str(avg_tbs_ms) + " ms")
        print(" - Avg time to eviction: " + str(avg_tte_sc) + " sched / " + str(avg_tte_ms) + " ms")
        print(" - Avg % of processes that needed a new cache on return: " + str(avg_nncr) + "%" + str())
        print("\nKernel accesses: " + str(self.cache_accesses_kernel) + "\n")

        if pinfo:
            for key in reversed(
                    sorted(self.tgid_process_map, key=lambda tgid: self.tgid_process_map[tgid].get_schedules())):
                self.print_process_info(key)

    def print_process_info(self, tgid):
        if tgid not in self.tgid_process_map:
            return

        out = "\n"
        out += self.tgid_process_map[tgid].get_process_info()
        out += self.tgid_process_map[tgid].get_thread_info()
        print(out)

    def get_tgid_streak(self, tgid):
        return self.tgid_access_streak_map[tgid]

    def get_accesses(self):
        return self.cache_accesses

    def get_kernel_accesses(self):
        return self.cache_accesses_kernel

    def get_evictions(self):
        return self.cache_evictions

    def export(self, export_path, core, num_caches):
        core_dict = {
            "sched_time": self.total_sched_time,
            "sched": self.cache_accesses,
            "sched_kernel": self.cache_accesses_kernel,
            "evictions": self.cache_evictions,
            "no_evict_streak_sum": self.access_streak_sum,
            "num_caches": num_caches + 1 
        }

        process_dict = {}

        for tgid in self.tgid_process_map:
            self.tgid_process_map[tgid].export(process_dict)

        core_dict["processes"] = process_dict

        if len(process_dict) > 0:
            json_obj = json.dumps(core_dict, indent=4)

            json_file = export_path + "/core" + str(core) + ".json"

            file = open(json_file, "w")

            file.write(json_obj)

            file.close()