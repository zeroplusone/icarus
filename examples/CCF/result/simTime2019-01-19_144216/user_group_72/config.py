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
        experiment['cache_placement']['cache_allocation'] = [0.0003079101228,0.607948447,0.0002123182422,0.004044157553,0.0000853702519,0.0002030314566,0.0002326870869,0.00040516242,0.00008012291219,0.0006145077677,0.0001385625204,0.0001235823714,0.005149744207,0.0001017653112,0.01435958226,0.06966055581,0.00008638327956,0.00002262928957,0.00008165690896,0.0002483149362,0.0002256540049,0.003145264071,0.0005870561607,0.00004611857163,0.00009544898143,0.00022867048,0.0009413908592,0.003204362923,0.00007634968983,0.0004749405289,0.00002247716673,0.0001764863047,0.00003236197731,0.00161546402,0.001423193306,0.1520514273,0.004275709301,0.002163777918,0.00006562349421,0.0001481749285,0.0002344362113,0.000256166826,0.0001426985479,0.0001421437626,0.00002462087497,0.0004882483391,0.00007587576667,0.0007949165649,0.0002275253041,0.00002270572399,0.00003613242806,0.0001432265791,0.0009129608264,0.0000612909398,0.0001361557975,0.0003400762067,0.007917031978,0.0001531887903,0.0001981801127,0.0000130808803,0.01692160165,0.00006236999131,0.0007211838951,0.0006652523847,0.0003382820035,0.00002656011569,0.0009408356622,0.00002502437358,0.000104363046,0.0004500595149,0.00005662294331,0.0001964026794,0.00002893824883,0.00006184712285,0.0001993329578,0.001008576753,0.0006541947922,0.03808492614,0.00006561225193,0.009629931457,0.0006989874932,0.001548626411,0.0001552075144,0.0005581543134,0.0003942998766,0.00001520315739,0.001288428394,0.0005379852024,0.000046583022,0.00008296457194,0.0001192962333,0.0003795099717,0.03048772026,0.00003645261437,0.0002502889055,0.00007747102593,0.0009987980062,0.0009190751314,0.002594747602,0.001141176164]
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
