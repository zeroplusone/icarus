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
        experiment['cache_placement']['cache_allocation'] = [0.000129281958,0.01211172681,0.00005194081521,0.00008687319177,0.00006413149629,0.0003129919366,0.009524162659,0.00002317769032,0.0001574915355,0.0003704580616,0.0004248529595,0.0001647243121,0.00007073702242,0.004427628727,0.001249815291,0.0002966544849,0.00008485914632,0.001155819434,0.001546168374,0.02472833131,0.01269423236,0.0003443632797,0.0005167659932,0.001279478178,0.1520738081,0.00006272658266,0.0001274045168,0.0005411432083,0.00001333662746,0.006094677595,0.0001732164476,0.00002244242429,0.00005678807325,0.0003552499762,0.0002503233261,0.00003788666049,0.003610367876,0.00005856025549,0.0009651240139,0.0007491463171,0.001007026628,0.0004929900828,0.00004737837782,0.002209453119,0.000447203243,0.0002550088844,0.00005722870105,0.0001135551881,0.001435283997,0.0002129176181,0.0001602051507,0.0006229972255,0.0004435827865,0.0001762211601,0.0003024140973,0.00003167821969,0.005080571876,0.0002381506396,0.0002468941637,0.00007609815389,0.0001661603252,0.003139863583,0.0002005811869,0.00009765399898,0.000117535711,0.00003394846851,0.000104866784,0.00004235887284,0.0005381443721,0.0002076061752,0.00004231304591,0.00001796364399,0.00001598307074,0.00004373684885,0.03803372571,0.0003606065785,0.00007881530975,0.00004087967076,0.0004414909056,0.6080310692,0.0001913681337,0.0006782881887,0.00144018397,0.00007197296879,0.001545367391,0.002403691049,0.000102650881,0.001634300605,0.0007093541656,0.06775464328,0.00003682349837,0.0001929240918,0.0007022329573,0.0008958470197,0.01691094944,0.001724158146,0.0001599568708,0.00008201887832,0.0002987413226,0.00004349525901]
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
