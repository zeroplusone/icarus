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
        experiment['cache_placement']['cache_allocation'] = [0.00001470617829,0.00006518361764,0.0001585935557,0.0001078831647,0.0001356749886,0.0002938238222,0.00002930738994,0.00009584419779,0.00008311914691,0.01746131636,0.00004003503014,0.00002796983428,0.00009255866315,0.002406857186,0.00005649960757,0.001814847726,0.0001775270059,0.00165080516,0.001570548122,0.6079665134,0.0001320878543,0.0008189667137,0.1522129718,0.03898213882,0.0000203354741,0.0001343528101,0.00002531993172,0.0005278509898,0.0003440893054,0.0007859109749,0.0003794190076,0.00002244949879,0.000306196445,0.0003485895343,0.0000835236792,0.00003518255773,0.000218886771,0.0005336725178,0.00003036380752,0.0001726825969,0.0001184674214,0.000160038253,0.000194492282,0.0005790966512,0.0000661056861,0.0008226162037,0.003344940895,0.00006378320784,0.00007736583312,0.002167835236,0.00006103787338,0.00003622684523,0.00001732230588,0.0005225553373,0.0005672695493,0.0002643628093,0.0001451565686,0.00001582457968,0.001814225633,0.00001897238268,0.00005067852573,0.00002699250476,0.0001866107737,0.00504268186,0.001499364681,0.0002349349188,0.0003116100158,0.0002027739806,0.0001462151735,0.000277946666,0.0001615056027,0.0000420543103,0.0001291277445,0.00009548781585,0.00006461620514,0.00002230179551,0.00008713046242,0.00009650832476,0.00003449204002,0.0002466416571,0.001648989427,0.00002739094811,0.00008061706205,0.00003973325701,0.0008578527575,0.06907522528,0.001211453218,0.0004538736482,0.01298026233,0.00008460873272,0.0405594116,0.0001005423281,0.0004035580334,0.0004276927986,0.00009001668614,0.002596000695,0.006123054233,0.003149707105,0.009578830351,0.0001292036653]
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
