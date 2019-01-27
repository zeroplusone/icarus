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
        experiment['cache_placement']['cache_allocation'] = [0.00002868525698,0.0002156277925,0.0005458461069,0.0001438416459,0.0001189573455,0.00485090601,0.01237351742,0.002257773668,0.01833729622,0.00001716005069,0.0001401652587,0.00006563299435,0.0004929877872,0.0004985885876,0.0001068375859,0.0002084919691,0.00004899829884,0.00008082488551,0.0003316806829,0.002124660851,0.000203019993,0.00002597637984,0.0003996159396,0.00003367472911,0.00008270591932,0.002409885483,0.0003548988094,0.0001701975065,0.000292517612,0.00003712863145,0.0006235216406,0.1068397235,0.00003662818916,0.000100947313,0.00005607388769,0.00001997847986,0.001989305582,0.00003474805642,0.0001142907116,0.0004189556454,0.00005049632894,0.0001194149725,0.00006839040435,0.0000540098707,0.00004061148358,0.00004723746221,0.007565546632,0.0001766899326,0.00004553921043,0.0001956362069,0.00005400005008,0.001527827496,0.006170689369,0.0001320188052,0.00004027972811,0.0005065130577,0.0005018469453,0.00498308118,0.0006579742512,0.0002330696368,0.00003887343872,0.0002151044564,0.005043200585,0.002799132504,0.0005619369519,0.00003596538526,0.00005755160882,0.00004653423509,0.00008451445976,0.0002290186446,0.00004128341637,0.0001453597924,0.0001665555346,0.0004736843379,0.003651923513,0.1521346863,0.00004461964594,0.0003391598548,0.0003440953524,0.0002203878859,0.00009955430262,0.0001098844313,0.02822430905,0.0001430239587,0.0002094207014,0.00001818154603,0.0000901810291,0.00002754824754,0.00009219107279,0.0009011001142,0.6080934265,0.00008390633931,0.00006733692745,0.0007502820778,0.0001165871798,0.0002326616797,0.0008927180766,0.0002842097169,0.01244747639,0.00003926526702]
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
