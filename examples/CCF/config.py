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
DATA_COLLECTORS = ['CACHE_HIT_RATIO', 'LATENCY', 'PATH_STRETCH', 'LINK_LOAD', 'CCF']

# Queue of experiments
EXPERIMENT_QUEUE = deque()

# Create experiment
experiment = Tree()

# Set topology
experiment['topology']['name'] = 'CCF'
# experiment['topology']['n'] = 3
# experiment['topology']['delay'] = 1


# Set workload
experiment['workload'] = {
         'name':       'STATIONARY',
         'n_contents': 10 ** 5,
         'n_warmup':   10 ** 2,
         'n_measured': 4 * 10 ** 2,
         'alpha':      1.0,
         'rate':       1
        }

# Set cache placement
# experiment['cache_placement']['name'] = 'CCF'
# experiment['cache_placement']['network_cache'] = 0.0
# experiment['cache_placement']['cache_allocation'] = [0.9, 0.1]
experiment['cache_placement']['name'] = 'UNIFORM'
experiment['cache_placement']['network_cache'] = 0.0


# Set content placement
experiment['content_placement']['name'] = 'UNIFORM'
# experiment['content_placement']['name'] = 'DATA'

# If True, read workload and content placement from data 
READ_FROM_DATA = False

# Set cache replacement policy
experiment['cache_policy']['name'] = 'LRU'

# Set caching meta-policy
experiment['strategy']['name'] = 'LCE'

# Description of the experiment
experiment['desc'] = "Line topology with customized cache"

# Append experiment to queue
EXPERIMENT_QUEUE.append(experiment)
