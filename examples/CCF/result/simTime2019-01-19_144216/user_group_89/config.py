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
        experiment['cache_placement']['cache_allocation'] = [0.0003899083489,0.00008222234778,0.0001800909722,0.001649636556,0.00008711568093,0.1526940715,0.0001404814451,0.00002577297794,0.0001737255462,0.001002122341,0.00003163029732,0.00006013832359,0.6115522269,0.0004192801167,0.00005574696089,0.00003205054697,0.0001535417034,0.0004768481825,0.0009335370894,0.00004128555358,0.000117524878,0.00005327367917,0.00002194075776,0.00510345191,0.0005805845136,0.006334675817,0.0001381296985,0.0001214165863,0.000249830328,0.002429121434,0.0009354809443,0.00009990874175,0.0312404374,0.0001730780201,0.0001357836601,0.0001644983299,0.00007319491971,0.0001245363264,0.000126596027,0.00002502075831,0.0001365888608,0.0001732724719,0.00003947998872,0.0007339022273,0.0002911758167,0.00002841554025,0.000719616328,0.0001332002729,0.00001864881961,0.0003102331578,0.000009517700805,0.0003333858336,0.07189177697,0.00004692401262,0.00002095059283,0.03801438559,0.0007352753609,0.0003760843052,0.00008206118512,0.00009592318531,0.001574169614,0.003098436034,0.003288338973,0.002114737095,0.001779929603,0.0002809297242,0.001921906675,0.0005937383275,0.00002910316508,0.0002304066754,0.0001184461744,0.0002056475082,0.0002682243934,0.001301303855,0.0000681332196,0.01690332887,0.00005300231653,0.0126371854,0.0001240462711,0.00003367451433,0.0001130961162,0.00003483186031,0.00003409812724,0.00006271100078,0.0001312782913,0.001215749883,0.01714933192,0.0001738316944,0.0002445832466,0.00002413078117,0.0000361916957,0.00004603604675,0.00006825128946,0.00003875444369,0.0002483560488,0.00006756402019,0.0005076660298,0.00003142085989,0.0000627428863,0.0004639490464]
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
