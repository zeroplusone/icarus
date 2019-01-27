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
        experiment['cache_placement']['cache_allocation'] = [0.00002159762985,0.0001750925455,0.0003071303412,0.005039158394,0.00002837759374,0.0009690357732,0.004576239747,0.001054476752,0.0001045015168,0.00007036182387,0.0002812491573,0.000227864801,0.00003800422836,0.0005179024778,0.00003393600729,0.003657125495,0.00007239283512,0.00002505231462,0.0002139211595,0.00163224885,0.0003122794906,0.0004778992573,0.00001601140761,0.00004612055384,0.0001968058466,0.001080777856,0.00004315437317,0.0009646562333,0.6079575412,0.000136371884,0.001566831371,0.002130536707,0.00001552297171,0.000330619579,0.0009655646393,0.06800421902,0.0003096077999,0.002499087034,0.008723311495,0.0005628461294,0.00005056591343,0.0002417923999,0.0001306531686,0.0005639342059,0.0002045776869,0.0002327084917,0.00007621621956,0.006103351057,0.00005376873287,0.0005660239419,0.000121332229,0.0004714895045,0.0004086581752,0.002786266878,0.0004932554314,0.01254890569,0.00006136570731,0.1520873616,0.0001158073381,0.00107947314,0.0006185365975,0.0003359170352,0.001260625584,0.00006534454084,0.000026843654,0.0000931892589,0.0001441832913,0.0000974821328,0.00003629401786,0.00002670797944,0.0000918056256,0.00008008027444,0.0005131585784,0.00129687524,0.0001088501633,0.02436022363,0.00004251200726,0.0002008091431,0.00005880354245,0.009751845065,0.01712927728,0.004249473819,0.0001377996023,0.0001360941883,0.00004766863485,0.000466377515,0.000342414518,0.00007850298951,0.002182976451,0.00003132676787,0.0000536236152,0.00004997433774,0.0006203586197,0.0003837998037,0.001726983626,0.03861525055,0.00008357466713,0.0002632058417,0.0003576885865,0.00005059939063]
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
