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
        experiment['cache_placement']['cache_allocation'] = [0.00002868526586,0.0000513151931,0.00002242772623,0.00001470656853,0.00001665025223,0.00009282076355,0.02444624006,0.0001412520025,0.0001879826246,0.0001253185237,0.005020978682,0.0004081896565,0.002304133028,0.0004765025395,0.0007473911979,0.00009181864184,0.00001167766079,0.0001168186615,0.00001115454109,0.0001940825028,0.0001112556275,0.1520591035,0.0002414172316,0.0001227173721,0.0001444086469,0.001004039352,0.0002472053663,0.00009988054782,0.0005450096394,0.0006177359683,0.005402650969,0.0003858624298,0.0009551045052,0.00008031456323,0.00101174367,0.00007821337604,0.000926599179,0.0000175066814,0.03810225872,0.0006465234428,0.00002094255264,0.00008551529224,0.0003364084539,0.00008142568171,0.001832193636,0.00003412911822,0.00449009043,0.0004931160441,0.002006825166,0.00009995653923,0.0008424627499,0.002718409118,0.007515977985,0.0001153249688,0.003137437316,0.00003531098319,0.0006236843095,0.00007404650297,0.002162616767,0.00007654510376,0.0004961360853,0.0001307516036,0.0001916051339,0.0001934020167,0.00008648652837,0.002181078733,0.00005980854313,0.06764226976,0.0002771422216,0.0003953501916,0.006258149818,0.6079944802,0.0001174593534,0.00003557814311,0.009509673599,0.0001761185643,0.002956316719,0.0009054585248,0.00004952599446,0.0008819464275,0.00004247523789,0.0001253860625,0.00003281370972,0.00004596802508,0.01714139535,0.0007246914415,0.0001647860194,0.0004139559432,0.0001388531788,0.0000672206549,0.0001025836129,0.0002252096457,0.0001311331607,0.00002830032264,0.0002340497061,0.00004836689824,0.00003890815544,0.0001085249673,0.003121306356,0.01243321779]
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
