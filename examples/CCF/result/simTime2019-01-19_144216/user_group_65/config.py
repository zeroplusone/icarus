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
        experiment['cache_placement']['cache_allocation'] = [0.003185401659,0.000464914635,0.00006261684437,0.00002525489072,0.0000284334219,0.0002296383548,0.0001560439758,0.0001417600862,0.0001783766842,0.03822048442,0.0009841542989,0.0003973955172,0.000773229349,0.0002317462077,0.0001167498906,0.0001203333578,0.0015179857,0.006169232362,0.0003270230852,0.001172522301,0.001127309635,0.00007452660722,0.0003161589551,0.0005781843477,0.00007773493786,0.02436706749,0.0008943867135,0.0680597863,0.00004231874151,0.0007842254557,0.00003736911073,0.00002106707947,0.002187809731,0.6079527824,0.0005432591293,0.00007377910909,0.001052395513,0.005203270501,0.00008375480509,0.00005236250367,0.0002393015049,0.0000855478701,0.00007938102096,0.0000370059923,0.0001339535592,0.01070381447,0.001621074066,0.0003437686907,0.00005568021137,0.0002577057708,0.009736041471,0.0002162872297,0.01705219572,0.00007136098075,0.0003198147957,0.0002164631892,0.0002414680688,0.1521277871,0.0007896626829,0.0002826557142,0.004580216466,0.00001639876716,0.0002145654429,0.0001196291078,0.00008315542575,0.0001368727505,0.00179877845,0.00001923553442,0.004463353201,0.00001885269039,0.0009226885721,0.0002036852413,0.0007216408553,0.002442040866,0.00001594619798,0.00002672255971,0.000215683152,0.0001319439426,0.0005379346562,0.0001877625551,0.00009784249011,0.003446107056,0.0004051269738,0.000559014375,0.00005987224937,0.00004243617866,0.0001825021728,0.0004483196874,0.00008203599377,0.0002236185462,0.0008810973305,0.0002931957582,0.00001461665338,0.0004153424323,0.0001911349634,0.00004653727908,0.000338925794,0.01251400543,0.000103593042,0.0001537529744]
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
