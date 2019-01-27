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
        experiment['cache_placement']['cache_allocation'] = [0.001685120793,0.00007580252927,0.000505961769,0.00002509501364,0.00005448001875,0.0001027692161,0.00004141986187,0.0001763164235,0.00007575413367,0.00006965719731,0.00001699038834,0.006267071704,0.003135342701,0.001705408722,0.03865259336,0.0000935102043,0.00006023636414,0.004218459137,0.00001678864801,0.152088477,0.0005376803862,0.0001929484187,0.0009450839225,0.02436792397,0.002126614703,0.00008886938378,0.0006554047409,0.06788613017,0.0002734556871,0.006253255038,0.0001327567543,0.00005341172916,0.00001966057421,0.6094010829,0.0003432451947,0.00004798401694,0.0003584782763,0.0000709273149,0.00006008787993,0.000472532563,0.00009810043689,0.0002239734674,0.000137195111,0.001889537699,0.00005533157353,0.0005588715214,0.00004715697299,0.0002419033901,0.0001897136575,0.002070681238,0.0001067979973,0.0000723528712,0.0004674352916,0.000207445882,0.00001388000759,0.0003210501947,0.0003225860058,0.00004946862329,0.00004757370104,0.000084141166,0.002439493509,0.001601825683,0.0001520472399,0.00002524689363,0.0003242308799,0.01006495144,0.0001874160037,0.0007779890765,0.000126411867,0.0004250314427,0.0001342353438,0.002762678349,0.001511631326,0.00158732387,0.01691364873,0.0001937780555,0.0003484866093,0.0001157819323,0.0005433916744,0.0002937157406,0.00007500411929,0.00752255046,0.01264408682,0.0000298385258,0.0000559677656,0.0001261858741,0.0007978255941,0.0001557180001,0.0008664765341,0.001037796962,0.00004060821946,0.004304023146,0.0005324287799,0.00004566302759,0.0001319728144,0.00008077578454,0.00004924594457,0.0002396848903,0.000035162604,0.0001396828121]
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
