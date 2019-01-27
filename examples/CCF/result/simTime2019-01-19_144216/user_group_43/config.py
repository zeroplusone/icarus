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
        experiment['cache_placement']['cache_allocation'] = [0.00005173029475,0.0001923305591,0.0002083360033,0.000192852587,0.001615758933,0.000727663427,0.0001676019611,0.00004171581195,0.001441947661,0.005214197949,0.00004050904772,0.0008020015302,0.0002870020654,0.0002162369202,0.0004516581623,0.0132099344,0.0001104924237,0.0006643935262,0.01731659433,0.00006511423237,0.000547829653,0.0004860746898,0.02857671648,0.0002074364996,0.00002534517426,0.0001126691841,0.0005419185372,0.00007296216834,0.06765272533,0.0001525694798,0.000162503301,0.009548271483,0.6079627668,0.00002697056148,0.00003849794046,0.0001419346889,0.03809161692,0.0009572880377,0.0001571555424,0.00009936814387,0.0001020262928,0.003126249587,0.0002296492786,0.1552759503,0.00005397216029,0.00009334565234,0.00008722229141,0.00007006347108,0.00002502122298,0.0002369386904,0.00008175967692,0.0002431924476,0.0009169652678,0.0009183551301,0.0001907653821,0.0001361609714,0.0001356773814,0.000100272673,0.0002935647002,0.00003030227328,0.000227299621,0.00002309364203,0.001120644034,0.00005772205017,0.00005073130541,0.0004551250014,0.00007411037443,0.0003534649612,0.0004611891873,0.002344290663,0.001380611886,0.00005055570349,0.00004798867916,0.00001912876651,0.001148857543,0.0001308341456,0.0002362202929,0.006292950135,0.00005226535522,0.002161854148,0.0003029222668,0.0001119136805,0.00007188407973,0.0001006661369,0.0004198189184,0.0002143977382,0.0005639211751,0.001010899557,0.003161796886,0.00003797757914,0.003678010227,0.0001804627038,0.0004451746174,0.0003948815139,0.0001441400478,0.00007612784143,0.0007159221907,0.00001885591571,0.008684966476,0.002048175644]
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
