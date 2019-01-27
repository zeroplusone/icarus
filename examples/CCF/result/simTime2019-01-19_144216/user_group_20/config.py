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
        experiment['cache_placement']['cache_allocation'] = [0.0001411090532,0.002111060116,0.0002127426396,0.0003682109379,0.0006798489873,0.00008778939904,0.01246499268,0.000015401165,0.0001092702925,0.03821723685,0.02444333155,0.00003410477054,0.001199087904,0.003264994761,0.0006788675207,0.0004644784638,0.0005371152539,0.0009318335071,0.0000515890978,0.0000194001481,0.00003918609228,0.0001806215435,0.0004177263067,0.0003489982121,0.0169702216,0.0006886686574,0.0007573594909,0.000210978668,0.0002727538829,0.0003599954566,0.00003889035209,0.0001333811473,0.0002585131538,0.0001256443214,0.009823724905,0.0002999721586,0.0002277712446,0.000134112103,0.002009857973,0.00006022875763,0.00001520005529,0.0001616073581,0.00003315797849,0.004477981682,0.00003349261657,0.00004367081902,0.0001680761999,0.0002597434578,0.0001988085236,0.0001687442862,0.0001196119557,0.00007699371831,0.0003152054699,0.0004197922743,0.000110355002,0.001557277701,0.0001065431782,0.6079630162,0.0003660735126,0.002388566359,0.1520821683,0.0005873270296,0.00003680154491,0.0001186133552,0.00006990239749,0.003844789289,0.001152648835,0.00005114258734,0.00008730692907,0.00007050112876,0.0000349582299,0.0008464315902,0.002338965168,0.00009773604684,0.0005546006654,0.00003932758872,0.001322904099,0.002801183557,0.00008051196173,0.0002789457752,0.005134719658,0.0001973687164,0.00009556690893,0.06762344688,0.001095198767,0.00009750522046,0.00006148222863,0.0009654268159,0.01365686138,0.003625713342,0.0001804722011,0.0002802669152,0.00006928706966,0.0001802304026,0.0005772999128,0.000627751673,0.0004497308986,0.00002322978377,0.00004345720374,0.0001432283925]
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
