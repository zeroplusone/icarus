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
        experiment['cache_placement']['cache_allocation'] = [0.0004130740753,0.0001569498448,0.0001066732763,0.00007362524733,0.0001189335006,0.0001515185255,0.00003816252232,0.04059563201,0.00006850892952,0.001026955559,0.001039670636,0.0003588874043,0.00002205220029,0.0004427855243,0.0000385285894,0.0001461682775,0.0001140138027,0.00003083434933,0.00008979230818,0.007620658209,0.0002675009268,0.0004430054528,0.0002779416466,0.0001831828957,0.0001201344582,0.0007686276398,0.00025183603,0.005535808985,0.003718804156,0.00003170199264,0.006542888122,0.0005974724239,0.0001714726468,0.0001390337002,0.003791661583,0.02517189948,0.00001803036434,0.00001240385626,0.001896797456,0.00007283689487,0.000198708193,0.00005880496429,0.0000550448496,0.00001703893041,0.00001590388248,0.002129640966,0.00002576278115,0.00109751574,0.0002558026555,0.00001696955462,0.00006552685888,0.0001749960685,0.0003974905786,0.0001347019951,0.000717235757,0.00006082399707,0.00005487408678,0.0002090138359,0.00006473370905,0.001759582871,0.01253469551,0.01961099089,0.001939037271,0.0008219328117,0.00004906792975,0.0008727380661,0.0000568890466,0.00003123571566,0.0002022150876,0.00003744069448,0.0002585113245,0.001746680015,0.001297003221,0.15204389,0.001390678263,0.00182619794,0.0003539441187,0.00003149350128,0.00005952507341,0.00001742659846,0.0004583738471,0.607982689,0.0009356910847,0.00004800684364,0.004356062517,0.0004171758921,0.009538311165,0.06790833798,0.0002226190644,0.0001093535302,0.00005791989745,0.0006950292224,0.00006537674452,0.0006553533466,0.00001508518786,0.00006274420605,0.0003859302188,0.0003351147595,0.0003457706697,0.00004682392476]
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
