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
        experiment['cache_placement']['cache_allocation'] = [0.0007356030133,0.00008353545489,0.0001718893481,0.001924642036,0.00002610008598,0.0002621240105,0.008845251446,0.0003616217494,0.002360025887,0.00008824774148,0.00006424514479,0.01245569928,0.00007947612975,0.00003996668386,0.0005226495284,0.00006297979806,0.003635586782,0.00018943768,0.0002952546112,0.0002605536846,0.00005542546059,0.6080036655,0.00004970857319,0.00007296604529,0.000309045549,0.00009734529422,0.00003887498954,0.000167584229,0.0001392428819,0.0001144396864,0.0001358271737,0.0004750192245,0.00005366501891,0.00003857068019,0.001578373626,0.001603979955,0.0000485276268,0.0004251832372,0.0002461487552,0.001010885649,0.00003504144194,0.00005532255382,0.0001238095615,0.0008469912858,0.0001651651797,0.00005972676293,0.06758356209,0.0005329398671,0.0244391331,0.0001400719716,0.005070453736,0.00001292194163,0.00003900988409,0.01702341806,0.0000306144439,0.04430553722,0.00003776781368,0.00005045675074,0.00003548716549,0.003173467744,0.0003617187062,0.001933718221,0.0005979805624,0.003302921611,0.00004199655059,0.0001258323645,0.0005178849256,0.0004001128476,0.00008350590826,0.0002054782298,0.00140575628,0.0007397924312,0.007617226753,0.00004286008619,0.0000654803845,0.0002598457792,0.00003368388898,0.1527008919,0.0001123371236,0.00005094659229,0.00003723895668,0.00066544964,0.00008236335904,0.0002588019932,0.0007782489393,0.0001830019755,0.0001330357696,0.0004397874741,0.000679661237,0.0002534729192,0.0000669148284,0.001352885938,0.0003438582948,0.00003900532732,0.00006095776127,0.00174520259,0.00002303125496,0.01057054194,0.0004633531921,0.0003329476395]
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
