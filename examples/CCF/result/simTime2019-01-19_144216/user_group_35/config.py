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
        experiment['cache_placement']['cache_allocation'] = [0.001323597104,0.0004495457876,0.00002642935697,0.0003708792981,0.00005476919641,0.0001564335555,0.00003100554292,0.003710952349,0.0001812084639,0.009105409761,0.0008823447293,0.0008466510779,0.002288382027,0.003629663409,0.0000225091527,0.0014741679,0.0000798253364,0.0001713398505,0.00004190115667,0.000750618234,0.004266463142,0.0002377156815,0.00004026787774,0.000122806477,0.0004320162091,0.00002628655365,0.00007211838876,0.005070409356,0.009632789265,0.00003023702867,0.0002793140362,0.0008054011906,0.00009467385581,0.00004855684136,0.00005830667698,0.0001082145605,0.00006649095303,0.0006260699744,0.0390869761,0.02439391586,0.008499610528,0.0003495923565,0.1522083437,0.000115766165,0.0001664896728,0.0003069017138,0.0124593971,0.0003329201107,0.00147397324,0.0005585323642,0.00005208102683,0.0001327460527,0.002177055634,0.000116981993,0.00115169068,0.0003675982853,0.00009400639182,0.0001627689544,0.000158608697,0.00001793884713,0.0000884787581,0.00003185978632,0.0004230686142,0.003366252602,0.0001696233551,0.00006226390097,0.0002535999246,0.00005894957018,0.0003261125812,0.01706598147,0.00005444742252,0.0005154096624,0.000400336614,0.0007867311859,0.00006609567107,0.001916663111,0.000309547706,0.00008372374448,0.6080088225,0.00005989545438,0.00003091579614,0.00003083716374,0.00001985391607,0.002457165919,0.0001706600943,0.00004720703589,0.06762324634,0.00006194766589,0.0001655622822,0.001035079865,0.0003963220772,0.0001735832711,0.00003545585963,0.0009216080728,0.0001619714807,0.0001738290367,0.00002487639458,0.00005579048472,0.0002660800193,0.0001004767587]
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
