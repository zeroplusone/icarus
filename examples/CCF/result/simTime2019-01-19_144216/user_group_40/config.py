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
        experiment['cache_placement']['cache_allocation'] = [0.0001233081349,0.0001346984038,0.0001506334471,0.00006956848111,0.0003632986928,0.0002726122048,0.002396409227,0.003887108754,0.00005728351295,0.0002286718748,0.00008549686258,0.003401585123,0.000147039541,0.00007291592191,0.00001193902987,0.0179809876,0.1522204083,0.0002483726349,0.00004075121633,0.0004029104437,0.0001042411126,0.0002211017541,0.0001064655368,0.00001424693737,0.00003808167768,0.0001774460441,0.003547843089,0.0001156350076,0.06760873282,0.00002053442766,0.01249205611,0.0008674705626,0.0005995445215,0.00003963634382,0.00325266337,0.00002403300381,0.005073172425,0.000027249172,0.001874236833,0.00006626879523,0.0000634402337,0.001006319131,0.0001297772636,0.001424289004,0.0004496830529,0.0001687910336,0.0003569969837,0.00002650895653,0.002919611424,0.001160618176,0.00005117184815,0.00003962586354,0.002051270418,0.0001122788639,0.00009856608785,0.02463482836,0.009538513034,0.0001023658023,0.00008452438545,0.006408988778,0.0002084773471,0.00009879797475,0.007570406573,0.00008317890775,0.0008859055996,0.00007276605392,0.000434591009,0.0005109286623,0.000022254574,0.00002125151482,0.00005687484364,0.000033519539,0.00007430690798,0.00004011732669,0.0003002534689,0.0003618856455,0.0007206555315,0.00004374628663,0.00006677804301,0.0006190938743,0.0009570630946,0.0001227283774,0.001003495581,0.0006748929834,0.0002631567788,0.6081588999,0.00007102992926,0.00001887235407,0.00004844962682,0.004466083376,0.0001998528046,0.00002858596783,0.0001178453752,0.00004116062662,0.0007759434551,0.0002993694618,0.00258024104,0.03811009577,0.0001574035815,0.000284212581]
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
