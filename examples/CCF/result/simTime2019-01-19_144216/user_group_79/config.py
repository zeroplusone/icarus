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
        experiment['cache_placement']['cache_allocation'] = [0.00004143076088,0.0001575312436,0.0001333533901,0.00003426530272,0.00008605417614,0.0001061993867,0.0004209239882,0.0001474825328,0.06800607971,0.00005142241189,0.0000243287321,0.003679397468,0.03802335914,0.0001445376624,0.0004040051619,0.00005762371491,0.0001521154997,0.00001499467505,0.00002569205265,0.000009252972832,0.00004338625419,0.0002877550633,0.001454945715,0.00003531973491,0.0006153898884,0.01508322276,0.0004345547244,0.00103768507,0.00007309463476,0.007526408298,0.00008919267611,0.0001092245491,0.00002744270832,0.0001115976498,0.0002338342827,0.0001407348654,0.0002556932091,0.6080078077,0.00007797410254,0.0007579724696,0.0002221163141,0.00001776787855,0.0008551869394,0.0001983093945,0.001599685018,0.0001077153094,0.0001785074932,0.0009335167868,0.00008475672329,0.0007247004826,0.001426651499,0.001913068073,0.00002831088057,0.0001527333691,0.01415486395,0.0001825029089,0.0003234355349,0.00005724199312,0.00008626504688,0.00006613940493,0.006735681101,0.00009049277961,0.002153736278,0.0001419790612,0.001643501981,0.0003358818212,0.0003133175527,0.00007939053477,0.0004739711175,0.00001576746699,0.003194646735,0.0005508612662,0.0003891286918,0.0003339285631,0.0001565465278,0.0001193394561,0.000008892855394,0.02481263812,0.002478744774,0.0000257445336,0.00006207704948,0.0007668621047,0.0008912131878,0.0000135361074,0.0003823427395,0.000523644752,0.00008056453561,0.01898930723,0.00003217549433,0.00005455863519,0.0000836169938,0.003150734582,0.000172037065,0.001326456576,0.0002372165365,0.00006995197335,0.001100732102,0.1562950291,0.00007734588696,0.0001996448484]
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
