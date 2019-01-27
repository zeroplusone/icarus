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
        experiment['cache_placement']['cache_allocation'] = [0.00002480143283,0.000214109004,0.00001778824961,0.0002202193754,0.0256533237,0.0001709474558,0.01712494013,0.0001052529756,0.0005129841901,0.0004025938415,0.000163430691,0.00005294181044,0.000586823858,0.00008768244249,0.00002976863033,0.00005142353655,0.0002160024593,0.00006208571194,0.1523080141,0.0003061486918,0.001163430409,0.002419326946,0.0004041470932,0.005061033944,0.00009169479538,0.0002293773509,0.00004917092186,0.003262226038,0.00001923147768,0.0002018641201,0.0009181074058,0.0002911195726,0.00001697131794,0.6080874184,0.00006213482824,0.0004706263537,0.0002619209859,0.00005358309466,0.00004734032795,0.0001456590236,0.0001682721798,0.00005312831808,0.038060434,0.00007827537913,0.00004195066541,0.0002299120233,0.0001110334315,0.001146336547,0.00006445012065,0.00008475860952,0.0001589893269,0.00004577294229,0.0002239241053,0.0006815681637,0.0001245779416,0.0001579321456,0.001497093143,0.003659334484,0.00003467783467,0.001459245372,0.00121606114,0.003224171622,0.0001639802178,0.0001519246984,0.0001033152362,0.00001956099505,0.00007364668077,0.0002127859174,0.001997141603,0.0002453418122,0.00002677223366,0.00005710197864,0.00114863738,0.0001405917875,0.00007107990659,0.00007818156729,0.00012342794,0.00005491593528,0.0001699327166,0.01269292905,0.0006703447761,0.0001474271876,0.006279967786,0.002925964938,0.0002475046571,0.01303988014,0.001291809203,0.009615361066,0.0003469404963,0.00005115665408,0.0001495713562,0.0001882688959,0.06757990917,0.0001468116102,0.0006035541026,0.00008610446494,0.0002459654539,0.002307408979,0.002440420882,0.00001479427102]
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
