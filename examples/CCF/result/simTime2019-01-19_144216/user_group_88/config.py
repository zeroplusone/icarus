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
        experiment['cache_placement']['cache_allocation'] = [0.002781984447,0.00009381356162,0.00007736646926,0.000140573917,0.00001686351453,0.01289786953,0.0001311840219,0.00004587300049,0.001184131865,0.000124241413,0.0007374085869,0.0001519861724,0.0001533846452,0.0002972608721,0.0002171487719,0.001677459732,0.0004315833889,0.0002056556172,0.00007789613922,0.0005115462738,0.00005713230732,0.004609915649,0.00005614371175,0.000477354498,0.1520425147,0.0006592928627,0.000237401818,0.0001922571947,0.000276985445,0.00005573136119,0.00009374534848,0.0033364233,0.0009519241665,0.00004965228043,0.02474746739,0.0001415350911,0.00003236401246,0.001009469056,0.00001833290279,0.00007495618461,0.000009448830446,0.000195419412,0.00003278701398,0.01695551388,0.000078346828,0.00005920595048,0.00004908731933,0.001243468952,0.03892181522,0.002756557895,0.0002969523489,0.0003964217689,0.0004360907515,0.00006399234111,0.0002671157313,0.005103310707,0.0001642715249,0.00005169853567,0.00004736340281,0.007579376045,0.00006996704057,0.00008200672165,0.00008811100985,0.0002531623228,0.0003042670721,0.00001241587009,0.000175206705,0.0008733021653,0.0003855289032,0.0008508298725,0.0006509658458,0.6140356487,0.001016467278,0.002470115014,0.00003169762407,0.0002099449413,0.00005358317063,0.0003809710926,0.0004236280772,0.0001916599928,0.0003399582409,0.0004749122316,0.00007568011402,0.00003810652146,0.00007399050474,0.0001919614369,0.00004570944502,0.0006846619677,0.00002632349424,0.0676741249,0.001439691714,0.01034726207,0.001475072098,0.007876505483,0.00001730341473,0.0003878739125,0.00002434447394,0.0003732864965,0.0000544678697,0.00003520845285]
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
