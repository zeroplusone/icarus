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
        experiment['cache_placement']['cache_allocation'] = [0.0004053068171,0.0408282338,0.0006477921885,0.00019895647,0.00006924776048,0.000114874721,0.00007905799712,0.002393226645,0.00004086421567,0.0002677553681,0.0007557738448,0.00004007035106,0.00007787624576,0.00001141046479,0.0001329233649,0.00003226674872,0.0001930545519,0.00005231240794,0.0005327724585,0.0002702377107,0.0001553293665,0.0004843281405,0.00004488449558,0.01695521897,0.00001652206162,0.00005405397944,0.0000832051142,0.0003967320309,0.00138193788,0.0002367783085,0.0001002746068,0.0002646130539,0.003713569341,0.00002997444983,0.00516815832,0.0001030437438,0.0005164107396,0.0003571275234,0.001937300248,0.0001815616486,0.008289277536,0.000592044954,0.00004622703822,0.00006170214835,0.0001678447689,0.00004212527867,0.00006194541244,0.001241178316,0.000433928006,0.00609833422,0.0002177733683,0.000155447312,0.009534145033,0.00001640143404,0.001462998371,0.00009034644966,0.00004157459197,0.000120480587,0.00005775747424,0.0001006487099,0.00292347038,0.0004450874842,0.001234743806,0.00001465393806,0.0004811781215,0.006331406093,0.0000723774084,0.06926908334,0.0008825007523,0.00005751803901,0.0001947542018,0.1520071245,0.00008912079325,0.00008679470888,0.00006041155134,0.004300758694,0.0003659693482,0.00006642153101,0.0003126428714,0.00003016129742,0.0006349759543,0.00003166312534,0.01249261555,0.0001680078465,0.0006447483421,0.02459769449,0.00006927326176,0.000669209602,0.6079766775,0.0001862085235,0.0004574840917,0.0008328704927,0.0001685162467,0.001538203236,0.001243684377,0.0000417461352,0.0006292129948,0.00001604191077,0.0001044633737,0.0001133049522]
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
