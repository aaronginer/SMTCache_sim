import itertools
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patches as mpatches
from adjustText import adjust_text
import json
import numpy as np
import os
from util import *
from calc import *

def compare_plot(config):
    
    title = config["title"]
    statistic = config["statistic"]
    central_tendency_type = get_central_tendency_type(config)

    x_labels = []
    
    bars_dict = {}
    bars = config["bars"]
    for bar in bars:
        bars_dict[bar] = []    # init dict

    traces = config["trace"]

    for t in traces:
        
        for bar in bars:
            assert bar in traces[t]["folders"] and "All defined bars must be present for each comparison"
        
        # data = [] bp -> belongs to boxplot
        for bar in bars:
            parent_folder_path = traces[t]["folders"][bar]
            filter = traces[t].get("filter")
 
            stat_array, _ = get_folder_data(parent_folder_path, statistic, filter)
            stat_array = trim_lists(stat_array)

            ct = central_tendency(stat_array, central_tendency_type)

            if statistic == "ps":
                ct = int(ct)
            bars_dict[bar].append(ct)

            res = scipy.stats.norm.interval(confidence=0.95, loc=ct, scale=scipy.stats.sem(stat_array)) 
            print(t, bar)
            print(ct, res, round((res[1] - res[0]) / 2, 4))

            # data.append(stat_array) bp

        # plt.boxplot(x=data, labels=list(bars_dict.keys())) bp
        # plt.show() bp
        x_labels.append(t)

    x = np.arange(len(x_labels))  # the label locations

    group_size = len(bars_dict)
    bar_width = 0.7 / group_size

    fig, ax = plt.subplots()
        
    print(bars_dict)
    for index, bar_label in enumerate(bars_dict):
        rect = ax.bar(x - ((bar_width*(group_size-1))/2) + (index * bar_width), bars_dict[bar_label], width=bar_width, color="grey", label=bar_label)
        
        ax.bar_label(rect, padding=3)
   
    # ax.set_ylabel(statistic, fontsize=15)
    ax.set_ylabel("processes spawned")
    ax.set_title(title)
    ax.set_xticks(x, x_labels) #, fontsize=15)

    # plt.yscale("log")

    fig.tight_layout()
    # plt.legend()
    plt.show()


