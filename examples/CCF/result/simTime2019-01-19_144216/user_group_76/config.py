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
        experiment['cache_placement']['cache_allocation'] = [0.0004458176506,0.00003149424976,0.009527183752,0.0001301671455,0.0001448987538,0.000798301597,0.0006318068773,0.001645493492,0.0250536492,0.00006571430817,0.0001174572912,0.001687338235,0.00006060680576,0.00003519493612,0.001952051163,0.005089713208,0.0002278235096,0.0001320971523,0.004649318257,0.0001157394226,0.006273825107,0.0002538591555,0.00004481022473,0.0001747107487,0.001514115821,0.0003805869276,0.00007223440623,0.00008644521367,0.0003249617107,0.00008556998046,0.001880046737,0.0005735363573,0.00008372658747,0.0009564293539,0.00001963168297,0.00005353166297,0.00008941151171,0.152476829,0.000076269862,0.0004100004392,0.0000836938277,0.00006333091723,0.0009019731047,0.0001086706879,0.0004990824996,0.0001253452513,0.0001924570467,0.0009867152056,0.00002137750334,0.00001976859592,0.01693198411,0.0006544764536,0.0001822971389,0.003637614897,0.0009866600957,0.0002032870438,0.00246264683,0.00001773004876,0.001920547643,0.6081113945,0.00004932679152,0.0007604042932,0.0004928035131,0.0002746258615,0.0008573312952,0.00006338616881,0.0007112896425,0.002147305892,0.0001247723357,0.06776766788,0.00004666236669,0.01250719131,0.0002884009117,0.00001858200505,0.00007158284773,0.00004367996235,0.0001433188615,0.001186855548,0.0001595878307,0.000238269654,0.00007576910331,0.0001115709162,0.007584729787,0.0001762660502,0.0001249094659,0.03816472628,0.00007631312057,0.00005468957652,0.0001570769383,0.00001719567095,0.003130808615,0.000247650044,0.0008279542725,0.0009316551652,0.0001391923428,0.00004141959833,0.00006108500399,0.0001845329972,0.003086873697,0.000369083451]
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
