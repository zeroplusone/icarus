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
        experiment['cache_placement']['cache_allocation'] = [0.0001523463441,0.006436861259,0.0003492715213,0.00005746661015,0.00001853162841,0.0002693255327,0.00184672853,0.0005724977234,0.0005385568338,0.0004488285985,0.0000591379531,0.00002630219449,0.004546793144,0.0001721780535,0.004449042565,0.00005041018291,0.00004617960274,0.001703683639,0.0001463747609,0.0001577941945,0.0004002408448,0.0008968529239,0.0003889384326,0.00002933305218,0.00001521808446,0.00008971437458,0.000208583654,0.0002822780289,0.02492437523,0.0003292014299,0.0002036486374,0.0003585887566,0.0002034195049,0.0000354837995,0.00004485885142,0.0001587171392,0.00002762905791,0.001412416879,0.007587698273,0.0001652890914,0.00007302051283,0.6081863615,0.00005477564667,0.03879617761,0.003240948653,0.00003097331423,0.0000418723723,0.0001681973775,0.005073727915,0.0002901651432,0.00002442341172,0.0001490316793,0.009564180989,0.00002548488602,0.00009016225598,0.00004534712538,0.00009847734716,0.00007322055782,0.00003711178869,0.0001228419046,0.001280538684,0.001340205707,0.0001325486667,0.0005749853901,0.00002815108309,0.0000296165006,0.00001662409846,0.00001780470687,0.00004359125649,0.0001034537254,0.00006448729959,0.00003622250856,0.003093743414,0.0000418455721,0.0005008187851,0.0003858682723,0.000394476044,0.001854461678,0.004471666754,0.06768314641,0.000214260334,0.0001058619417,0.0000553121092,0.00008722538827,0.00004559428268,0.000791736543,0.0005120542361,0.00004424988276,0.0001154273387,0.00002646308521,0.002133120879,0.0004202270008,0.0001822267208,0.002215550326,0.01727317133,0.00004324877527,0.01370089771,0.00152113654,0.1523989706,0.00002170950857]
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
