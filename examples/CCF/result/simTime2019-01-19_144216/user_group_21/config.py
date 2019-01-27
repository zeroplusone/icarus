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
        experiment['cache_placement']['cache_allocation'] = [0.003154185296,0.0003258466075,0.0001010178977,0.00008900590406,0.01249171912,0.00002216135504,0.06772224364,0.6080750898,0.001989905027,0.0006936851745,0.0004061272462,0.001968649406,0.0002205624761,0.001391561953,0.000204810988,0.002942915409,0.0001053010581,0.0001009193932,0.0005916824445,0.009626829841,0.0001580343597,0.0004539330756,0.00002292416436,0.0003012715157,0.0008219446242,0.00002558500923,0.00006355860837,0.00001957993164,0.007524712132,0.00004730361246,0.00002683909697,0.002412339296,0.0003000713201,0.0000705697844,0.0001175448606,0.0005797903377,0.00005469805748,0.0006457903462,0.0001750438561,0.001153253268,0.0002138121621,0.00003329542891,0.0003785144263,0.00009599142635,0.00002894159978,0.00007943412988,0.0002320364716,0.1520315325,0.000173988907,0.0001904735072,0.00006666613174,0.00007030955356,0.00001637257273,0.00145457876,0.001849329846,0.00007801728398,0.001556156756,0.0006138692645,0.0003460345929,0.0001957445069,0.0005926683934,0.0001084843515,0.000224270111,0.001291013226,0.00008218436943,0.0001526356338,0.006104860581,0.002142155788,0.00004083546681,0.00003358734538,0.00004851898597,0.0001046510128,0.0006504250765,0.00006981368699,0.001368805026,0.0001105819847,0.03805597618,0.0003340997763,0.000471482726,0.02137723046,0.0002467233526,0.0001121371488,0.0001008168856,0.0001747683377,0.0003153444652,0.0005424141968,0.0002187797826,0.003798281091,0.0001164633406,0.0000253382612,0.001261807329,0.0008567314716,0.00007531922308,0.0001484090745,0.02438017684,0.00009102405264,0.005044067932,0.002122984419,0.00003757183891,0.0000624536605]
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
