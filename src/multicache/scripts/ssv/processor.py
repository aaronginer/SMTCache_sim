import re
import sys
import os
from timeit import default_timer as timer
from core import Core
from parseobject import ParseObject


class Processor:
    def __init__(self, num_cores, caches, num_threads, debug=False, stdin=False):
        self.num_cores = num_cores
        self.num_threads = num_threads
        self.cores = [Core(i, caches, num_threads) for i in range(num_cores)]
        self.debug = debug
        self.stdin = stdin
        self.parse_errors = 0
        self.pid_errors = 0

    def sched(self, core, thread, is_kernel, tgid, pid, name, time):
        core = thread % self.num_cores

        self.cores[core].sched(thread, is_kernel, tgid, pid, name, time)

        if self.debug:
            if not self.stdin:
                pass  # input()
            self.cores[core].print_debug_info()

    def parse_trace_file(self, file, target_core):
        prev_pid = [None] * self.num_cores * self.num_threads

        for line in sys.stdin if file is None else file:

            if line[0] == '#':
                continue
            
            parse_obj = ParseObject(line, self.num_cores, self.num_threads)

            if target_core is not None and parse_obj.core not in target_core:
                continue

            # TODO: check > is lcore correct?
            if prev_pid[parse_obj.thread] is not None and prev_pid[parse_obj.thread] != parse_obj.p_pid:
                self.pid_errors += 1

            self.sched(parse_obj.core, parse_obj.thread, parse_obj.t == 0, parse_obj.n_tgid, parse_obj.n_pid, parse_obj.n_comm, parse_obj.time)

    def print_results(self, target_tgids, target_core, program_info):
        for core in self.cores:
            if target_core is not None and core.get_number() not in target_core:
                continue

            if target_tgids is None:
                core.print_generic_results(program_info)
                # core.print_debug_info()
            else:
                print("\nCore: " + str(core.get_number()))
                for tgid in target_tgids:
                    core.print_process_info(tgid)

    def export(self, trace_file):

        export_path = os.path.splitext(trace_file)[0]

        if not os.path.exists(export_path):
            os.mkdir(export_path)

        for core in self.cores:
             core.export(export_path)

# Eviction rate does not include kernel accesses in its calculation. If kernel is scheduled, core.self.accesses is not
# incremented
