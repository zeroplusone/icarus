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
        experiment['cache_placement']['cache_allocation'] = [0.0001831167733,0.00009006605066,0.00005199168401,0.001046071357,0.0002340287627,0.1520302618,0.0000235720388,0.002127325183,0.0003223167416,0.001733803605,0.002777968424,0.0001122665993,0.009647960703,0.0007739808886,0.000386870642,0.0001017076594,0.001976191024,0.000186694258,0.00002589974117,0.0000612112219,0.0001437383882,0.00030091715,0.0004050690142,0.0005603267109,0.0002538359644,0.00002229558288,0.001396915691,0.0001709754711,0.02559569815,0.0004109535151,0.000271205327,0.0003509660664,0.00002172209595,0.00005150781412,0.00008513406031,0.00006383051438,0.00003355377374,0.0006215943916,0.0005587264308,0.004691756522,0.00004398494356,0.0001692431806,0.00007172079222,0.003137971871,0.00012005287,0.00007583365871,0.00002864182427,0.00003723083719,0.00003757496886,0.004789045974,0.00008463802288,0.0005330051557,0.00001294747905,0.0004908866706,0.005148518557,0.00008916929456,0.6079655376,0.0004735695803,0.00093234656,0.0001347972711,0.0006163692814,0.00005108193776,0.000207688053,0.0000910452203,0.002236345738,0.001081976923,0.001097236082,0.01270612823,0.00007036639391,0.0001322648603,0.00007705969518,0.00002096492516,0.00003785161389,0.00004618106751,0.0001866497008,0.00283856971,0.00008768437486,0.00006917539648,0.0002679855212,0.0001491607029,0.00007530178326,0.03947194721,0.0002683039186,0.00004060324755,0.000511029961,0.0001795596889,0.00009790578918,0.000172469531,0.0002024985515,0.002167809565,0.0007212011708,0.06758399647,0.0001675102357,0.006826236567,0.0002174547391,0.00003522201685,0.0003327341873,0.01695067918,0.00007680739626,0.007548198503]
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
