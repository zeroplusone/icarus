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
        experiment['cache_placement']['cache_allocation'] = [0.0001204618536,0.0000135848408,0.0243442368,0.0001828721683,0.01709048536,0.0001276238282,0.0002145829858,0.0001417278959,0.00002879995955,0.003210613326,0.00005618915013,0.0001195158984,0.6080108083,0.0001469052199,0.004285715437,0.000453124489,0.001413454888,0.00045639389,0.0003723207779,0.0001156877423,0.0001691319649,0.001888949172,0.0002279620995,0.00004009332361,0.0391765478,0.00002643666299,0.0001128745788,0.000273626532,0.00005196840121,0.0003316076408,0.00001886830241,0.06774622723,0.00001651011487,0.0002207485949,0.0004849748536,0.0001530322346,0.0001803061185,0.0006173622051,0.000009768320457,0.00003852826604,0.003295901036,0.00002155644535,0.0004130457718,0.0008637711728,0.0008053054668,0.0002420028203,0.00008193705363,0.00008432071742,0.00009033821154,0.00003738637749,0.0008097240186,0.01255441138,0.0001005390157,0.00003373185083,0.0005381244623,0.0000474845953,0.007975928367,0.0007468383146,0.00002000698926,0.0009477850504,0.00001736685467,0.1520885828,0.002534962118,0.00009951722308,0.00002790223994,0.000304220709,0.0001555927662,0.0001285977071,0.001671964991,0.000178261709,0.005074521207,0.00009865766514,0.0002944748121,0.0004555818553,0.00002465991264,0.01021751033,0.00006258774826,0.00004094048555,0.00005261062199,0.00002863806387,0.0006719753208,0.0002088746319,0.00007959526924,0.0002825389832,0.00007829138028,0.0000250769128,0.000097261881,0.002232257842,0.00001680282357,0.009942417595,0.00003939978709,0.0001463040416,0.00373154417,0.002271188777,0.0001208765935,0.002422773338,0.0001020211488,0.00002701039263,0.000423717368,0.001122151498]
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
