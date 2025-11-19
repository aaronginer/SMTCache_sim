from curses.ascii import BEL
from operator import indexOf
from os import stat
from random import random
from ssl import _create_default_https_context
from util import *
import matplotlib.pyplot as plt
import scipy
from scipy.stats import ttest_ind
import random
import math

def basic_stats(config):
    statistic = config["statistic"]

    result_dict = {}
    
    traces = config["trace"]["folders"]
    filter = config["trace"].get("filter")
    for benchmark in traces:
        benchmark_dict = {}

        parent_folder_path = traces[benchmark]

        stat_array, _ = get_folder_data(parent_folder_path, statistic, filter)

        stat_array = trim_lists(stat_array)

        benchmark_dict["a_mean"] = np.mean(stat_array)
        benchmark_dict["median"] = np.median(stat_array)
        benchmark_dict["g_mean"] = scipy.stats.mstats.gmean(stat_array)
        benchmark_dict["std"] = np.std(stat_array)

        #plt.bar(np.arange(len(stat_array)), stat_array)
        #plt.show()

        alpha = 5e-2
        _, p = scipy.stats.normaltest(stat_array)

        print(benchmark, p)

        benchmark_dict["gaussian"] = p <= alpha

        result_dict[benchmark] = benchmark_dict

    # plt.legend()
    # plt.show()
    return result_dict


def two_sample_ttest(config):
    statistic = config["statistic"]

    # benchmark -> [statistic trace 0, ...]
    stats_dict = {}
    
    traces = config["trace"]["folders"]
    filter = config["trace"].get("filter")

    assert len(traces) == 2 and "can only perform ttest on 2 input samples"

    samples = []

    for benchmark in traces:
        parent_folder_path = traces[benchmark]

        stat_array, _ = get_folder_data(parent_folder_path, statistic, filter)
        stat_array = trim_lists(stat_array)

        samples.append(stat_array)
    
    x = samples[0]
    y = samples[1]

    alpha = 0.05

    # independent non-normal
    ranksums_result = scipy.stats.ranksums(x=x, y=y, alternative="less")
    print("Ranksums: alternative=less: Reject={reject}, pvalue={pvalue}, statistic={statistic}".format(
        reject=(ranksums_result.pvalue <= alpha), pvalue=ranksums_result.pvalue, statistic=ranksums_result.statistic
    ))

    # dependent non-normal
    #wilcoxon_result = scipy.stats.wilcoxon(x=x, y=y, alternative="less")
    #print("Wilcoxon: alternative=less: Reject={reject}, pvalue={pvalue}, statistic={statistic}".format(
    #    reject=(wilcoxon_result.pvalue <= alpha), pvalue=wilcoxon_result.pvalue, statistic=wilcoxon_result.statistic
    #))

    # independent normal
    #ttest_result = scipy.stats.ttest_ind(a=x, b=y, equal_var=False, alternative="less")
    #print("Welch ttest: alternative=less: Reject={reject}, pvalue={pvalue}, statistic={statistic}".format(
    #    reject=(ttest_result.pvalue <= alpha), pvalue=ttest_result.pvalue, statistic=ttest_result.statistic
    #))

    return stats_dict

