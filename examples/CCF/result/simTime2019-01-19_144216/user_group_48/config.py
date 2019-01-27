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
        experiment['cache_placement']['cache_allocation'] = [0.000290224001,0.00007110454963,0.0005074390202,0.0009014346622,0.00001869738579,0.0002447806586,0.0002866259817,0.001689651417,0.00002016298907,0.003238134451,0.00007597561033,0.0001674140806,0.0001671830691,0.00374383736,0.005052316492,0.0001742645871,0.00007778734544,0.0001048041706,0.0001751007034,0.0009156903479,0.0003018036613,0.02435964273,0.00001905107337,0.0007633482776,0.0001366965005,0.01046541615,0.00003096167711,0.0001259518693,0.00006345493471,0.00241519557,0.0007643618457,0.00010413654,0.01244658766,0.000507731717,0.000438506481,0.0002939770502,0.002514316711,0.1520915313,0.00003576064034,0.0001037894257,0.01699609684,0.0004905774688,0.00003327424432,0.0002984347678,0.0005967026796,0.0001853907406,0.0000502628458,0.00002176530288,0.0001319861459,0.001970833451,0.0002683980111,0.006255202315,0.00002619524944,0.0003753662815,0.0002166803302,0.0002204401396,0.0002083648778,0.00006536719949,0.00006426013618,0.0002509897637,0.00001951378134,0.0003054767653,0.0005198214449,0.0003236996927,0.00002789027514,0.00002048039157,0.0001471426731,0.001260242992,0.00009057902645,0.0001807831978,0.0002861330244,0.0000127219459,0.00001816075812,0.0004112927292,0.6080765771,0.003142701012,0.00006070412899,0.00002480831477,0.001523191215,0.0002767722333,0.00004296263293,0.0003128568349,0.0000182485411,0.00007748197508,0.00008116357434,0.0001059858618,0.00002328361095,0.07560475257,0.0003963802023,0.001912251859,0.0009047851713,0.00009567356876,0.001166370121,0.0004747613095,0.001129064507,0.0001066160365,0.04110572906,0.00004864147705,0.0007743910974,0.0042584678]
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
