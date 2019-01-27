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
        experiment['cache_placement']['cache_allocation'] = [0.0001685982332,0.0002193198208,0.002870217407,0.001977366681,0.00001261994924,0.00009053708454,0.0005413704617,0.00002058084932,0.0003839313301,0.0002204484805,0.00005298037172,0.0001125361791,0.0001871003013,0.0007719027431,0.00001802593262,0.0002913735821,0.02440521295,0.003258771608,0.0001497877206,0.000273160231,0.0006033334611,0.00008541846185,0.0003673635265,0.0002595575729,0.0009846223624,0.0001076224223,0.00001340473216,0.00005297267629,0.00006067722784,0.0000156311689,0.06773626327,0.002820133577,0.00004494244311,0.0008778028904,0.00003914294503,0.0004481658013,0.0004480309589,0.03807021633,0.00003492159612,0.000447840283,0.0005739533828,0.0006954803878,0.00001993934222,0.002438298755,0.0002446044832,0.001919745662,0.001881241454,0.001731417564,0.007149770115,0.0001009009535,0.007720361721,0.0002512422189,0.0002143382519,0.0003177835823,0.00009972588929,0.00001503539557,0.00006184451017,0.0004211912145,0.0001722263977,0.00006910934112,0.0001954089205,0.0002867060688,0.0001059102063,0.6082631072,0.0000798730899,0.006159536416,0.00005645130016,0.0000387976748,0.001187557601,0.00001692318307,0.00004347033643,0.0001961492046,0.0002513573336,0.0000550479008,0.0002528123978,0.00009569895617,0.00002649866955,0.0004443614827,0.0008559812561,0.004291735996,0.0003400699236,0.0006541069588,0.001550768009,0.0001616203112,0.00009714794141,0.0002490239992,0.001450939242,0.000036274443,0.00002589089702,0.1617229132,0.003648826012,0.0000573673039,0.0001804591589,0.0002716353362,0.00002943538142,0.0005045022072,0.0003996501762,0.00005248902742,0.01742893219,0.01259244689]
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
