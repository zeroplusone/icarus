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
        experiment['cache_placement']['cache_allocation'] = [0.0006104450793,0.0001071503083,0.0009590773865,0.000234762716,0.0001392255554,0.0000561331311,0.0005670774568,0.0001430571047,0.1530042603,0.0003103966154,0.00004032326482,0.00006443196117,0.0001065470258,0.00002105183786,0.0001714621646,0.000120579946,0.0001619243134,0.000259231907,0.0003295915465,0.0001278409347,0.00003108932073,0.001209561178,0.00003140489732,0.0002205120781,0.00008284946219,0.00008626017365,0.00004321095113,0.005059643082,0.0009164386273,0.00002427563825,0.02435543712,0.008164232924,0.006332814358,0.0005616943552,0.00009398342527,0.001380117263,0.01457957769,0.607999089,0.0001839198881,0.0001284480877,0.0007808690068,0.00009553836864,0.00007164879936,0.00002643045355,0.00007120699183,0.00004935786073,0.00006261904059,0.00003274080013,0.0008753487601,0.0004626648496,0.0008090182471,0.0006075686014,0.00001735813016,0.00005038635014,0.0005314630917,0.0000290894745,0.0006706585392,0.00094304619,0.00002878041105,0.03860728617,0.0001308868634,0.003263250213,0.0001260619051,0.0001007027588,0.000009529673387,0.01206303242,0.0002423153222,0.0000289712488,0.003745269284,0.0003035474918,0.0001909523615,0.004263670719,0.00002254150434,0.0004815214494,0.001728902889,0.0001463572084,0.0002695558705,0.0007686044662,0.01724054307,0.00001935619306,0.00001837900919,0.0001614894059,0.0001072197872,0.0004799087409,0.0004589554077,0.0001355697649,0.0001384401816,0.00003947388197,0.00002911753876,0.001745781047,0.00008637496701,0.0001357296998,0.00004226625681,0.001502346006,0.0009911116735,0.00010812949,0.001568775292,0.0001058975284,0.07303380882,0.0001234423321]
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
