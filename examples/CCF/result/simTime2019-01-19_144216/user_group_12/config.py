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
        experiment['cache_placement']['cache_allocation'] = [0.00006113359934,0.00004441318019,0.00005085580545,0.0006955251534,0.0005101767189,0.000640157214,0.02433895532,0.00011086446,0.00002460858777,0.0002150143934,0.02935983506,0.0008597242033,0.00008398845086,0.001133769923,0.0001805634674,0.00009207690503,0.005254640942,0.0001314756042,0.0001008914673,0.00003918901298,0.0001753698801,0.001569969284,0.000176427846,0.0000843878388,0.00008546403202,0.008059207668,0.003117871559,0.0001032654921,0.00007990243102,0.00007171084782,0.00007446593799,0.03929854546,0.06765578889,0.00006075768049,0.0003506629544,0.0002156616254,0.00006303343323,0.001288648548,0.0001532553089,0.00005705208522,0.00004191757158,0.001183583298,0.1520219984,0.0000846165141,0.00002682478806,0.0006310687552,0.0006671575018,0.00004445651553,0.00258475942,0.00009826228106,0.001793131094,0.01158793423,0.0002107576308,0.0006779102167,0.0004055059822,0.00007718720433,0.000117128861,0.00004502887832,0.0002238147135,0.0004474018625,0.0003537460143,0.004303679424,0.0003083540418,0.003682836556,0.0000451115229,0.001050199372,0.000411514961,0.0002251161732,0.00113420198,0.0007917720174,0.00001100848186,0.0005032135772,0.0002573703574,0.00003622668381,0.002149280892,0.00004297357148,0.00004793088815,0.0004553907218,0.00006279622232,0.0002924838669,0.007632293228,0.0009964852741,0.000237137191,0.000370896845,0.0005681336049,0.0003370213035,0.00002626242597,0.000485394723,0.0002523855343,0.0002434738682,0.0001614537532,0.00004596551193,0.001124681583,0.0001030452708,0.00006330322097,0.0005734497343,0.002960458742,0.00001883240704,0.607972241,0.00002212354514]
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
