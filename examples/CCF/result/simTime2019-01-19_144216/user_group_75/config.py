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
        experiment['cache_placement']['cache_allocation'] = [0.0005598007781,0.000178317889,0.001147152859,0.0000455403143,0.001042180299,0.0006550175897,0.00002864548571,0.0001647423335,0.00007088210898,0.00006394450606,0.00008048134928,0.00009261103679,0.007645376631,0.0002627592344,0.152054249,0.01104460181,0.00007918448407,0.0004841806648,0.00003467184588,0.00007205858085,0.00008637701974,0.001786215342,0.00006651840383,0.002225221899,0.000166005623,0.001142550328,0.0003188196563,0.001320475548,0.0001233334959,0.001419070409,0.001234346911,0.0001408754169,0.0000471536501,0.00004074619205,0.0003020506659,0.000217228687,0.0003625643723,0.00008378127134,0.002315394629,0.00004515108318,0.005091739163,0.0001430664413,0.00004699162654,0.0001283065167,0.00007283677495,0.0003595549146,0.0002099954054,0.00003067955795,0.00008013888164,0.0009930508575,0.0001310868325,0.0002194911274,0.002494615518,0.0002880207747,0.00004681623919,0.0006697957336,0.0001385717524,0.0006000179985,0.0002488409309,0.0001508519609,0.000190543008,0.0005453703175,0.00004408515359,0.009693477183,0.00003197606686,0.0001103222632,0.6079585348,0.00004302043699,0.000030215669,0.004243106944,0.0006504599505,0.0002345694801,0.0001910647128,0.00004999423439,0.0009193446193,0.00281156411,0.001368269033,0.00008083426105,0.05802220092,0.000165786709,0.0001419013631,0.00005514695244,0.0001396068222,0.0007323589147,0.06774923455,0.00008821578908,0.00006277047215,0.00008611908625,0.0008268328309,0.0004952531639,0.0001073514674,0.00006897963189,0.0006333217138,0.00006679218495,0.001906568306,0.00003456813847,0.00006100173888,0.01243901532,0.00003550525303,0.02548996797]
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
