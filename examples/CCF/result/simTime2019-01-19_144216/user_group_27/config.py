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
        experiment['cache_placement']['cache_allocation'] = [0.0004314763521,0.00033699257,0.0001618730129,0.0005411751047,0.0001271701065,0.0003244601582,0.1520879898,0.0005865716335,0.0004348359507,0.07471907449,0.0001937004606,0.00003435589702,0.01744379753,0.004306161589,0.0000614622575,0.0002734615659,0.003130487899,0.00005751867271,0.00003039921293,0.00007777789521,0.00002680327196,0.0002336520917,0.0001911118978,0.0000850664181,0.00001631240624,0.0007444567553,0.0001864668843,0.0003049111819,0.0008297068081,0.0001946126203,0.0005467513574,0.0003295053407,0.001025864657,0.001744863619,0.0003697420259,0.0001388473428,0.0007451961499,0.00007113657468,0.00006895156547,0.002155688765,0.00008675802857,0.002880694939,0.0002827913473,0.0002509095948,0.0004243352346,0.0005582753796,0.0008446911976,0.00001728049276,0.00009919498091,0.002477614833,0.00001986870122,0.00005617356698,0.005078993341,0.0001970454167,0.001983478452,0.00006196500021,0.00003561416292,0.00005577364234,0.000165180468,0.0001170474953,0.000242435232,0.009636037045,0.00002388020681,0.0000550636544,0.00008027169014,0.00008711869015,0.00003124480318,0.001744123913,0.00008857653031,0.0001998420118,0.00001083288419,0.0001046234753,0.0008272588621,0.00001334099456,0.01244731641,0.000150905515,0.0004068255298,0.0001689100399,0.0005303139156,0.0000454995489,0.007907206649,0.0004693314798,0.0009366952863,0.0006828533694,0.0002497980702,0.607996208,0.0001507244669,0.001226531962,0.00001923838293,0.00006689094394,0.00005652049231,0.0002189983307,0.03907163455,0.00009830622305,0.00009210878842,0.006077056443,0.02572129757,0.00012778628,0.00009200190244,0.0007803136692]
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
