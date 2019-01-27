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
        experiment['cache_placement']['cache_allocation'] = [0.000296265752,0.1566146998,0.0002635397252,0.0000783120291,0.0001288782317,0.002599812475,0.00005963135522,0.00005488793481,0.00006224999066,0.002086544736,0.0005633863224,0.00002648641552,0.00005733137391,0.0002216611987,0.00008568201953,0.00006975583152,0.00009095390386,0.000561382053,0.0135996418,0.001185175881,0.0001962724669,0.0008665136791,0.00002413009181,0.0006005489963,0.00440230337,0.0001121095231,0.00004393080206,0.00003479817441,0.009829990169,0.00006844973943,0.009938486188,0.0001150304329,0.0001296077783,0.0382458759,0.0001923598207,0.0001412408009,0.0001518945322,0.00004913807177,0.0003563249599,0.001547457675,0.0009400159882,0.0008428137466,0.001294504195,0.0001726382866,0.0005653780109,0.02446817847,0.0004626637188,0.0169365377,0.00006247703338,0.0003775132475,0.0001984944994,0.00005000999706,0.0004890171998,0.001523397199,0.00002907638452,0.0001852903192,0.00008684475351,0.0006983808434,0.0000656412868,0.0004288829595,0.0001184542083,0.00007836264737,0.0001736292752,0.00001622553977,0.0001016972194,0.0009958645217,0.0003044129698,0.0003526273659,0.007599366906,0.00005363237288,0.0001022126893,0.0004782232301,0.0009056487256,0.003979612909,0.0009156692435,0.006209600661,0.00005953324406,0.0002023159135,0.0002482878687,0.00008162944302,0.00002155483482,0.0003342298004,0.0002222487694,0.0009401473963,0.00007415097795,0.00006716688535,0.0002025978654,0.0001444131204,0.0005162081485,0.0001569377915,0.000132673714,0.00001970874248,0.06764459589,0.0002109349931,0.0002139793007,0.6079991722,0.0001084981622,0.00003700346768,0.002248606558,0.00009766658859]
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
