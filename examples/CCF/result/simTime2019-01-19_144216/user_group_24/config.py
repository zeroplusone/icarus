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
        experiment['cache_placement']['cache_allocation'] = [0.0001125832538,0.00008724243228,0.06766842833,0.0005726696332,0.00003661123396,0.0002048137435,0.0001381621363,0.6079583387,0.0001430083478,0.0003914554881,0.0004055072693,0.00005925740343,0.0002231846887,0.00005691197332,0.00008281547684,0.06325781017,0.01702432909,0.002465075068,0.000250208766,0.001954971718,0.001800951485,0.0005441036725,0.0001330148448,0.0003095036447,0.005109894488,0.007701666205,0.003205077002,0.0002055047434,0.0001969284141,0.0003395158947,0.0003567609465,0.0007170910923,0.004744728083,0.00008753245284,0.00003331756044,0.0002462946732,0.00008359786426,0.001225571174,0.0001822120325,0.002466035526,0.00004408149455,0.00012344936,0.00002403157057,0.0003680162682,0.0000433048344,0.0004274823482,0.00003129778282,0.0001659715974,0.00005489955609,0.001570185409,0.00003924985749,0.001381902362,0.0002971058312,0.1523191188,0.0002127547669,0.0001666433987,0.000765304902,0.0003463806166,0.001958871615,0.0001593979604,0.0001846658569,0.000465715294,0.0003118210767,0.00002158040665,0.0105418995,0.00005832360977,0.0001254894581,0.001312146323,0.00002156863002,0.00001945070957,0.00002311937029,0.003164160668,0.0001017491783,0.00003565237094,0.006181806938,0.00002346106974,0.00007270815783,0.002139258394,0.00009681671772,0.00001520011094,0.00006561257271,0.001136592496,0.00005742674178,0.000107450746,0.00001775380596,0.01252286492,0.000383671049,0.0000222454722,0.0044886462,0.00002532673525,0.00006712693795,0.0001392824995,0.0002630477146,0.00009987950504,0.0002733192358,0.0002127342852,0.0007532116183,0.0008682373022,0.0002491212804,0.00004771800996]
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
