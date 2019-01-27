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
        experiment['cache_placement']['cache_allocation'] = [0.005154503077,0.00004565313992,0.6080043817,0.00111724507,0.03842735376,0.0002824667512,0.00001076095535,0.001847291965,0.00003837061729,0.002119695122,0.0002082652024,0.000122481307,0.0005939802519,0.001955670782,0.0002085839414,0.00009930393278,0.0002484120632,0.00002045852104,0.00003596921823,0.0001177274956,0.0003775608287,0.00006896930835,0.0001943443127,0.002198238405,0.0001176740385,0.0009329844198,0.007573248913,0.0003301566287,0.0001330788836,0.0001849352226,0.0003821620464,0.000403118504,0.2196276307,0.0001946325111,0.0001318607948,0.00002479709497,0.0002192671315,0.00002156702045,0.009859395692,0.001236082303,0.00007255167958,0.0002423522404,0.00008840363042,0.0006619305065,0.0003502625066,0.0001171123617,0.0002605279795,0.0005514594756,0.0004020481278,0.01691741875,0.0002155339919,0.000785624118,0.000336671287,0.00004546395143,0.001315684076,0.000009995888876,0.0001511064901,0.0001402804554,0.0001066948692,0.0003891569427,0.00003964061456,0.004356596788,0.002458020443,0.0001783215922,0.0002698293322,0.00007309893981,0.003119436499,0.001124417026,0.0005265896,0.001376043656,0.0001495485909,0.0001012901587,0.0007064572274,0.0004354156709,0.001175236308,0.00004323402681,0.00002399213167,0.0003349261756,0.00007811612561,0.0001617380899,0.0002151617311,0.00002329617405,0.0004701807564,0.00002241714362,0.0068725272,0.00007803616015,0.002743500898,0.00006043060059,0.00003982337903,0.01327464016,0.001397805654,0.0003146727772,0.003639399766,0.00003761042754,0.00003270231057,0.02526701387,0.0001367830919,0.0003731517054,0.0001161895867,0.0001221486634]
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
