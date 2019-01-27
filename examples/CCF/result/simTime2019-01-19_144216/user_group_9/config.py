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
        experiment['cache_placement']['cache_allocation'] = [0.0008655315751,0.00008539650395,0.0004450368624,0.00003514598499,0.00003498555149,0.00002063915426,0.001639269155,0.0001341712024,0.01076793883,0.0009123363417,0.0004335969506,0.00008868505844,0.00007443752276,0.00005140858706,0.0006727681456,0.00005568395089,0.0001697541019,0.00004652801493,0.00007720831398,0.003184093226,0.0000134413713,0.004041530971,0.0005816863846,0.00033979576,0.0003195114239,0.0003749700106,0.0004775519418,0.0001370078611,0.00003996540334,0.00006172089622,0.001733270614,0.00007456720067,0.0003779143184,0.0008944299375,0.0001057610916,0.002627217004,0.01693232787,0.00004172786152,0.0001278157987,0.0002206348652,0.002162511417,0.0009227194053,0.001042671879,0.0002128693804,0.00009127418045,0.006116975187,0.00004354803017,0.00006351353624,0.0007663476317,0.0007937533494,0.000203531014,0.00006532695312,0.0000507670806,0.00009012521836,0.001483951399,0.1719238085,0.00003819751418,0.0001549499099,0.0004416910505,0.0003551994672,0.00002262800429,0.001272532855,0.00001988867671,0.00004101325473,0.00003271681695,0.00007959696079,0.0002353187094,0.06797515261,0.0002547680241,0.0001611470531,0.00008619218412,0.0001546753561,0.03823913855,0.00007523831869,0.0004275727161,0.0007242124127,0.0001547730043,0.02624361062,0.00003220674384,0.0001802128381,0.00004049073484,0.000130836694,0.002844693439,0.00505507296,0.00004380534424,0.004724568231,0.00002712131013,0.0003048511435,0.001559057459,0.00006670176552,0.0004473925956,0.0002724018192,0.0009878485579,0.000347481532,0.0002204836698,0.001530513713,0.6080730119,0.00008145234064,0.0001101057311,0.000378317663]
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
