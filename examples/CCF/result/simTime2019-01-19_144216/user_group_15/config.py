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
        experiment['cache_placement']['cache_allocation'] = [0.00001568560798,0.000234947383,0.0006703650015,0.0001340734928,0.0001252329681,0.0001229273163,0.001388019805,0.0002165668328,0.0009745211795,0.0003455224331,0.0002953898513,0.0001018127031,0.00003665152793,0.00003265794671,0.00008130841376,0.00001812190038,0.00001135645693,0.0006220554966,0.06776321456,0.0003501481478,0.00009941056379,0.00004259009301,0.000021712753,0.00007495456154,0.001943438568,0.00005110912154,0.00004517626506,0.002541363387,0.001603111004,0.00006587164,0.0001194506112,0.00004186656353,0.0004462854375,0.00004067637212,0.00005745082579,0.00003254969344,0.005210487767,0.0001366728088,0.0003171706997,0.001082966326,0.005229865578,0.0003151655829,0.0002586231947,0.0002583203579,0.001791751508,0.0003712954875,0.00003481221094,0.01703364029,0.000222257031,0.1521413678,0.000137776996,0.001134027636,0.00004494707804,0.0008698682402,0.000152715528,0.0007844102619,0.00006883600621,0.0001685977666,0.0005626709432,0.001319776764,0.0001959520897,0.000142801119,0.0003675425074,0.00002142629589,0.0001237753283,0.00003981200758,0.0001175106205,0.00003721695044,0.00479436581,0.0005616687771,0.009691339002,0.00002548928565,0.0002966545447,0.6081093151,0.001670300133,0.00008126889168,0.00813394556,0.00009578096552,0.0004586352981,0.02463378249,0.00007837366975,0.01275652565,0.0001115790105,0.00009566162274,0.03841779621,0.0003857999924,0.0001723763473,0.002858089359,0.006104516205,0.0007466536903,0.0001065463844,0.0007884364503,0.0001352957346,0.004129286546,0.000112184788,0.0001484231906,0.0001955252577,0.0001402628929,0.002483795016,0.00001866883157]
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
