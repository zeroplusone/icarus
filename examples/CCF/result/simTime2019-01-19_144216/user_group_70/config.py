"""Configuration file for running a single simple simulation."""
from multiprocessing import cpu_count
from collections import deque
import copy
from icarus.util import Tree

# GENERAL SETTINGS

# Level of logging output
# Available options: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL = 'INFO'

# If True, executes simulations in parallel using multiple processes
# to take advantage of multicore CPUs
PARALLEL_EXECUTION = True

# Number of processes used to run simulations in parallel.
# This option is ignored if PARALLEL_EXECUTION = False
N_PROCESSES = cpu_count()

# Number of times each experiment is replicated
N_REPLICATIONS = 1

# Granularity of caching.
# Currently, only OBJECT is supported
CACHING_GRANULARITY = 'OBJECT'

# Format in which results are saved.
# Result readers and writers are located in module ./icarus/results/readwrite.py
# Currently only PICKLE is supported
RESULTS_FORMAT = 'PICKLE'

# List of metrics to be measured in the experiments
# The implementation of data collectors are located in ./icaurs/execution/collectors.py
DATA_COLLECTORS = ['CACHE_HIT_RATIO', 'LATENCY', 'PATH_STRETCH', 'LINK_LOAD']

# Queue of experiments
EXPERIMENT_QUEUE = deque()

# Create experiment
experiment = Tree()

# CCF settings 
source_number = 100
IS_BASELINE = False
# If True, read workload and content placement from data 
READ_FROM_DATA = True
IS_ZIPF = False
# Set topology
experiment['topology']['name'] = 'CCF_SCALE'
experiment['topology']['n'] = source_number
# experiment['topology']['delay'] = 1


# Set workload
# ZIPF
if IS_ZIPF:
        experiment['workload'] = {
                'name':       'STATIONARY',
                'n_contents': 10 ** 5,
                'n_warmup':   10 ** 5,
                'n_measured': 2 * 10 ** 5,
                'alpha':      2.0,
                'rate':       1,
                'is_random':   True
                }
else:
        experiment['workload'] = {
                'name':       'NORMAL',
                'n_contents': 10 ** 5,
                'n_warmup':   10 ** 5,
                'n_measured': 2 * 10 ** 5,
                'rate':       1,
                'is_random':   True
                }

# Set cache placement
if IS_BASELINE:
        experiment['cache_placement']['name'] = 'UNIFORM'
else:
        experiment['cache_placement']['name'] = 'CCF'
        experiment['cache_placement']['cache_allocation'] = [0.01745952776,0.004068267023,0.00004550922048,0.000750236497,0.001143292528,0.0002283546021,0.0000256214898,0.0005959943498,0.02616714081,0.001102801356,0.0006765128907,0.000101094349,0.00001296010022,0.0001645242849,0.00006608589427,0.00002583941722,0.0003338684186,0.0000249483106,0.000112705826,0.001167690495,0.00004865071442,0.00003385804637,0.00008696044716,0.0009414271378,0.001019850171,0.00003575368537,0.00017951285,0.0001622074671,0.0001435705663,0.0006540168853,0.00003449670171,0.00006989290397,0.00004678728632,0.0000747079225,0.6098707834,0.007529347453,0.000889472087,0.00003813012171,0.00004777821934,0.0001636810489,0.00007101975674,0.00611087719,0.0000912233298,0.00004615447105,0.0001334834509,0.0000919047825,0.0009684604575,0.000892142643,0.00002022099371,0.0001113911269,0.0007216735649,0.009570367533,0.00004730656864,0.0002117336855,0.00002098958086,0.00009582405192,0.0003603326652,0.00007709311315,0.00001321184066,0.03819487955,0.001824030704,0.00009243182681,0.0002397618678,0.002319900812,0.00002646219275,0.0002429574153,0.002901214937,0.001499783705,0.0002153056567,0.00008488513207,0.0004645288464,0.00001953230494,0.0009958321956,0.0004444015476,0.00007318745114,0.00008165342744,0.00009572878091,0.0001045756035,0.003159470146,0.01668210187,0.00009101545098,0.0003861682001,0.005164381793,0.0004420556995,0.0002045892261,0.0000380446088,0.0004417422976,0.002678700443,0.0001644055611,0.00002195405575,0.00007134234962,0.001613351361,0.0002051455002,0.002156841294,0.0005412465488,0.00007361373131,0.1522305556,0.00004129955608,0.06760976127,0.00006188794422]
experiment['cache_placement']['network_cache'] = 0.001

# Set content placement
if READ_FROM_DATA:
        experiment['content_placement']['name'] = 'DATA_TO_CCF'
else:
        if IS_ZIPF:
                experiment['content_placement']['name'] = 'UNIFORM'
                # experiment['content_placement']['name'] = 'ZIPF'
                # experiment['content_placement']['alpha'] = 2
                # experiment['content_placement']['is_random'] = True
        else:
                experiment['content_placement']['name'] = 'NORMAL'
                experiment['content_placement']['is_random'] = True
                # experiment['content_placement']['name'] = 'WEIGHTED'
                # experiment['content_placement']['source_weights'] = dic

# Set cache replacement policy
experiment['cache_policy']['name'] = 'LRU'

# Set caching meta-policy
experiment['strategy']['name'] = 'LCE'

# Description of the experiment

experiment['desc'] = "Line topology with customized cache"

# Append experiment to queue
EXPERIMENT_QUEUE.append(experiment)
