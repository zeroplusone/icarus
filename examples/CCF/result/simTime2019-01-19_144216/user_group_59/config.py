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
        experiment['cache_placement']['cache_allocation'] = [0.00002526341689,0.002216832053,0.0005739934322,0.001005690184,0.0001020216571,0.00009356031738,0.00004037431149,0.0006574622739,0.0006345642008,0.00007757335826,0.004243631025,0.002634945195,0.00003116348829,0.0001085871958,0.00009334832058,0.0003358303986,0.0001142119003,0.00004952250833,0.0003448889947,0.0002550031101,0.00007035762967,0.00008032625651,0.0002292318052,0.009192313551,0.00009812116078,0.0003151344453,0.00001472443011,0.000345180622,0.000155882636,0.005062597817,0.00003016373159,0.0000407804592,0.06837424283,0.00002776089733,0.02448561162,0.608117247,0.000018402706,0.00003719372061,0.00002440807436,0.009561439231,0.0002173604097,0.0001240833926,0.00005099691747,0.0001898790767,0.00007203680363,0.001063316783,0.003953296438,0.00002323515807,0.040738903,0.00004137332481,0.0001322185609,0.1520287252,0.007831543475,0.00001477649267,0.0001308907688,0.0000971118145,0.00005036123775,0.00004180944728,0.00006419895894,0.000410205397,0.0000954927228,0.000113059752,0.0007761356285,0.0004645782422,0.0001647862994,0.00004647580592,0.0006683781071,0.0001338272542,0.00002313259438,0.00006245586103,0.0001220537534,0.000473454955,0.00004191055712,0.01813784312,0.0001886524495,0.001460437478,0.001195622904,0.002113463986,0.0001306945039,0.00009286266016,0.0006500940631,0.0000175740081,0.003461788047,0.00004273635249,0.01250932878,0.00006225115802,0.002086665921,0.0004422359811,0.00003919166208,0.0005621242743,0.000152772186,0.0002383862684,0.0005133858716,0.0005143231969,0.00001990495532,0.0002755070443,0.00005427722297,0.002086649616,0.002159728798,0.0004098453486]
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
