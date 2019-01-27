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
        experiment['cache_placement']['cache_allocation'] = [0.00001890615725,0.00003727960747,0.0001227030952,0.001611209217,0.00006810551904,0.0002920909081,0.004317449414,0.0006968184271,0.0001020344994,0.0001437438592,0.0004530468123,0.001365224117,0.00004251887598,0.001081099067,0.0002413703487,0.00006346937753,0.00001375890898,0.0003493594478,0.001198749085,0.0009429735873,0.0002424969781,0.0002444940024,0.0007718220467,0.001397435935,0.0002087789928,0.00007349965206,0.0002062690845,0.0007417972177,0.0002723131159,0.00009235520817,0.002323423056,0.00007157019632,0.0002354938163,0.001280907285,0.00002779335822,0.01694253346,0.0007459007355,0.0003564357104,0.00004304955284,0.00007421090097,0.005080030544,0.0002017933897,0.00005325806781,0.0004906766812,0.0002001088013,0.009519890934,0.01307284918,0.06817370649,0.02452173214,0.0005066734563,0.0004035526513,0.0001807123887,0.003553565421,0.00001992742776,0.00003738200609,0.00003468845981,0.00002634695484,0.007127418519,0.001264595172,0.00008755053323,0.0000651688099,0.000292482829,0.1520080384,0.0001259311291,0.0001722786884,0.0003919204581,0.0001312569135,0.000274114729,0.0004162955603,0.003668867455,0.00234519498,0.001065762663,0.00001972267091,0.00009709272888,0.0003864957124,0.0001461298091,0.0007720424252,0.00005890219304,0.6080229243,0.0000272945385,0.0003972571256,0.0001067410585,0.03801845294,0.0001577406781,0.0001256301476,0.007576679615,0.0001337023115,0.00003266956148,0.00003919311648,0.002413750347,0.00004760014543,0.003644899018,0.00001748377158,0.0001707678109,0.0001082661937,0.0002827709922,0.00001257673058,0.002033418535,0.00007626883919,0.00004526419483]
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
