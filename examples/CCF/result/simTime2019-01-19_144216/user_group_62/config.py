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
        experiment['cache_placement']['cache_allocation'] = [0.0002779332035,0.0001966084467,0.01447734588,0.00001891243975,0.001372804615,0.00001858345541,0.00003422317912,0.00621872584,0.0001241457932,0.00009890661834,0.041264147,0.00004081887046,0.003915144417,0.00006724381044,0.00003681974807,0.0008146792156,0.00007925050135,0.0008913541858,0.00009530325495,0.001772024038,0.00003924296954,0.06766450048,0.00005190887105,0.00005266795627,0.001320375133,0.0017131056,0.0003926058685,0.000113373443,0.0002817169021,0.0001457643449,0.00008766259057,0.00004738989273,0.0001699502794,0.0002406493992,0.0002767186552,0.00003101525293,0.0001769410696,0.00004626869704,0.0001674109681,0.00005671196709,0.0000208867696,0.0006843008286,0.0003154491227,0.007526353686,0.00001355539018,0.00003662369862,0.001431403068,0.0003811395897,0.0007861659167,0.00006070920401,0.00009059097409,0.002424997668,0.000980023134,0.0004496006773,0.00009063486336,0.0007080926453,0.00007528109649,0.001050386488,0.0007735381737,0.6094648496,0.00004435382081,0.00001023102632,0.00009346467113,0.0002982638406,0.0009576427349,0.00001010894512,0.0003079204012,0.0005233211542,0.0004639264505,0.0001261625732,0.00003572067358,0.00006956152806,0.0002730213414,0.0004290352147,0.00002246164129,0.003760789346,0.0002162818396,0.005176053695,0.0006178840692,0.03809549406,0.00009502266368,0.0005579861506,0.004247995863,0.0003164060448,0.00002960428771,0.000198023566,0.1520824618,0.00006663045734,0.0000956726722,0.0001700913066,0.002591181757,0.0003655977532,0.009560350867,0.0003046103622,0.00009885893653,0.00217783596,0.0001294769871,0.00007788857149,0.002991613781,0.00005545378933]
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
