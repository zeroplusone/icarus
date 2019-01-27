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
        experiment['cache_placement']['cache_allocation'] = [0.00004740872641,0.001934687323,0.0001730573664,0.006179420984,0.00146473429,0.03806020198,0.0000232112745,0.00006719534609,0.00009932901644,0.0008204508484,0.0001990221749,0.0004230521875,0.06779819195,0.0001887834199,0.00009345324188,0.01750961117,0.00004976645457,0.0007312177815,0.003861465594,0.0007619483563,0.0001483724319,0.0001250138771,0.00007841298754,0.0005480399814,0.00009644807976,0.00008773111422,0.007574339793,0.00002789170236,0.0001709010819,0.0000386537923,0.00006256413531,0.0004613635427,0.0001665776547,0.00003995411021,0.0001754236063,0.0002618863867,0.00001811255269,0.002852152405,0.0001904509563,0.0003054293439,0.0001663770312,0.0004801460161,0.009712231229,0.0001317618924,0.02490799026,0.00004394958512,0.00005484420438,0.0006425903378,0.001104117615,0.00003460786746,0.00004602372497,0.0001151282085,0.0001844117845,0.0006134686692,0.6079888025,0.00007767357311,0.00005358515865,0.0004558474303,0.009157073674,0.000121949763,0.0009506112968,0.0001868045091,0.0003629214083,0.0001843866785,0.00002233527278,0.0002285122929,0.004419412256,0.001795844166,0.00009393059517,0.0002546372489,0.0009642743742,0.00006159960739,0.00007140407587,0.0003293493052,0.0001260039949,0.001809202706,0.001573184547,0.00004035596548,0.0007016423859,0.0001203640839,0.00001128985061,0.00002031187624,0.0001834634028,0.0001560876092,0.001499765653,0.0004519749056,0.0001025259684,0.00004799726096,0.1520289673,0.00001936024629,0.01261867779,0.001251725244,0.0009721011893,0.00020818517,0.00005228820429,0.0001656599334,0.0005334572705,0.003117050637,0.00002191824675,0.002231905929]
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
