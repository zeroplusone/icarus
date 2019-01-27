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
        experiment['cache_placement']['cache_allocation'] = [0.000521840635,0.0002249422114,0.0003495708187,0.002272679267,0.001347789902,0.0001721664619,0.00003371893677,0.0001040444233,0.0001663402601,0.000628742601,0.00004694661323,0.00002257299582,0.00008304619079,0.000107415766,0.0002080241959,0.0001966790762,0.002537080929,0.00005618015317,0.0001248154657,0.0685823876,0.0001535080364,0.004390245558,0.0002895638423,0.0001520998332,0.0001410396927,0.00003851042476,0.0001726122351,0.000596643581,0.0002173600514,0.005073483771,0.001145831981,0.001228525972,0.0000137176051,0.0002394906114,0.00006175878202,0.00009332450965,0.0001965179493,0.001931523542,0.00002490568916,0.0007722011911,0.006140953849,0.0005751203302,0.00007669482402,0.003713797053,0.0002905711416,0.00002469047326,0.0005327858369,0.0001988187398,0.00005433604316,0.6082148039,0.0004059193007,0.00002250200067,0.00006349568575,0.003779885055,0.001542665981,0.0000243760673,0.001095373944,0.0001344568719,0.00002638345268,0.002430653137,0.00006431211413,0.001406634143,0.0124217042,0.0009770024801,0.00003072915452,0.00001859809315,0.000123089873,0.0001513458461,0.00007064843498,0.0003896967421,0.0004378822679,0.01783966015,0.0001882004435,0.00008509464692,0.00005937865543,0.1521365038,0.00004617096804,0.001703150605,0.00009749231183,0.0008615411026,0.0005382136188,0.00002256791472,0.03813160913,0.0002001733056,0.0001742794173,0.00004911587407,0.0000958855533,0.00003203700191,0.02578259828,0.002899697256,0.0001133812193,0.00002435825317,0.0004272052785,0.00005655564648,0.009517704368,0.0007909554552,0.0000983949806,0.00007021088003,0.0001304972466,0.00766759027]
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
