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
        experiment['cache_placement']['cache_allocation'] = [0.03809759598,0.0004326685756,0.0001396483419,0.0002107654821,0.00008228832409,0.0001992116453,0.0001398105405,0.009517148,0.00003894569013,0.0003197098963,0.01376567806,0.0002177098776,0.001557767377,0.00008738171396,0.004372704766,0.0003949234425,0.00003891015261,0.00003822319606,0.0676062495,0.00004768705361,0.00006825519874,0.00002660960462,0.0002563036925,0.00004722224248,0.0005137606233,0.0003109391967,0.0002646926026,0.00002573256781,0.0000119292127,0.0005693048142,0.003988416934,0.0001100983446,0.002544430368,0.0009697020878,0.00008653226133,0.0003374138421,0.0004648440763,0.0006543303455,0.0003971701684,0.001901721973,0.00002303024735,0.0001817890496,0.0005215482969,0.001209494807,0.00008300205719,0.0003496710126,0.003164795506,0.001742242861,0.0003791120424,0.0004455659809,0.00009433506219,0.0006685353714,0.00003765028836,0.0001556501566,0.0006932050881,0.00007220462302,0.00001391915951,0.0000514279887,0.00096559106,0.0007065984952,0.0004347489045,0.0001110590257,0.001584840856,0.02500943989,0.0002215688697,0.00506840124,0.002755295773,0.00005720163326,0.0004517024206,0.00007108262884,0.0001905415917,0.0002207379051,0.001182180402,0.00002189423411,0.0002418118363,0.1520333689,0.0005745660578,0.00005241162697,0.0001744908203,0.0008365376667,0.00003091221943,0.0005424745859,0.0001609132563,0.0003035069843,0.00008178732605,0.0001297261158,0.0000245836636,0.0002210181927,0.0001461276834,0.0001163426946,0.609207635,0.01266102722,0.002060989709,0.00009373640696,0.002131816676,0.0169253078,0.0006943551561,0.00006051996523,0.00002761369036,0.000671916438]
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
