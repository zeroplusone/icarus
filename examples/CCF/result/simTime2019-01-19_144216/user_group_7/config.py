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
        experiment['cache_placement']['cache_allocation'] = [0.002437413167,0.00008235580031,0.0001260785864,0.0001516131212,0.001796144671,0.0001156015015,0.00008819826593,0.02628406313,0.0002586762005,0.00001837814834,0.159545293,0.001742368835,0.0001876511041,0.0003297654977,0.001871203528,0.0001034788948,0.00006162803219,0.003664731619,0.001594963679,0.0008857453085,0.0001662936042,0.0001363100413,0.002719468079,0.00004363924827,0.000196173601,0.00004504403837,0.0002382509114,0.0001355037832,0.0002720296828,0.00002527234609,0.0001106754034,0.0005186473214,0.00004647952016,0.001330616362,0.00001857299736,0.0006654942784,0.01250903958,0.0002321367866,0.0001823096114,0.001628728029,0.0002237993889,0.0001111192245,0.00009808558737,0.0002116298627,0.00005357001988,0.0001829387401,0.00001095092386,0.0001048621411,0.005186729275,0.00003738749207,0.00003654730115,0.009783315142,0.001527983709,0.0009186080723,0.0002034297901,0.00002929961357,0.0004513661514,0.0002062768271,0.000103440783,0.0005239732908,0.00008481188141,0.06827710266,0.0001485932836,0.0004154857727,0.0001439731388,0.006114697739,0.00008321365921,0.0001563804901,0.001339197202,0.00001597652955,0.0001595379563,0.0003568384976,0.00008577203181,0.00006710968118,0.0005175643807,0.01708552956,0.0000930160489,0.0003635315098,0.001161745051,0.00438035077,0.00006051718689,0.03944323254,0.0002808554732,0.00004937122476,0.0001387669425,0.00002544261066,0.0001239930961,0.0002399755836,0.00004583187483,0.6079673706,0.0005573571565,0.00009441450348,0.0004096777493,0.0002792203662,0.0001875389716,0.0001107476484,0.002202444957,0.0007573262608,0.00008574634527,0.00331839041]
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
