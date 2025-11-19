#!/bin/bash

l1_miss=0x004308d1
l1_hit=0x004301d1
# no kernel
l1_miss_u=0x004108d1
l1_hit_u=0x004101d1
# no user
l1_miss_k=0x004208d1
l1_hit_k=0x004201d1

all_loads=0x004381d0
all_loads_u=0x004181d0
all_stores=0x004382d0
inst_retired=0x004300c0
inst_retired_u=0x004100c0
l1d_replacement=0x00430151
l2_all_rfo=0x0043e224
fb_hit=0x004340d1

disable_mask=~0x400000

evtsel0=0x186
evtsel1=0x187
evtsel2=0x188
evtsel3=0x189
evtsel4=0x18a
evtsel5=0x18b

wrmsr --all $evtsel0 $l1_miss
wrmsr --all $evtsel1 $l1_hit
wrmsr --all $evtsel2 $inst_retired
wrmsr --all $evtsel3 $all_stores
wrmsr --all $evtsel4 $l1d_replacement
wrmsr --all $evtsel5 $l2_all_rfo
