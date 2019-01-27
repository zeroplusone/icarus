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
        experiment['cache_placement']['cache_allocation'] = [0.02448543945,0.0002535419551,0.01063399496,0.0001453739336,0.0004511669217,0.001533664057,0.0003845539123,0.00001357837041,0.0001125598645,0.0004629836506,0.0001193997775,0.0006174194202,0.00005255700346,0.00009070664356,0.00007972533567,0.001015685628,0.0007228039542,0.00002405399939,0.00006063555792,0.008024940843,0.00001472641957,0.6082900373,0.00004347524309,0.00008967315343,0.0002037470218,0.00009976109385,0.002435884916,0.0002783667639,0.001697247573,0.0000524330044,0.152169998,0.000475868438,0.00007480563398,0.0003637821299,0.0066800519,0.0002182789115,0.00007961399254,0.00004645604715,0.0009500098244,0.00277855963,0.0002071934376,0.00001454164865,0.0001292421503,0.009540031173,0.006109609176,0.000198458999,0.004275726048,0.00004592302834,0.0001210020487,0.06765121192,0.0001339046594,0.01283856704,0.00002496121968,0.000102012321,0.0001028703127,0.00003926118655,0.00006296398926,0.01701377099,0.0003859258673,0.0001039990797,0.0004318056159,0.00005838439893,0.002257427922,0.0002354995141,0.00289189613,0.001243116237,0.00006313249159,0.00005695661027,0.00004834860064,0.0002879135457,0.00001746825172,0.001911299928,0.000145523575,0.0001122228327,0.00008864334887,0.0002754812766,0.0002850105172,0.00007682596314,0.00003143339567,0.00007836027694,0.00006136862904,0.00001616306335,0.0001311080058,0.001201589047,0.0002030036241,0.000190320288,0.0009185881093,0.03803829987,0.0004039179404,0.0003050116165,0.0001607231917,0.0001252469378,0.0001722260352,0.0005114838562,0.0008085658105,0.00005131692998,0.00008156228953,0.0002417015419,0.0002367913898,0.000115522864]
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
