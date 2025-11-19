L1_MISS=0
L1_HIT=1
ALL_LOADS=2
ALL_STORES=3
L1D_REPLACEMENT=4
L2_ALL_RFO=5

def load_miss(event_cnts):
    assert event_cnts.size == 8
    
    return 0 if event_cnts[L1_MISS] + event_cnts[L1_HIT] == 0 else round(100 * event_cnts[L1_MISS] / (event_cnts[L1_MISS] + event_cnts[L1_HIT]), 3)

def store_miss(event_cnts):
    assert event_cnts.size == 8
    
    return 0 if event_cnts[ALL_STORES] == 0 else round(100 * event_cnts[L2_ALL_RFO] / (event_cnts[ALL_STORES]), 3)

def replacement_rate(event_cnts):
    assert event_cnts.size == 8
    
    return 0 if event_cnts[ALL_LOADS] + event_cnts[ALL_STORES] == 0 else round(100 * event_cnts[L1D_REPLACEMENT] / (event_cnts[ALL_LOADS] + event_cnts[ALL_STORES]), 3)

def total_miss(event_cnts):
    assert event_cnts.size == 8
    
    return 0 if event_cnts[ALL_LOADS] + event_cnts[ALL_STORES] == 0 else round(100 * (event_cnts[L1_MISS] + event_cnts[L2_ALL_RFO]) / (event_cnts[ALL_LOADS] + event_cnts[ALL_STORES]), 3)