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
        experiment['cache_placement']['cache_allocation'] = [0.000523269237,0.0006104984501,0.00002481080968,0.00127466925,0.00005160330431,0.0009937728213,0.00009199070168,0.001147654154,0.0001769372644,0.00006867153934,0.0006635558779,0.0003633223127,0.6079684971,0.002723953419,0.00003357060766,0.0005282394008,0.0001004196175,0.00002896429697,0.0008238199625,0.0003043111777,0.0001269038617,0.000286200668,0.0009522199415,0.0003801632763,0.007608036266,0.03803322943,0.0001107915325,0.0006215201341,0.009518336082,0.0004312558262,0.0002405992991,0.0003994811677,0.0001817920486,0.0000690168513,0.0006129857473,0.0001908665743,0.0002435279036,0.007677326563,0.0002079884165,0.00009709537403,0.0001584149973,0.0001103232069,0.006113040838,0.000343962287,0.0001262116297,0.00003323739792,0.0001076969009,0.0001006289824,0.00003648096533,0.00001702186998,0.06777010808,0.0002206702367,0.000108100799,0.0007102145764,0.00008416008314,0.001716020725,0.00008016443733,0.0000642540827,0.00009522804006,0.00006363850649,0.002442648167,0.0001940048715,0.0005088417036,0.0003350680979,0.00006877778343,0.0001432841828,0.00003949045208,0.00003986724265,0.00004160175208,0.001480828705,0.1521858047,0.0001398041489,0.005237037387,0.00006262408204,0.0000444595896,0.001502855055,0.00004094550237,0.00003354526584,0.0009118629242,0.00003509464572,0.001956087053,0.0001331672029,0.00002522737683,0.0000977364869,0.02517652885,0.00164819407,0.002312837727,0.00001415115669,0.0006518825097,0.02994024732,0.0005652597078,0.003846497397,0.0001610845133,0.00001240762824,0.001744487593,0.0002553113573,0.0007203622692,0.0000703877723,0.0002271448465,0.0004011039889]
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