def tcompare_plot(config):
    title = config["title"]
    statistic = config["statistic"]
    central_tendency_type = get_central_tendency_type(config)
    
    statistic = config["statistic"]

    traces = config["trace"]["folders"]
    filter = config["trace"].get("filter")

    thread_filter = config.get("thread_filter")

    benchmarks_dict = {}
    all_threads = set()
    for benchmark in traces:
        parent_folder_path = traces[benchmark]

        _, folders_dict = get_folder_data(parent_folder_path, statistic, filter)

        benchmarks_dict[benchmark] = {}

        for folder in folders_dict:
            for file in folders_dict[folder]:
                processes = folders_dict[folder][file]["processes"]
                
                # extract thread hits and misses over an entire folder
                threads_data = {}
                for process in processes:
                    threads = processes[process]["threads"]
                    for thread in threads:
                        t_data = threads[thread]
                        t_name = t_data["name"]
                        if thread_filter is not None and t_name not in thread_filter:
                            continue

                        all_threads.add(t_name)
                        hit = 0 if t_data.get("hit") is None else t_data.get("hit")
                        miss = 0 if t_data.get("miss") is None else t_data.get("miss")
                        sched = 0 if t_data.get("sched") is None else t_data.get("sched")
                        time = 0 if t_data.get("time") is None else t_data.get("time")
                        loads = 0 if t_data.get("load_all") is None else t_data.get("load_all")
                        inst = 0 if t_data.get("inst") is None else t_data.get("inst")
                        if t_name not in threads_data:
                            threads_data[t_name] = {
                                "hit": hit,
                                "miss": miss,
                                "sched": sched,
                                "time": time,
                                "loads": loads,
                                "inst": inst
                            }
                        else:
                            threads_data[t_name]["hit"] += hit
                            threads_data[t_name]["miss"] += miss
                            threads_data[t_name]["sched"] += sched
                            threads_data[t_name]["time"] += time
                            threads_data[t_name]["loads"] += loads
                            threads_data[t_name]["inst"] += inst

                for thread in threads_data:
                    if thread not in benchmarks_dict[benchmark]:
                        benchmarks_dict[benchmark][thread] = {
                            "stat_array": []
                        }
                    miss = threads_data[thread]["miss"]
                    hit = threads_data[thread]["hit"]
                    sched = threads_data[thread]["sched"]
                    time = threads_data[thread]["time"]
                    inst = threads_data[thread]["inst"]
                    loads = threads_data[thread]["loads"]
                    if statistic == "lmr":
                        benchmarks_dict[benchmark][thread]["stat_array"].append(miss / (hit + miss))
                    elif statistic == "time":
                        benchmarks_dict[benchmark][thread]["stat_array"].append(time / sched)
                    elif statistic == "sched":
                        benchmarks_dict[benchmark][thread]["stat_array"].append(sched)
                    elif statistic == "Instructions per Schedule":
                        if inst <= 0:
                            continue
                        benchmarks_dict[benchmark][thread]["stat_array"].append(inst / sched)
                    elif statistic == "lps":
                        if loads <= 0:
                            continue
                        benchmarks_dict[benchmark][thread]["stat_array"].append(loads / sched)
                    elif statistic == "lmpi":
                        if inst <= 0:
                            continue
                        benchmarks_dict[benchmark][thread]["stat_array"].append((miss / (hit + miss)) / inst)

    for benchmark in benchmarks_dict:
        for thread in benchmarks_dict[benchmark]:
            stat_array = benchmarks_dict[benchmark][thread]["stat_array"]

            stat_array = trim_lists(stat_array)

            benchmarks_dict[benchmark][thread]["stat"] = central_tendency(stat_array, central_tendency_type)

    groups_dict = {}

    for benchmark in benchmarks_dict:
        for thread in sorted(all_threads):
            if thread not in groups_dict:
                groups_dict[thread] = []
            if thread not in benchmarks_dict[benchmark]:
                groups_dict[thread].append(0)
            else:
                groups_dict[thread].append(benchmarks_dict[benchmark][thread]["stat"])

    bars_dict = {}
    for index, (benchmark, thread) in enumerate(benchmarks_dict.items()):
        if benchmark not in bars_dict:
            bars_dict[benchmark] = []
        for thread in groups_dict:
            try:
                bars_dict[benchmark].append(groups_dict[thread][index])
            except:
                # print(benchmark, thread)
                bars_dict[benchmark].append(0) # thread was not present in benchmark

    xlabels = list(groups_dict.keys())
    x = np.arange(len(xlabels))  # the label locations

    group_size = len(bars_dict)
    bar_width = 0.7 / group_size

    fig, ax = plt.subplots()

    for index, bar_label in enumerate(bars_dict):

        rect = ax.bar(x - ((bar_width*(group_size-1))/2) + (index * bar_width), bars_dict[bar_label], width=bar_width, label=bar_label)
        ax.bar_label(rect, padding=3)
   
    ax.set_ylabel(statistic)
    # ax.set_title(title)
    ax.set_xticks(x, xlabels)
   
    ax.legend()

    fig.tight_layout()

    plt.show()


def hist_plot(config):
    title = config["title"]
    statistic = config["statistic"]
    thread_filter = config.get("thread_filter")

    plt.title(title)

    traces = config["trace"]["folders"]
    filter = config["trace"].get("filter")

    for benchmark in traces:
        parent_folder_path = traces[benchmark]

        stat_array, _ = get_folder_data(parent_folder_path, statistic, filter, thread_filter)

        stat_array = trim_lists(stat_array)

        plt.hist(stat_array, label=benchmark, alpha=0.5)
        
        res = scipy.stats.norm.interval(confidence=0.95, loc=np.mean(stat_array), scale=scipy.stats.sem(stat_array)) 
        plt.axvline(x=res[0], color="black")
        plt.axvline(x=res[1], color="black")
        plt.axvline(x=np.mean(stat_array), color="red")

    handles, _ = plt.gca().get_legend_handles_labels()

    mean_line = Line2D([0], [0], label='mean', color="red")
    ci_line = Line2D([0], [0], label='95% CI', color="black")

    handles.extend([mean_line, ci_line])

    plt.xlabel(statistic)
    if statistic == "lmr":
        plt.xlabel("load miss ratio")

    plt.ylabel("# observations")
    plt.legend(handles=handles)
    plt.show()

