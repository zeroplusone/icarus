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
        experiment['cache_placement']['cache_allocation'] = [0.0006679621038,0.001238802037,0.0001460407701,0.0005418297614,0.00003906968662,0.0002878653138,0.0001575551478,0.000340963901,0.0002453749988,0.0001546858973,0.0003060893576,0.000107933898,0.0005150453237,0.000230507627,0.0001154941688,0.00005878881026,0.0001654266061,0.0000659991974,0.00001718313349,0.00009801474196,0.0001885742755,0.0125840632,0.00005215757703,0.00005837986648,0.00005130829237,0.00006713551796,0.00017030177,0.00005415066092,0.0005927956676,0.00009319674395,0.00003038010528,0.003661499403,0.00005360432227,0.009645996794,0.00007791498282,0.0002428289532,0.00752580552,0.0001449549708,0.00002471175041,0.001891795705,0.001274107701,0.00004408707429,0.00002542154187,0.00009507795203,0.0008159374434,0.0008342935599,0.00005371123285,0.0006478222303,0.001603624216,0.000186172478,0.001344232238,0.00005583050234,0.001377080085,0.00005025605319,0.00007109979073,0.0006600871898,0.0004903288533,0.006368071651,0.002421567669,0.0002619396195,0.03803113669,0.001054371504,0.00008295058242,0.00006825890613,0.000100102232,0.00003209078228,0.00004746024911,0.00003266945274,0.0004101535768,0.001296984695,0.0002580320404,0.0001734355842,0.0001277062837,0.001753780044,0.0002708242275,0.00003504516431,0.0003775681337,0.0001358054958,0.0000558027335,0.001560140862,0.0001199184806,0.02482216821,0.0003915829639,0.007427060603,0.02173490713,0.005135151915,0.6079413634,0.00006535703598,0.00005019087431,0.1528982386,0.0004662466106,0.06758278299,0.0004412895174,0.001144668579,0.0002728030448,0.00008838934745,0.00001996172456,0.00005701868332,0.0001276597428,0.001915983704]
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
