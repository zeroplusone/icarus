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
        experiment['cache_placement']['cache_allocation'] = [0.00009421416285,0.00003589835236,0.00003602387573,0.00279367721,0.0001448874638,0.0002429613172,0.00002775144052,0.0002205298212,0.0001493216965,0.000090796102,0.00007904805775,0.001756062123,0.00001724704206,0.000166606554,0.00001878680897,0.0001314173733,0.0001809989679,0.0003419558328,0.000114232815,0.0001666031563,0.000259054261,0.0001384884902,0.0000833062558,0.00004681308438,0.0001265917895,0.005093646333,0.0001028760269,0.00002718351236,0.0001300262645,0.00002130038207,0.0004630357291,0.0001561987429,0.6080836816,0.007806212965,0.0009494846231,0.0003176257172,0.000122492285,0.009638717898,0.0001436182571,0.0001620654719,0.00006252041562,0.00006531270885,0.003912182091,0.00006997226721,0.0001079151449,0.001579361499,0.006320960437,0.004302997168,0.00004331154532,0.00004337981052,0.000438393803,0.003329812777,0.001048254344,0.00006691444786,0.0001035596045,0.0005244127713,0.000290520888,0.00003050232974,0.001885221606,0.0000206174849,0.08465609773,0.0003192759726,0.0001248303895,0.0005280146437,0.0005429931341,0.00009774193533,0.0001155473727,0.00003997071082,0.006923080345,0.0002008718493,0.0009325713877,0.0007273463696,0.03806313449,0.0007072171089,0.1527538707,0.006370631287,0.00006586559979,0.00001694130869,0.00006898352133,0.00009221821626,0.00001501643596,0.000314842607,0.0005003472464,0.01261940169,0.02479109498,0.0007288814543,0.00003939152977,0.00003869471657,0.0003224233214,0.0001511669684,0.00001229433461,0.0002457469559,0.0003104774105,0.0000789082311,0.0001158318604,0.00009416640254,0.00003277579169,0.0005681735421,0.0001204749267,0.0006251224966]
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
