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
        experiment['cache_placement']['cache_allocation'] = [0.02072703124,0.0322529344,0,0,0.00008204816967,0.00000003017350109,0.00245050494,0.001886603834,0.006712464474,0.02150559939,0.0001854193386,0,0.001264511726,0.03059530227,0.04374682614,0,0.00002910970964,0,0.001957227034,0.00002177503089,0,0.0007615148319,0.000121655419,0,0.005601616512,0.0007052459077,0,0.05087494087,0.00002112846375,0,0.000006888112099,0,0.0305613776,0.04682448092,0.006223387427,0.02917834207,0.003426801689,0,0.03457872175,0.002674398116,0.0144656653,0,0.0000396139893,0.0004772014197,0.03891365535,0.0001337815031,0,0.01240374596,0.01543260797,0.01297160765,0,0,0.0008575582587,0.03997222752,0.003485654156,0.03985399606,0.00566336696,0,0.04063362164,0.004596324976,0.02375836564,0,0.001081109087,0.0004235395253,0,0.02482631443,0.01658530731,0,0.04791459276,0,0,0.0006857068688,0,0,0,0.0001021790465,0.0001209908401,0.008570938032,0.004206975784,0,0.01944873752,0.00000002528965151,0,0,0.0002164835339,0,0.0003709038791,0.007706398957,0.0001478603978,0.04537016553,0.0002813927594,0.01077239658,0.000113996803,0.01062198525,0.03411264971,0.04384573598,0.04798422742,0,0.04585250482,0]
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