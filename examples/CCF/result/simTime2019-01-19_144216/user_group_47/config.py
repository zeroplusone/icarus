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
        experiment['cache_placement']['cache_allocation'] = [0.00007659673246,0.00003554744058,0.01099637475,0.0001348473897,0.0001195692857,0.0003508484446,0.001425986006,0.0001122720803,0.00008875301341,0.00009892117607,0.6081812449,0.02456923733,0.0002344908214,0.00005245119892,0.006152560862,0.00005245817398,0.00006162944596,0.0001003602791,0.0002095411706,0.00004803814978,0.00002066087535,0.000393081434,0.0002378929337,0.00008780880792,0.0000364773677,0.00006517066339,0.0002853049213,0.0001411809057,0.0004894334222,0.0002239870851,0.0001880142298,0.000157070179,0.00007284696684,0.00008250533031,0.0004163299786,0.03806748096,0.0004748511861,0.0012129555,0.0001878956057,0.00002181338058,0.0001792050563,0.0007996014518,0.006730835182,0.001642183415,0.0008568368664,0.0002912637627,0.0001529853243,0.01729216411,0.00008838364543,0.0002591770798,0.00005852438894,0.00027041838,0.002820640136,0.0003829741006,0.1534860808,0.00007147126189,0.0007686232759,0.0000257388573,0.0001357463868,0.0002233774017,0.00002057182045,0.00003271809374,0.00003428560304,0.06766413816,0.0009281653749,0.00002210618238,0.0002419319892,0.0002211017839,0.00001849808644,0.000101464569,0.000174581571,0.001161963427,0.0003927103524,0.0005901335278,0.00108506839,0.00001609046092,0.005057427495,0.00001888952446,0.00006668394894,0.003122809781,0.000873115235,0.000929663386,0.00005258951586,0.004407040877,0.0006459018621,0.0003489781025,0.00006093717345,0.00006886321465,0.00009627686588,0.00003591866409,0.02193939575,0.002038637569,0.000140682416,0.001682713642,0.0000887533985,0.0001115533374,0.0002014224046,0.0006037205484,0.002120878155,0.0000808964995]
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
