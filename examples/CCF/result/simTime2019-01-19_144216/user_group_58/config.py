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
        experiment['cache_placement']['cache_allocation'] = [0.002492776384,0.0004974611753,0.01017237817,0.002056462698,0.0002825295269,0.003445731894,0.00003858855336,0.0002240144455,0.0001583177008,0.0005039520749,0.007886285094,0.002859109872,0.00003006596321,0.001404165315,0.00003429795871,0.001106998894,0.000163424729,0.00006412815915,0.0006125019543,0.0004080991454,0.0004872815943,0.0006681270605,0.00007771476405,0.0008224708176,0.001392673759,0.00008809444401,0.00007729876287,0.00002866512891,0.0002218097568,0.0003504250636,0.00002777263775,0.00005299402182,0.00004864593822,0.0000303935328,0.1520248331,0.6080369611,0.002354179323,0.0004136865092,0.0002200297789,0.0000456023344,0.001417641317,0.001496814948,0.00008075070513,0.0005679138436,0.0001584311192,0.0001381315697,0.0003899900693,0.00005214306612,0.004144791639,0.0001861663531,0.0007172021465,0.0001245345118,0.0003077772247,0.0004817865327,0.00004830232918,0.00007046681379,0.0003915113833,0.01034897577,0.00003235680333,0.00002242928213,0.00001870424995,0.00004793445927,0.00002766641354,0.01242552794,0.0001630663838,0.001186535785,0.0000821966582,0.00001202952403,0.00002072513444,0.0004671112923,0.0005443608379,0.0001700077882,0.0001814536893,0.000922129383,0.0000784880909,0.00003240162614,0.0004147389564,0.0001159657679,0.0244008255,0.0001251013836,0.00004812914466,0.00001912470979,0.0001846350314,0.00004555553319,0.0000321699682,0.0441299524,0.00008076558946,0.00002406382783,0.00005278548933,0.0002380132582,0.0002597340225,0.0002993186738,0.00005314461798,0.0002924092609,0.0001651418952,0.0002867430569,0.01698708426,0.0005513329316,0.0004469219215,0.071276937]
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
