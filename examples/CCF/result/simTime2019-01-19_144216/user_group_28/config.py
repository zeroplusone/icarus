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
        experiment['cache_placement']['cache_allocation'] = [0.0006097317409,0.00004676684321,0.0006970381899,0.003617250441,0.0001492843101,0.00004244127476,0.0007790492623,0.001818381995,0.03902560103,0.01248110325,0.0001409993017,0.00001792189296,0.0001335452111,0.006118806892,0.0008498671033,0.0001146144932,0.00002362370857,0.0001513061193,0.00002506403948,0.005389770894,0.00001369168287,0.0001112605818,0.0008960604242,0.0000485626359,0.000391382876,0.00002419129465,0.0004746075958,0.002736297297,0.001156735708,0.0005691143771,0.6083620404,0.0002353206549,0.0001048690027,0.007804387031,0.0004081552674,0.1768718437,0.00002830044926,0.00004350812298,0.001538349745,0.00002134414945,0.003378353258,0.0001846756459,0.0001340361375,0.000469287022,0.001714120413,0.0002349289614,0.0002196198954,0.0002827492264,0.00006854558136,0.00006463629426,0.000080699212,0.00001542373882,0.004250268428,0.00003037540409,0.0002815844184,0.002481068589,0.00002128982126,0.00003169257646,0.00007577748445,0.0002609729198,0.00008736310017,0.00004022302759,0.009530065967,0.00006831944218,0.002033487507,0.001838903139,0.000175603234,0.0007019626336,0.00008625830151,0.0002594072696,0.00003480588065,0.0001286077895,0.00005808665669,0.00297006864,0.001240134421,0.00003053878987,0.0000302822947,0.0169463204,0.0000291221155,0.0002881803316,0.00006012158993,0.001415097971,0.0001992510083,0.00009009542186,0.0000810580817,0.00003420414058,0.0002112381139,0.001044082072,0.00008295796917,0.001948722586,0.000134113183,0.000009584225188,0.0001209500994,0.0006861471451,0.000110240799,0.0001564345783,0.0003597764257,0.0005366453998,0.06757433346,0.0002149087532]
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
