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
        experiment['cache_placement']['cache_allocation'] = [0.0002529991375,0.0002148173492,0.0127376061,0.0001929138412,0.00005895934192,0.03814349926,0.0009186009507,0.001431181914,0.0007441795281,0.00006565452403,0.00005886735405,0.00002020141037,0.6084726857,0.00001302497309,0.00008459168865,0.003631218619,0.0001512934869,0.0001857838426,0.0001855742139,0.0001877780248,0.0008800841843,0.002435089457,0.0002549915505,0.003287602998,0.0009831149118,0.01726942377,0.00007273094756,0.00007172965966,0.0004870583691,0.1526747544,0.001286887587,0.0003556736814,0.0003712987094,0.0003011779273,0.00006859334407,0.00538736105,0.02440417381,0.00007825260243,0.0008439770488,0.00003433394666,0.00004710861247,0.0018170226,0.00004150837424,0.00004716734718,0.00009117783832,0.00007145896264,0.00002362800697,0.000191403697,0.00003307955028,0.0002562972894,0.009869317843,0.0001133167973,0.00007271346055,0.0003070413872,0.00004517821223,0.0007472582241,0.00008305158047,0.00009381405107,0.0002971980279,0.002292211547,0.004770435772,0.00007305489602,0.00004879410587,0.00005512998166,0.0001281323256,0.0001497124236,0.0003257142989,0.0006512964166,0.0002055680546,0.001296000786,0.003621970644,0.00008163219247,0.0001814962806,0.00005229653651,0.0002059531593,0.0001162005578,0.0001189624602,0.0001911103326,0.0000912423125,0.00126829125,0.0004947873138,0.001101616445,0.000501807911,0.00002868538217,0.0001318710484,0.0001455625445,0.0001070109602,0.06764359314,0.00004052904484,0.002131542594,0.0001518640373,0.01368917544,0.002712710644,0.00003543654306,0.0000170898347,0.001310711337,0.00004663510413,0.00003256715364,0.00002891469921,0.0001741993765]
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
