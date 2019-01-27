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
        experiment['cache_placement']['cache_allocation'] = [0.0004307401577,0.0003811559563,0.00112452279,0.0001285323095,0.00004525976093,0.00006232875842,0.00001365715198,0.1551337209,0.02548659633,0.00003945117785,0.0004135033819,0.00004866954456,0.00006042018512,0.0003226921495,0.00423834614,0.001637958321,0.006718762151,0.0003379657961,0.0003676778049,0.00002630043787,0.00002386454454,0.0002020750266,0.005118229232,0.0008322134987,0.000520834504,0.0001828953797,0.00004896176255,0.00002579658857,0.00008514593435,0.01711034063,0.001416201238,0.0004616546928,0.00003122286987,0.00004520806263,0.0001904654429,0.00003026651179,0.0005054383982,0.000103053816,0.0002953043774,0.00755198369,0.00004030588517,0.002157251687,0.000294724672,0.608339729,0.00006394189519,0.00006142303984,0.0001823491274,0.00003098596368,0.01243007582,0.0001361823561,0.002738351418,0.00003512975838,0.00004312831021,0.0001264429491,0.00002926235116,0.0000358718463,0.00002580271686,0.0005374031229,0.001060390538,0.000341598602,0.0001310564888,0.0002611658996,0.001361888593,0.000996199104,0.0008229699318,0.0004137885332,0.06759005247,0.00006351545896,0.00006894472775,0.003830910323,0.0003637990627,0.002570915836,0.00009230060818,0.001716005141,0.0007735963733,0.00002213397112,0.03809269045,0.00003642693528,0.009777353489,0.0002351534425,0.0002942833051,0.001261212544,0.001036090255,0.0001994869943,0.0004184712992,0.00008536513053,0.0001354772426,0.0002733655842,0.00007560661473,0.00004636392931,0.0001581679776,0.001864731257,0.00003111639748,0.00002331634499,0.0001237513705,0.0001296635867,0.0007736025555,0.0005293698099,0.002655684424,0.0001542380646]
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
