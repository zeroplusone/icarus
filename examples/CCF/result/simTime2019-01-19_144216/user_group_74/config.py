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
        experiment['cache_placement']['cache_allocation'] = [0.0001623539534,0.0001526785887,0.00004431708613,0.0002287589769,0.0001045326711,0.00003266397038,0.0002560737582,0.007520866435,0.00004724504269,0.0002950497156,0.0004989803409,0.002158312116,0.00009075780811,0.00005644498744,0.00008699619303,0.0005567474174,0.04503278934,0.00009719284407,0.0002962583134,0.00002036244509,0.00009471044264,0.00002965320434,0.009871727834,0.01743139153,0.0006030362545,0.00006608554726,0.0005806363006,0.00009316231818,0.0001400329631,0.0002506691411,0.0001041785204,0.0002395842858,0.001024407143,0.0003695077382,0.1522459664,0.0004965792275,0.001557827695,0.001981477262,0.0001523897597,0.01495735101,0.0000693772414,0.00004198826486,0.00008145775868,0.00002285420097,0.0008870152767,0.0001061959908,0.0001822516581,0.00003671073459,0.0001866068219,0.00002692745859,0.005061739934,0.0003615105543,0.00105382798,0.0004713259593,0.001092486318,0.00005868108262,0.001991573497,0.0002583417118,0.0000363122531,0.000030486474,0.00004975221036,0.0002844216491,0.02888817343,0.00005689285258,0.001182983829,0.0008899574187,0.06826382017,0.0000608564501,0.00008447980135,0.6080177006,0.0000218055198,0.00003885837867,0.00002594885309,0.003817204124,0.003930196754,0.00004160682006,0.00009246998785,0.002719776782,0.00009496580747,0.000159456807,0.0000472158647,0.00006261933399,0.0001152684415,0.001114265199,0.001672025059,0.0006131221053,0.001251567232,0.0001736503672,0.00001254734559,0.0001138396349,0.00003384940049,0.0002018454783,0.0002969760089,0.00280255932,0.00004678634299,0.000204111335,0.0002471242162,0.00005099292391,0.00007860462111,0.00005227379552]
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
