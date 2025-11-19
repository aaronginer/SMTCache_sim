#!/usr/bin/python3 -u


import numpy as np
import sys
import matplotlib.pyplot as plt
import scipy

freq = 4200000000
ns_ps = 1000000000 / freq

def get_mean(file_name):
    tsc_arr = []
    f = open(file_name, 'r')

    for line in f.readlines():
        tsc = float(line)
        tsc_arr.append(tsc)

    mean = np.mean(tsc_arr)
    std = np.std(tsc_arr)
    res = scipy.stats.norm.interval(confidence=0.95, loc=mean, scale=scipy.stats.sem(tsc_arr))

    return mean, std, res

def mean_diff(file_name1, file_name2):
    tsc_arr1 = []
    tsc_arr2 = []
    f1 = open(file_name1, 'r')
    f2 = open(file_name2, 'r')

    for line in f1.readlines():
        tsc = float(line)
        tsc_arr1.append(tsc)

    for line in f2.readlines():
        tsc = float(line)
        tsc_arr2.append(tsc)

    print(np.mean(tsc_arr1), np.mean(tsc_arr2))
    tsc_diff_arr = np.subtract(np.array(tsc_arr2), np.array(tsc_arr1))

    mean = np.mean(tsc_diff_arr)
    sem = scipy.stats.sem(tsc_diff_arr)
    res = scipy.stats.norm.interval(confidence=0.95, loc=mean, scale=scipy.stats.sem(tsc_diff_arr))

    return mean, sem, res

files_0 = ["normal_l1d_flush_0.b", "cc_l1d_flush_0.b"]
files_16 = ["normal_l1d_flush_16.b", "cc_l1d_flush_16.b"]
files_32 = ["normal_l1d_flush_32.b", "cc_l1d_flush_32.b"]
files_48 = ["normal_l1d_flush_48.b", "cc_l1d_flush_48.b"]
files_64 = ["normal_l1d_flush_64.b", "cc_l1d_flush_64.b"]

sets = [files_0, files_16, files_32, files_48, files_64]
sets_n = [0, 16, 32, 48, 64]

sets_r = []
sets_sem = []

for i in range(len(sets)):
    mean, sem, ci = mean_diff(sets[i][0], sets[i][1])

    sets_r.append(ns_ps * mean)
    sets_sem.append(sem)


plt.xlabel("sets accessed")
plt.ylabel("L1D flush time (ns)")

x = np.arange(len(sets_r))  # the label locations

# plt.bar(x, sets_r, yerr=sets_sem, capsize=7, color="gray")
plt.bar(x, sets_r, color="gray")

plt.ylim(300, 600)
plt.xticks(x, sets_n)

plt.show()

#plt.yscale("log")
#plt.hist(tsc_arr, bins=10000)
#plt.xlim(mean - std, mean + std)
#plt.show()