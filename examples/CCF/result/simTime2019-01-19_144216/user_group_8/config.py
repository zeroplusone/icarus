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
        experiment['cache_placement']['cache_allocation'] = [0.00006657423997,0.0002634469727,0.00006447215524,0.00001660255871,0.01035086783,0.6081620016,0.0000428378015,0.00002375442168,0.0001324850484,0.0007699328121,0.00005016719055,0.0003726494427,0.0003661044819,0.00827618132,0.007809485616,0.001459679089,0.00003546185213,0.06759493797,0.001280016307,0.00006221534113,0.0000346650454,0.002916247339,0.0001316943588,0.001387261616,0.0004977686334,0.00008385488347,0.0001146097251,0.005074899266,0.00005188893547,0.004669315074,0.0000470197528,0.0003644227204,0.00005022307713,0.1523828321,0.00003493318581,0.00008230838999,0.00015018956,0.0001298030841,0.001148707416,0.01245473663,0.0007706588512,0.0001105855226,0.0007763660933,0.00007337616103,0.0004605518411,0.0002537809849,0.00003915066381,0.0005608106555,0.003609975232,0.0001698025533,0.00007589122348,0.0006901260018,0.0001229299873,0.0001615679348,0.0000371372742,0.0002186691189,0.00007268599421,0.0003714562805,0.0005063196904,0.00005854474666,0.03811513165,0.001764240978,0.0001555344189,0.0006418180517,0.00006537478812,0.0001004339719,0.001002009124,0.00008049224559,0.0009860489063,0.0001616331072,0.0001317488278,0.0001974551119,0.00030885986,0.00004693997933,0.000308515732,0.002324359842,0.000210764195,0.0001531821569,0.02593906523,0.0001539225285,0.0002490834083,0.000907359364,0.0001406587873,0.0001199078891,0.00008224394392,0.00004151142254,0.00006219559978,0.01692963537,0.00062598624,0.0002215927306,0.00005565296896,0.004436509741,0.00004841223591,0.001590867268,0.002729851918,0.00008571647903,0.0001017880574,0.00007883397568,0.0003591039134,0.000137916265]
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
