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
        experiment['cache_placement']['cache_allocation'] = [0.00002597312833,0.0152817698,0.0006877356614,0.000323097642,0.06775307461,0.03801250262,0.00007451010077,0.000199282862,0.004355857286,0.0002028668802,0.00003331031687,0.0001894930212,0.0006598060972,0.00007704649255,0.0001067830318,0.00003656691986,0.0001720970405,0.6082892581,0.0000411517758,0.0003446667725,0.00614594876,0.0001199581374,0.00006013261541,0.0001748428707,0.001239371957,0.0000581208202,0.00007832357436,0.00009320245369,0.1537935116,0.0001465518748,0.000247301692,0.001504430505,0.003719963784,0.0002419445004,0.00003609315956,0.0006823656595,0.0000199368364,0.0007957860326,0.00003241318718,0.0001866122467,0.0001084942966,0.006015407342,0.00006673564834,0.008286538923,0.0001477796414,0.00003586777743,0.0006811799927,0.00008970647345,0.0009378037463,0.00002737007967,0.00004660369325,0.0007464011521,0.0007770178918,0.0008255769447,0.0000398721018,0.00001908006692,0.0243663647,0.0002260557006,0.001903211011,0.000239378585,0.0005476343619,0.0003311217834,0.00009110894564,0.0002394921552,0.00003718956742,0.001027336011,0.00005337392691,0.0009493742992,0.00009152162369,0.00003171625042,0.0003953069643,0.0001983849085,0.00003105241914,0.0000962968691,0.00144630827,0.01692765563,0.0001684720911,0.002828183331,0.0007149423122,0.001976606997,0.000305202233,0.002138597682,0.0001996580449,0.0002379583706,0.0001725193978,0.0001765466814,0.0002535275258,0.0006213402556,0.0002481285146,0.009560806851,0.0001034531225,0.0001248702557,0.00004960659477,0.003696683732,0.0001588210293,0.001179518549,0.0004165755366,0.0001280901933,0.0001197515739,0.0000951568801]
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
