#!/usr/bin/python3 -u

import os
import sys
import numpy as np
import math

import argparse

from plot import *
from calc import *

parser = argparse.ArgumentParser(description="Analyze trace data export files")
requiredArgs = parser.add_argument_group("Required arguments")

requiredArgs.add_argument("-f", "--file", help="Input file", required=True)

optionalArgs = parser.add_argument_group("Optional arguments")

#optionalArgs.add_argument("-p", "--plot", help="Plot type")
#optionalArgs.add_argument("-t", "--type", help="Plot sub-type")
#optionalArgs.add_argument("-T", "--title", help="Plot title")

args = parser.parse_args(sys.argv[1:])

file = args.file
#plot_type = args.plot
#plot_subtype = args.type
#plot_title = args.title


config_file = open(file, "r") # close me
config = json.load(config_file)
config_file.close()

type = config["type"]

if type == "compare":
    compare_plot(config)
elif type == "tcompare":
    tcompare_plot(config)
elif type == "var":
    var_plot(config)
elif type == "dist":
    gaussian_plot(config)
elif type == "hist":
    hist_plot(config)
elif type == "ttest":
    two_sample_ttest(config)
elif type == "eval":
    central_tendency_type = get_central_tendency_type(config)
    baselines, points, _ = eval_calc(config, central_tendency_type)
    eval_plot(config, baselines, points)
elif type == "delta":
    servers = config["servers"]
    delta_points_map = {}
    for server in servers:
        config_server = servers[server]
        central_tendency_type = get_central_tendency_type(config)
        _, _, delta_points = eval_calc(config_server, central_tendency_type)
        delta_points_map[server] = delta_points

    print(delta_points_map)
    delta_plot(servers, delta_points_map)
