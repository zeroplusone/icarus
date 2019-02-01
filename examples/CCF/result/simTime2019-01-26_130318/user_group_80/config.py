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
        experiment['cache_placement']['cache_allocation'] = [0,0.05409674494,0.03200427226,0.00E+00,0,0.03129239342,0.02026696584,0.0279886836,0,0,0,0,0.009597835253,0,0,0,0,0.02545678193,0.01061581344,0.03729265853,0.00402606576,0.04948154987,0.009422290664,0.006878456462,0.03041029383,0.0109449103,0.01401451679,0.005886905248,0.01567757349,0.03366850558,0.00725878821,0,0,0.01368126493,0,0,0,0.02606373731,0,0,0,0,0,0.02820192795,0.0004496896655,0,0,0.02446896407,0,0,0,0.01906074343,0,0,0,0,0,0,0,0,0,0.05189007431,0,0.01712372435,0,0,0,0,0.0124953093,0,0.05087906326,0.0402573381,0.03601146779,0,0.04002199495,0,0,0,0.002988053061,0,0.0001384467873,0.02626242747,0,0.02532980122,0,0,0.02987992238,0,0,0,0.02474250827,0,0.02880687985,0,0.0123239881,0,0.007049365098,0,0.007324669054,0.0382666339]
experiment['cache_placement']['network_cache'] = 0.1

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