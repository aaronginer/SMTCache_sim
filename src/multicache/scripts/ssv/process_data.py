from os import access

# Info:
# On linux, tgid = pid, pid = tid
class ProcessData:
    def __init__(self, tgid):
        self.tgid = tgid
        self.accesses = 0
        self.evictions = 0
        # starts at -1 because first schedule is not a reuse
        self.reuse_counter = -1
        self.pid_name_map = {}
        self.pid_schedule_map = {}
        self.total_time = 0

    def acc(self, name, pid, time_delta):
        if pid not in self.pid_name_map:
            self.pid_name_map[pid] = name

        self.accesses += 1
        self.total_time += time_delta

        if pid not in self.pid_schedule_map:
            self.pid_schedule_map[pid] = 1
        else:
            self.pid_schedule_map[pid] += 1

    def evict(self):
        self.evictions += 1

    def reuse(self):
        self.reuse_counter += 1

    def get_schedules(self):
        return self.accesses

    def get_reuse_counter(self):
        return self.reuse_counter

    def get_process_info(self):
        out = 'TGID: {:<10}\n'.format(self.tgid)
        out += '- Accesses: {:>10}\n'.format(self.accesses)
        out += '- Evictions: {:>10}\n'.format(self.evictions)
        out += "- New cache on return: {:>6} {:>11}\n".format(0 if self.reuse_counter < 0 else self.reuse_counter,
            ("(" + str(-1 if self.accesses == 0 else round((0 if self.reuse_counter < 0 else self.reuse_counter) / self.accesses * 100, 5))) + "%)")
        return out

    def get_thread_info(self):
        out = "\n"
        for pid in self.pid_name_map.keys():
            out += "  > {:<5} {:>20} {:>10}\n".format(pid, self.pid_name_map[pid], self.pid_schedule_map[pid])
        return out

    def export(self, process_dict):
        p_dict = {
            "sched_time": self.total_time,
            "sched": self.accesses,
            "evictions": self.evictions,
            "reuse": self.reuse_counter
        }

        threads_dict = {}

        for pid in self.pid_name_map:
            t_dict = {
                "name": self.pid_name_map[pid],
                "sched": self.pid_schedule_map[pid]
            } 

            threads_dict[pid] = t_dict

        p_dict["threads"] = threads_dict

        process_dict[self.tgid] = p_dict