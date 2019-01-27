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
        experiment['cache_placement']['cache_allocation'] = [0.00003047809776,0.000006888297109,0.00974871913,0.0005530759729,0.0006141491023,0.06761296099,0.0001493403142,0.0001702738854,0.00005810595004,0.0003881232057,0.0001100103844,0.0004340858294,0.0001186396429,0.00005020667124,0.00003987465881,0.00001378364717,0.001880997036,0.00005817253138,0.0001163417137,0.0001885126724,0.0004001229906,0.003321641925,0.000451930791,0.00004486535608,0.02194128763,0.0000431390652,0.0001981744283,0.0002021348277,0.002179055561,0.0001881289369,0.00003674670992,0.00006927487144,0.000136450856,0.0001533320892,0.0003858632708,0.00008512788037,0.00005264636631,0.0001623561839,0.0006880724502,0.01246169474,0.00001476670231,0.0002504404494,0.00006730169823,0.001090743235,0.00005262996358,0.6086525071,0.00001621573232,0.0002572193685,0.002234908358,0.00002967744947,0.0002948838052,0.001321213182,0.0001075835256,0.04628583498,0.00004319729856,0.007876729903,0.00107933701,0.0001719658008,0.00005620306644,0.003702330539,0.001005662441,0.0001145298869,0.00001709010636,0.00009432809233,0.00003184253513,0.0008029954938,0.0003655621283,0.001040382642,0.02441076558,0.0003220119616,0.001555196062,0.0006141027077,0.004339598879,0.0005790350274,0.0000651397151,0.0001322307746,0.0000253431715,0.000922557384,0.0007357855348,0.0001662223737,0.000844711191,0.001905561487,0.0001038548915,0.0001028487872,0.0002821548041,0.00006694273143,0.0001013276536,0.002399544397,0.1522281942,0.00005167310043,0.00008739039091,0.0002671808484,0.001286444185,0.00003990708305,0.000192280036,0.002863520995,0.000451624369,0.0001062122633,0.00006167335555,0.00006609490876]
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
