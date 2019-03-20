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
source_number = 10
# If False, read workload and content placement from data
IS_BASELINE = False

# Initialize parameters
READ_FROM_DATA = not IS_BASELINE

# Set topology
experiment['topology']['name'] = 'CCF_SCALE'
experiment['topology']['n'] = source_number

# Set workload
# ZIPF
experiment['workload'] = {
    'name':       'STATIONARY',
    'n_contents': 10 ** 5,
    'n_warmup':   10 ** 5,
    'n_measured': 2 * 10 ** 5,
    'alpha':      0.00001,
    'rate':       1,
    'is_random':  True
}
# set cache ratio
experiment['cache_placement']['network_cache'] = 0.1

if IS_BASELINE:
        # BASELINE
        # Set cache placement
        experiment['cache_placement']['name'] = 'UNIFORM'
        # Set content placement
        experiment['content_placement']['name'] = 'WEIGHTED'
        experiment['content_placement']['source_weights'] = {}
else:
        # READ FROM DATA
        # Set cache placement
        experiment['cache_placement']['name'] = 'CCF'
        experiment['cache_placement']['cache_allocation'] = [0.130905,0.110228,0.110894,0.137875,0.0552108,0.0842742,0.0973745,0.0630391,0.0576518,0.152547]
        # Set content placement
        experiment['content_placement']['name'] = 'DATA_TO_CCF'

# Set cache replacement policy
experiment['cache_policy']['name'] = 'LRU'

# Set caching meta-policy
experiment['strategy']['name'] = 'LCE'

# Description of the experiment

experiment['desc'] = "Line topology with customized cache"

# Append experiment to queue
EXPERIMENT_QUEUE.append(experiment)
