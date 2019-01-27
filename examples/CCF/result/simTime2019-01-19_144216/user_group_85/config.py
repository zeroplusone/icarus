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
        experiment['cache_placement']['cache_allocation'] = [0.00005065019143,0.00009455120843,0.0003386239267,0.0000873499982,0.00008621784696,0.00002392432339,0.0005521765088,0.0007141065378,0.00004395953917,0.002735466337,0.0005576283263,0.0005598884918,0.00006014094469,0.0002295492269,0.0002092342771,0.00001687566149,0.000319571571,0.0007657942388,0.001105071453,0.0006803215754,0.000158969544,0.004140716772,0.0002307284518,0.00005205067229,0.00006054868038,0.00003678734277,0.0001059765411,0.00004055750618,0.0006330141319,0.00004311038263,0.0009514964022,0.006240901769,0.0003615385189,0.0001375872351,0.00001825018379,0.04241402631,0.0004632565825,0.0003637109241,0.01694867997,0.00124086789,0.00007628903607,0.0004568592525,0.01262281036,0.003424980239,0.02455290747,0.0001140889428,0.00008679950537,0.0001016661497,0.01009672197,0.0002405666893,0.0001463660894,0.0003165493354,0.00002785221889,0.1595092773,0.002981261701,0.00005325800306,0.0002719024709,0.00006741590323,0.0001694596322,0.00230909508,0.0003121745005,0.001060849535,0.0007059218027,0.00001814060778,0.00004363214373,0.0009085471195,0.0001576937253,0.00003675975308,0.00001894764232,0.0001466362554,0.0001897231421,0.001412103589,0.0009430864388,0.0005567518538,0.0006621288161,0.00002193827839,0.0002114337359,0.00006155811737,0.00007339004295,0.001574653472,0.00013876832,0.0002157461549,0.0001083437672,0.00247841553,0.00005427868678,0.00004257990976,0.0004661712408,0.00004146773265,0.0008630282938,0.0001190940119,0.00006866058356,0.005146785514,0.00003324860224,0.0005677175018,0.002284634887,0.0000181849523,0.00006610702928,0.0000497292761,0.06758778353,0.6090331786]
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
