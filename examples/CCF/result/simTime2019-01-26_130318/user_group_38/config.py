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
        experiment['cache_placement']['cache_allocation'] = [0,0,0,0.01637783635,0.02336331862,0.03949819178,0.01617281876,0.02075264298,0,0,0.01903808402,0,0.0163246249,0,0.02220466364,0,0.002759406794,0,0.0108200003,4.16E-02,0.006259759409,0,0,0,0.01623432933,0,0.01816354285,0,0.003401292054,0,0.01938552264,0,0,2.45E-02,0,0.01915306339,0,0,0.03911802029,0,0,0,0,0,0,0.0002226356419,0.01933652919,0.00E+00,0.02785852725,0,0.01700942163,0,0.004681135686,0.003581754965,0.03408588232,0.03750205967,0,0,0.00461413998,0,0,0.01935380274,0.01522446528,0,0,0.03234023133,0.005522186987,0.01504760483,0,0,0.01242108019,0.00E+00,0.005867181224,0.03075022484,0,0,0.0288430121,0,0.01766580206,0.009323848485,0,0,0,0.03612323806,0.03638685687,0.001307216963,0.01771012303,0.008897387561,0,0.01562644773,0.04259913409,0.002814530583,0,0,0.03807706968,0.03929577509,0,0.003785343202,0.02723322973,0.01377476899]
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