def var_plot(config):
    title = config["title"]
    statistic = config["statistic"]
    outliers = config.get("outliers")

    filter = config["trace"].get("filter")
    parent_folder_path = config["trace"]["folder"]

    stat_array, _ = get_folder_data(parent_folder_path, statistic, filter)

    if outliers is not None and outliers == "no":
        stat_array_copy = list(stat_array)
        stat_array = trim_lists(stat_array)
        stat_array = [e for e in stat_array_copy if e in stat_array]

    # print(stat_array)
    print("STD:", np.std(stat_array))
    print("STE: {:.7f}".format(scipy.stats.sem(stat_array)))
    print("IRQ:", scipy.stats.iqr(stat_array))

    # matplotlib.rcParams.update({'font.size': 12})
    x = np.arange(len(stat_array))
    plt.bar(x, stat_array, color="grey")
    # plt.hlines([np.mean(stat_array)], [-1], [len(stat_array)], ["red"])
    plt.ylim(np.mean(stat_array)-0.005, np.mean(stat_array)+0.002)
    plt.xlabel("run")
    plt.ylabel("load miss ratio")
    # plt.title(title+str(round(np.std(stat_array), 5)))
    plt.show()

def eval_plot(config, baselines, points):
    base_x = [baselines[0][0], baselines[1][0]]
    base_y = [baselines[0][1], baselines[1][1]]

    plt.plot(base_x, base_y, marker="o", markerfacecolor="red", alpha=0.5, markeredgecolor="black", color="red", label="baselines")

    cpc3_b = []
    cpc4_b = []
    cpc5_b = []

    cpc3_x = []
    cpc4_x = []
    cpc5_x = []
    
    cpc3_y = []
    cpc4_y = []
    cpc5_y = []

    cpc3_c = []
    cpc4_c = []
    cpc5_c = []

    for benchmark in points:
        if "cpc3" in benchmark:
            cpc3_x.append(points[benchmark][0] * 100)
            cpc3_y.append(points[benchmark][1])
            cpc3_c.append("green" if points[benchmark][2] else "red")
            cpc3_b.append(benchmark)
        elif "cpc4" in benchmark:
            cpc4_x.append(points[benchmark][0] * 100)
            cpc4_y.append(points[benchmark][1])
            cpc4_c.append("green" if points[benchmark][2] else "red")
            cpc4_b.append(benchmark)
        else:
            cpc5_x.append(points[benchmark][0] * 100)
            cpc5_y.append(points[benchmark][1])
            cpc5_c.append("green" if points[benchmark][2] else "red")
            cpc5_b.append(benchmark)


    text_labels = []

    if len(cpc3_x) > 0:
        for x, y, c, b in zip(cpc3_x, cpc3_y, cpc3_c, cpc3_b):
            plt.scatter(x, y, marker="*", color=c)
            text_labels.append(plt.text(x, y, b))
    if len(cpc4_x) > 0:
        for x, y, c, b in zip(cpc4_x, cpc4_y, cpc4_c, cpc4_b):
            plt.scatter(x, y, marker="+", color=c)
            text_labels.append(plt.text(x, y, b))
    if len(cpc5_x) > 0:
        for x, y, c, b in zip(cpc5_x, cpc5_y, cpc5_c, cpc5_b):
            plt.scatter(x, y, marker="x", color=c)
            text_labels.append(plt.text(x, y, b))

    adjust_text(text_labels, only_move={'points':'y', 'texts':'y'})

    plt.hlines([base_y], [0], [100])

    plt.xlabel("MultiCache Simulated Eviction Rate")
    plt.ylabel("Load Miss Rate")
    plt.legend()
    # plt.savefig(config["title"]+".png")
    plt.show()

