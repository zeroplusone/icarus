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
        experiment['cache_placement']['cache_allocation'] = [0.6079649086,0.0007521768689,0.0001897171169,0.0009586213567,0.00002522264754,0.0004123338621,0.0002961600498,0.00004552722054,0.00003145451477,0.0001256497548,0.00001843648887,0.0007071732784,0.00005644761402,0.00006623088116,0.00006082628364,0.0001478114065,0.00007914863316,0.00002512051968,0.0002012058691,0.00003657932547,0.00001858404306,0.0001052534919,0.002414012616,0.0005519889407,0.002188148306,0.03810444169,0.00003997569229,0.0000290655727,0.006506750281,0.0006729928155,0.0004942797334,0.00004526826336,0.0001203743673,0.006671098253,0.0001246054068,0.00002685297105,0.00006016570885,0.00004899801284,0.0000623780227,0.00004376764974,0.0002982413134,0.00785686027,0.0002524981493,0.0004883543751,0.00007388428255,0.00009099033664,0.001427456158,0.0001894123851,0.00007218105977,0.1521137035,0.0001920745677,0.00003235880602,0.00003473674911,0.01702726874,0.00004928587158,0.00004090793329,0.000138475456,0.00002379749064,0.00007719804797,0.0006107297848,0.001526834731,0.06797769317,0.0002636651477,0.00007578296745,0.001897662763,0.0002284935471,0.0001885499509,0.0001849939604,0.00003735771403,0.0002360379191,0.0008078683387,0.001136493541,0.0002282977003,0.01257778195,0.00008851643885,0.00130969445,0.0005540919006,0.002846696466,0.00071454815,0.0004407009834,0.002496419708,0.00001518622109,0.004146980907,0.0007768103325,0.00007804102484,0.0001346713376,0.03483156474,0.001748843999,0.0002176904644,0.0001035631935,0.00007013308273,0.00005333118047,0.00002181185262,0.00009378027341,0.003613754742,0.004910416051,0.0003090940839,0.0003134163048,0.001096999856,0.00002555948728]
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
