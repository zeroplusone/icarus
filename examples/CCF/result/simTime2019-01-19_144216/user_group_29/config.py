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
        experiment['cache_placement']['cache_allocation'] = [0.00006989158267,0.001426351204,0.0001023359126,0.0005502805914,0.02435543383,0.00009557201289,0.00001908681961,0.00004108445676,0.0003672445369,0.0001070965576,0.00003850899338,0.0007003989507,0.0001608978462,0.0003623474516,0.0005267773513,0.00004924373958,0.00009325275277,0.00002227625027,0.000282616688,0.01306310914,0.0001833924362,0.00004571721729,0.0001238324451,0.0004231602304,0.0001025188329,0.0005405877603,0.00006103627018,0.00004572785812,0.00003414881989,0.06763925557,0.0009516680333,0.003125812416,0.0002827736638,0.0001208441703,0.001956995888,0.0002987516262,0.01050092969,0.0001544502132,0.00003866580189,0.001269672831,0.0001209681012,0.0004001295998,0.0001396649969,0.0001144155174,0.002944584117,0.00009496632056,0.03815042028,0.003449381178,0.0001330489157,0.0001259602393,0.0001172387733,0.00002002495782,0.0002299192823,0.000844373151,0.0001359818302,0.00004698515642,0.001263702681,0.0005927258444,0.007682656667,0.001774705562,0.003666502721,0.0001043444212,0.00008284894806,0.0001013333997,0.0005078219485,0.0004802412115,0.005123818793,0.0003967032483,0.0001049601718,0.009528034659,0.001895790783,0.001805510649,0.00008539042383,0.0004854250615,0.00003484179335,0.001259431671,0.0007654205793,0.00006098765333,0.0001591516427,0.0002718183119,0.0001191862784,0.00008287647321,0.00005492558886,0.00008956638616,0.001551048955,0.01960865317,0.6084194613,0.0001650488548,0.1521612412,0.0007145226019,0.00003697686926,0.0001136361109,0.00003805693693,0.0002300854568,0.0001384275613,0.0004227942439,0.0001565628301,0.0001003548216,0.0001155310018,0.0000450636973]
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
