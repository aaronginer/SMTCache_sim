class ParseObject:
    def __init__(self, line, cores, cpus_per_core):
        line_split = line.replace("\t", "").replace("\n", "").replace("\r", "").split(',')

        time_split = line_split[0].split(".")
        time_micro = int(time_split[0]) * 1000000 + int(time_split[1])
        self.time = time_micro / 1000000
        self.thread = int(line_split[1]) % (cores * cpus_per_core)              ## e.g.: 7 % (4*2) = 7. 7 % (4*1) = 3. 5 % (1*1) = 0.
        self.core = self.thread % cores                                       ## e.g.: 7 % 4 = 3. 7 % 2 = 1. 6 % 4 = 2. 4 % 1 = 0.
        self.f = int(line_split[2])
        self.p_pid = int(line_split[3])
        self.p_tgid = int(line_split[4])
        self.p_comm = line_split[5]
        self.t = int(line_split[6])
        self.n_pid = int(line_split[7])
        self.n_tgid = int(line_split[8])
        self.n_comm = line_split[9]

    def print(self):
        print(str(self.time)+","+str(self.thread)+","+str(self.core)+","+str(self.f)+","+str(self.p_pid)+","+str(self.p_tgid)+","+self.p_comm+","+str(self.t)+","+str(self.n_pid)+","+str(self.n_tgid)+","+self.n_comm)