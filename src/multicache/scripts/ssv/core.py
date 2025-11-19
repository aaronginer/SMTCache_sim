from core_data import *

class Core:
    def __init__(self, number, num_caches, num_threads):
        self.number = number
        self.num_threads = num_threads
        # caches - 1 because 1 is dedicated to the kernel, we never touch that
        self.num_caches = num_caches - 1
        self.threads = {}
        self.caches = [None] * self.num_caches
        self.core_data = CoreData()

    def sched(self, thread, is_kernel, tgid, pid, name, time):
        assert len(self.threads.keys()) <= self.num_threads

        if thread not in self.threads:
            self.threads[thread] = None

        self.core_data.sched(is_kernel, tgid, pid, name, time)

        # there is a dedicated kernel cache anyway, so ignore kernel schedules here
        if not is_kernel:
            if tgid in self.caches:
                # remove tgid and shift entries up to tgid's current position
                self.shift(self.caches.index(tgid) + 1)
                # re-insert element at front
                self.insert_front(tgid)
            else: 
                self.core_data.reuse(tgid)
                # evict pgd and shift pgds up to evict-position
                self.shift(self.caches.index(self.find_to_evict(thread)) + 1)
                # insert new element at front
                self.insert_front(tgid)

        self.threads[thread] = tgid if not is_kernel else "kernel"
        self.core_data.inc_access_streak(self.caches)

    #
    # Shift all pgds before 'shift_to' up to a 'shift_to'
    #
    def shift(self, shift_to):
        # shift existing pgds to index age_to
        for i in reversed(range(1, shift_to)):
            self.caches[i] = self.caches[i - 1]

    #
    # find tgid to evict (LRU policy w.r.t. SMT)
    #
    def find_to_evict(self, thread):
        for tgid in reversed(self.caches):
            # evict empty caches first
            if tgid is None:
                break
            # evict if tgid not currently active for another logical core
            if tgid not in self.threads.values():
                break
        else:
            # if no caches are empty and all other ones are in use by other logical cores
            # evict cache of current tgid of current thread
            tgid = self.threads[thread]
        
        if tgid is not None:
            self.core_data.evict(tgid)

        return tgid

    def insert_front(self, tgid):
        self.caches[0] = tgid

    def get_accesses(self):
        return self.core_data.get_accesses()

    def get_accesses_kernel(self):
        return self.core_data.get_kernel_accesses()

    def get_evictions(self):
        return self.core_data.get_evictions()

    def get_eviction_rate(self):
        return -1 if self.get_accesses() == 0 else round(self.get_evictions() / self.get_accesses() * 100, 2)

    def get_number(self):
        return self.number

    ############### PRINT METHODS ##################

    def print_generic_results(self, pinfo):
        self.core_data.print_generic_results(pinfo, self.number)

    def print_process_info(self, tgid):
        self.core_data.print_process_info(tgid)

    def print_debug_info(self):
        print("Core: " + str(self.number))
        out = "["
        for i in range(self.num_caches):
            out += ('[{:<15s}-{:>6s}]' + (', ' if i < self.num_caches - 1 else '')).format(
                str(self.caches[i]) if self.caches[i] is not None else "None",
                str(self.core_data.get_tgid_streak(self.caches[i])) if self.caches[i] is not None else "0")
        out += "]"
        print(out)
        print(self.threads)

    ############### EXPORT #####################

    def export(self, export_path):
        self.core_data.export(export_path, self.number, self.num_caches)