def eval_calc(config, central_tendency_type):
    filter = config["trace"].get("filter")

    assert config["trace"].get("baseline_low") is not None
    assert config["trace"].get("baseline_high") is not None
    assert config["trace"].get("benchmarks") is not None

    baseline_low, _ = get_folder_data(config["trace"]["baseline_low"], "lmr", filter)
    baseline_low = trim_lists(baseline_low)
    baseline_high, _ = get_folder_data(config["trace"]["baseline_high"], "lmr", filter)
    baseline_high = trim_lists(baseline_high)

    ct_low = central_tendency(baseline_low, central_tendency_type)
    ct_high = central_tendency(baseline_high, central_tendency_type)

    baselines = [(0, ct_low), 
                 (100, ct_high)]
    points = {}
    delta_points = {}

    benchmark_info = {}

    benchmarks = config["trace"]["benchmarks"]
    color = config["trace"].get("color")

    for benchmark in benchmarks:
        assert benchmarks[benchmark].get("l1e") is not None
        assert benchmarks[benchmark].get("ssv") is not None

        l1e, _ = get_folder_data(benchmarks[benchmark]["l1e"], "lmr", filter)
        l1e = trim_lists(l1e)
        ssv, _ = get_folder_data(benchmarks[benchmark]["ssv"], "er", filter)
        ssv = trim_lists(ssv)

        print(ssv)

        ct_l1e = central_tendency(l1e, central_tendency_type)
        ct_ssv = central_tendency(ssv, central_tendency_type)

        print(ct_ssv)

        l1e_conf = scipy.stats.norm.interval(confidence=0.95, loc=ct_l1e, scale=scipy.stats.sem(l1e))
        ssv_conf = scipy.stats.norm.interval(confidence=0.95, loc=ct_ssv, scale=scipy.stats.sem(ssv))


        benchmark_info[benchmark] = {
            "mean_lmr": ct_l1e,
            "mean_lmr_error": (l1e_conf[1] - l1e_conf[0]) / 2,
            "mean_er": round(ct_ssv, 3),
            "mean_er_error": (ssv_conf[1] - ssv_conf[0]) / 2
        }

        print(benchmark)

        print("L1E: ", round(ct_l1e, 6), round((l1e_conf[1] - l1e_conf[0]) / 2, 6))
        print("SSV: ", round(ct_ssv, 6), round((ssv_conf[1] - ssv_conf[0]) / 2, 6))

        print("Scaled difference to lower bound baseline:")
        diff_lower_bound = ct_l1e - ct_low
        # assert ct_high > ct_low
        baselines_segment_len = ct_high - ct_low # = 1 DELTA
        print(round(diff_lower_bound / baselines_segment_len * 100, 2))

        delta_diff = diff_lower_bound / baselines_segment_len

        print("Gain/Loss")
        shift = baselines_segment_len * ct_ssv
        simulated_l1e = ct_low + shift
        print(simulated_l1e, ct_l1e, ct_low, ct_high)
        print(round((simulated_l1e - ct_l1e) / ct_l1e * 100, 2))
        
        benchmark_info[benchmark]["change"] = (simulated_l1e - ct_l1e) / ct_l1e * 100

        # shift the baseline samples by eviction rate * segment size
        simulated_l1e_arr = baseline_low + shift

        assert abs((central_tendency(simulated_l1e_arr, central_tendency_type) - shift) - ct_low) < 0.0000001

        alpha = 0.05

        ranksums_result = scipy.stats.ranksums(x=simulated_l1e, y=l1e, alternative="less")
        print("Ranksums: alternative=less: Reject={reject}, p={pvalue}, 1-p={pneg}".format(
            reject=(ranksums_result.pvalue <= alpha), pvalue=ranksums_result.pvalue, pneg=1-ranksums_result.pvalue
        ))

        benchmark_info[benchmark]["p_value_less"] = ranksums_result.pvalue
        benchmark_info[benchmark]["less_reject"] = ranksums_result.pvalue < alpha
        benchmark_info[benchmark]["greater_reject"] = (1 - ranksums_result.pvalue) < alpha

        ranksums_result = scipy.stats.ranksums(x=simulated_l1e, y=l1e)
        print("Ranksums: alternative=different: Reject={reject}, p={pvalue}, 1-p={pneg}".format(
            reject=(ranksums_result.pvalue <= alpha), pvalue=ranksums_result.pvalue, pneg=1-ranksums_result.pvalue
        ))


        points[benchmark] = (ct_ssv, ct_l1e, ct_l1e > simulated_l1e)
        delta_points[benchmark] = (ct_ssv, delta_diff, ct_l1e > simulated_l1e, color)

    print("Benchmark\tMean LMR\t\tMean ER\t\t\tChange\t pvalue (less)\t< reject\t > reject")
    for benchmark in benchmark_info:
        print("        {b} & {mean_lmr:.3f} ($\\pm${pm_lmr:.3f}) & {mean_er:.3f} ($\\pm${pm_er:.3f}) & {change:+.3f}\\% & {pvalue:.4f} & {less_reject} & {greater_reject} \\\\\n        \\hline".format(
            b = benchmark.replace("_", "\_"),
            mean_lmr=benchmark_info[benchmark]["mean_lmr"],
            pm_lmr=0 if math.isnan(benchmark_info[benchmark]["mean_lmr_error"]) else benchmark_info[benchmark]["mean_lmr_error"],
            mean_er=benchmark_info[benchmark]["mean_er"],
            pm_er=0 if math.isnan(benchmark_info[benchmark]["mean_er_error"]) else benchmark_info[benchmark]["mean_er_error"],
            plus="+" if benchmark_info[benchmark]["change"] > 0 else "",
            change=benchmark_info[benchmark]["change"],
            pvalue=benchmark_info[benchmark]["p_value_less"],
            less_reject="T" if benchmark_info[benchmark]["less_reject"] else "F",
            greater_reject="T" if benchmark_info[benchmark]["greater_reject"] else "F"
        ))

    return baselines, points, delta_points