def delta_plot(servers, delta_points_map):
    base_x = [0, 100]
    base_y = [0, 1]

    plt.plot(base_x, base_y, marker="o", markerfacecolor="red", alpha=0.5, markeredgecolor="black", color="red", label="baselines")

    x = []
    y = []
    c = []
    s = []

    for server in servers:
        delta_points = delta_points_map[server]
        for benchmark in delta_points:
            x.append(delta_points[benchmark][0] * 100)
            y.append(delta_points[benchmark][1])
            #c.append("green" if delta_points[benchmark][2] else "red")
            c.append("black" if delta_points[benchmark][3] is None else delta_points[benchmark][3])
            s.append("*" if "SMT" in benchmark else "+")

    for x, y, c, s in zip(x, y, c, s):
        plt.scatter(x, y, marker=s, color=c)

    handles, _ = plt.gca().get_legend_handles_labels()

    #smt_marker = Line2D([], [], color='black', marker='*', linestyle='None',
    #                      markersize=8, label='SMT') 
    #nonsmt_marker = Line2D([], [], color='black', marker='+', linestyle='None',
    #                      markersize=8, label='non-SMT')

    app_marker = Line2D([], [], color='blue', markersize=8, marker='.', linestyle='None',label='App')
    db_marker = Line2D([], [], color='orange', markersize=8, marker='.', linestyle='None',label='DB')
    file_marker = Line2D([], [], color='green', markersize=8, marker='.', linestyle='None',label='File')
    mail_marker = Line2D([], [], color='red', markersize=8, marker='.', linestyle='None',label='Mail')
    stream_marker = Line2D([], [], color='purple', markersize=8, marker='.', linestyle='None',label='Stream')
    web_marker = Line2D([], [], color='cyan', markersize=8, marker='.', linestyle='None',label='Web')

    '''
    handles.extend([smt_marker, 
        nonsmt_marker, 
        app_marker,
        db_marker,
        file_marker,
        mail_marker,
        stream_marker,
        web_marker
    ])
    '''
    handles.extend([app_marker,
        db_marker,
        file_marker,
        mail_marker,
        stream_marker,
        web_marker
    ])

    
    plt.xlabel("MultiCache Simulated Eviction Rate (%)")
    plt.ylabel(r"Change ($\delta$)")
    plt.legend(handles=handles)
    plt.show()

def gaussian_plot(config):
    statistics_dict = basic_stats(config)

    for benchmark in statistics_dict:
        print(benchmark, statistics_dict[benchmark]["gaussian"])
        Gaussian.plot(statistics_dict[benchmark]["a_mean"], statistics_dict[benchmark]["std"], legend_label=benchmark)

    # plt.savefig(config["title"]+".png")
    plt.show()


# https://stackoverflow.com/questions/53152190/drawing-multiple-univariate-normal-distribution

class Gaussian:
  @staticmethod
  def plot(mean, std, lower_bound=None, upper_bound=None, resolution=None,
    title=None, x_label=None, y_label=None, legend_label=None, legend_location="best"):
    
    lower_bound = ( mean - 4*std ) if lower_bound is None else lower_bound
    upper_bound = ( mean + 4*std ) if upper_bound is None else upper_bound
    resolution  = 100
    
    title        = title        or "Gaussian Distribution"
    x_label      = x_label      or "x"
    y_label      = y_label      or "N(x|μ,σ)"
    legend_label = legend_label + " μ={}, σ={}".format(mean, std)
    
    X = np.linspace(lower_bound, upper_bound, resolution)
    dist_X = Gaussian._distribution(X, mean, std)
    
    plt.title(title)
    
    plt.plot(X, dist_X, label=legend_label)
    
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend(loc=legend_location)
    
    return plt
  
  @staticmethod
  def _distribution(X, mean, std):
    return 1./(np.sqrt(2*np.pi)*std)*np.exp(-0.5 * (1./std*(X - mean))**2)