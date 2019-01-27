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
        experiment['cache_placement']['cache_allocation'] = [0.00002361395202,0.0007988802056,0.004301907797,0.00004149532227,0.0004348071637,0.00002437637892,0.01023989259,0.01384302816,0.00006003578922,0.00004332872743,0.00003184359734,0.00009823744332,0.0001467909076,0.0004583520209,0.0002933200021,0.00005561981956,0.001150161462,0.0001403696712,0.001907425774,0.00611388802,0.00008077950467,0.000400126891,0.0002214997168,0.0000469189441,0.0002940547284,0.00006860517875,0.00004822114514,0.0000912081552,0.000846737449,0.00003512877424,0.0001072360542,0.0002229974958,0.0004052278039,0.01821401906,0.6080595503,0.0003616207614,0.001120190906,0.0006027135801,0.00008303887739,0.002145917274,0.00002361222388,0.00008358494713,0.000353092282,0.00006517155381,0.0000552672392,0.00007189524741,0.00001624193652,0.0003924948617,0.00008635554334,0.0008235619506,0.001728189838,0.00002814593926,0.0005785461841,0.1529123436,0.00006201889938,0.0001133453286,0.0001466077802,0.02461768004,0.001034641156,0.0002904786777,0.001265751275,0.00007129939676,0.00007807809262,0.002474230169,0.00002873136835,0.0003987882407,0.00005227301713,0.0001082824559,0.0001314627223,0.001750318782,0.0001276469525,0.000038576127,0.03866924368,0.00011065463,0.0003585619465,0.0004163031629,0.06787967323,0.0004426376389,0.0001542939429,0.003421242782,0.00106491454,0.003623963807,0.00001820608626,0.0000900171788,0.00009047559284,0.00007808329253,0.0001540034841,0.009531875848,0.000164745998,0.00193154855,0.0004113688687,0.00003012655311,0.0004601088001,0.0000541730201,0.00006575014024,0.005056965541,0.0002007309144,0.00119542816,0.0001931143614,0.0004599070225]
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
