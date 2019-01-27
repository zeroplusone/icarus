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
        experiment['cache_placement']['cache_allocation'] = [0.0001819447472,0.0001544419183,0.0001913532004,0.006228794705,0.0003284820892,0.0006818254202,0.0002307218372,0.000127594005,0.00201098759,0.01462446311,0.00003618733335,0.0001732154302,0.00005447889532,0.000105445715,0.0001104494469,0.0002718154419,0.00006886664624,0.6082013378,0.0002770497352,0.0001212227723,0.02565049921,0.00005484961011,0.00001999931898,0.0006290880792,0.0001698779448,0.005068623807,0.002012392098,0.001276342845,0.002726089122,0.0005325973551,0.0002896040653,0.03802310721,0.0001553434741,0.01695732216,0.0001113614252,0.0002222788025,0.0001405934465,0.0002742354178,0.00008341986591,0.00002606050193,0.001214460728,0.00005898623757,0.00003412221241,0.0008240045431,0.007597145809,0.00002673545318,0.00006342076552,0.00002361105669,0.00002981409599,0.06804276101,0.0003404604464,0.004246660234,0.00006225795063,0.000934987844,0.00004530015794,0.0004307196025,0.0000170708394,0.0004368647562,0.0001649144351,0.00005604054652,0.0002925098207,0.0001613849993,0.009527290748,0.0001946241002,0.0007454080969,0.00004855257501,0.0000833328426,0.00003453175803,0.0002315995267,0.00008774273361,0.0001531561322,0.00003988301871,0.0001591315531,0.0002058222014,0.00008959587455,0.00001859112879,0.0001949395653,0.0009852077265,0.00002984836282,0.0004094234836,0.0018819986,0.001017914026,0.001938404427,0.1530856142,0.00004364435925,0.0004407379021,0.0006242032099,0.0001645395373,0.0001342283067,0.0003163742813,0.005370566655,0.002417414472,0.0004245912148,0.00005336669561,0.00007926323248,0.00003927130275,0.003221097222,0.0001697119428,0.001558758454,0.00007102135215]
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
