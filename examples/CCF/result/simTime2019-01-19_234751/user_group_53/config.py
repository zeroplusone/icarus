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
        experiment['cache_placement']['cache_allocation'] = [0.0128572597,0,0.005273897711,0,0,0,0.00004168237657,0,0.0000003079183383,0.04659708043,0.000005995784861,0.006201133882,0.00000001452621456,0,0.003885061081,0.01858896577,0.0000363227257,0.008627750459,0.0000002128119728,0.0000157596517,0.0002545633203,0.02119298887,0.0005516916258,0,0,0,0.01533121914,0.0003040030765,0.002680880251,0.003385839061,0.00004430691748,0.0007592408205,0,0.0008791275995,0,0.0000007365186255,0,0.000000001675121931,0.0002438595522,0.00001263626715,0.01606805554,0,0.003807434927,0.009389268058,0.0311214757,0,0,0.0001459715546,0.03852898465,0,0.03316417681,0.04503306099,0.01306186364,0.0004393293124,0.002265079594,0,0.0002009208214,0.03933667706,0.02896118789,0.05023579847,0,0,0.03976156711,0.04875700373,0.008147853512,0.02404600361,0,0,0,0.04463561513,0.03688451308,0.04140553465,0.0496308008,0.000240159048,0.02051020643,0.006623489581,0.03490974516,0.02579883368,0.001468065011,0.000001975569059,0.01791890909,0.00193765705,0,0,0.0007239784231,0.0007786350534,0.000005098880774,0.04718737334,0.0002649927144,0.04302454641,0.00004869792148,0.0000115078612,0.001305671159,0.009741391528,0.02673877505,0.002685005315,0,0.00004724023456,0,0.00522732933]
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
