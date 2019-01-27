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
        experiment['cache_placement']['cache_allocation'] = [0.007534059672,0.00005962623642,0.00002827272656,0.0002215864423,0.1520537943,0.005074210579,0.0005374145495,0.004536515022,0.00008932437032,0.00007698869438,0.0008226037312,0.0000953338145,0.03831422924,0.00003625151429,0.005965020021,0.0000369038628,0.0002667520136,0.0001266259271,0.0008989239087,0.0001218810243,0.001730656198,0.0006912686795,0.00008502078921,0.07077385822,0.0002735948616,0.00009332238817,0.0003275457453,0.02467306689,0.00008834211514,0.0000597508282,0.0005192083336,0.0003309473604,0.0000324022006,0.00003524381683,0.0001040194169,0.00004371793203,0.0002148638318,0.0001316819778,0.000261666844,0.00005276837237,0.00135616055,0.0002100470196,0.0004473559045,0.001953592154,0.0002872318756,0.0004762636531,0.0002750706196,0.00106968045,0.009534756645,0.00003976093965,0.00004024096111,0.0002945758319,0.00007148673733,0.001212735834,0.0002840477605,0.0003191887445,0.00117634237,0.0004350979688,0.0001446742751,0.6079927808,0.00007304476162,0.001302561304,0.0003342178753,0.0003864320842,0.00002587125583,0.000125533675,0.0001502192738,0.00003490407805,0.02301023372,0.0001304699878,0.0000459696967,0.01290436913,0.00002528354667,0.004050999744,0.00009545160434,0.00001565095003,0.0006494059405,0.00005437358343,0.0009546376387,0.0004945298973,0.00003917666734,0.0007392044825,0.0001227227769,0.0000677150882,0.0001629966384,0.0001512386396,0.0001376880148,0.00007774250349,0.002785094977,0.0001745623548,0.0003478070753,0.001902849203,0.00008979155859,0.00005642263597,0.000074823896,0.0001245860213,0.00004463812519,0.00006381742011,0.002768822806,0.0001637837927]
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
