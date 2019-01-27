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
        experiment['cache_placement']['cache_allocation'] = [0.0001109272435,0.00004454928069,0.0002912617484,0.0005904531783,0.0008936476708,0.0001509724769,0.0007759118257,0.00004726162216,0.00216280642,0.06783372237,0.0001736632437,0.000189070755,0.000009504569513,0.0005270508799,0.00007133104077,0.0001721470989,0.00002799605613,0.00006417580495,0.00003178945025,0.000051980129,0.0004445466658,0.00005440868798,0.0007704827251,0.0002929273166,0.0006568502874,0.0001693000023,0.0002485779697,0.0009411242494,0.00002553840083,0.1528401241,0.00006919748904,0.0001396528134,0.0001805837408,0.00005910495514,0.01000206869,0.007746346621,0.0002791634107,0.0001651366865,0.00002749876855,0.00007504994417,0.00002662927462,0.00005752908608,0.6080675214,0.00003966691135,0.004279916794,0.00007669244364,0.002060925181,0.0001564410256,0.00362042695,0.001679471486,0.00004187495765,0.0000432477532,0.00001262852241,0.03863662896,0.001090413138,0.01377905349,0.0001524992875,0.0000237339794,0.0001693375762,0.0008321996679,0.0002618732797,0.001174535368,0.006313303,0.0001721390345,0.00009685156654,0.0000636555968,0.0006449922368,0.0001067336475,0.003456761966,0.0000324965101,0.00003111151921,0.0002152948836,0.0001511364302,0.00004731659787,0.001401071531,0.000392631913,0.0004228094044,0.0004983350921,0.0001427360542,0.0002781050924,0.00006957832459,0.003039906069,0.00003222888786,0.003835893738,0.00004933001052,0.0001050544709,0.0001514949569,0.001423328728,0.00001758680615,0.005390785123,0.0001141473993,0.0001821064662,0.00005700507708,0.01693179916,0.0000774820056,0.0003932339523,0.00006236507732,0.0001942321287,0.003056795516,0.02465701113]
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
