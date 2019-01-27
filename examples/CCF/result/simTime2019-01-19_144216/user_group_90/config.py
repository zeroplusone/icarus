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
        experiment['cache_placement']['cache_allocation'] = [0.0004733307832,0.00005397842949,0.0003217786453,0.0001071139995,0.001406371559,0.0004241312685,0.000130898204,0.0009828750941,0.0003185634437,0.01700537234,0.0002866081156,0.0003511955742,0.0002144934082,0.000998788684,0.002761805579,0.0007339876552,0.0003391658633,0.0008022069367,0.0002480730197,0.00002240618771,0.0001426324596,0.001184482745,0.00005639235045,0.0001044240734,0.00003265692658,0.0001100359157,0.0000210866317,0.00002231891198,0.0001303576607,0.0001021226908,0.00005062416586,0.0004378788848,0.00002251483968,0.0001389482179,0.00004447399145,0.1525522748,0.001886416004,0.00006221295983,0.002192936798,0.0001039953532,0.00007249032125,0.0005211924819,0.0001162163373,0.00003249478495,0.06767778115,0.00004431869855,0.000121727126,0.00008280770022,0.01274740897,0.0002237759705,0.0003630027556,0.00003946399175,0.0005748109307,0.00002274862692,0.0001988151741,0.01111246181,0.00008992314368,0.0002328545171,0.00001015090207,0.00008338484634,0.00002644958883,0.00002589499849,0.0003630038897,0.00003829141466,0.0003144424941,0.007785115969,0.03810765657,0.00156231161,0.0006830821792,0.00001307129878,0.0001622654033,0.00006655931406,0.0001980894763,0.00005872176661,0.00005239808132,0.0003852138786,0.00215551852,0.0007244308619,0.003646053326,0.0001493946688,0.0002271536144,0.0001326715986,0.007022463051,0.00312783977,0.608485337,0.000120891609,0.00008416755312,0.004244482428,0.001924675703,0.0003014956436,0.0001607365312,0.00002761972209,0.0001760818353,0.00009377850722,0.007629792558,0.00004670758452,0.00005058349816,0.02486542659,0.00003330316473,0.002977065296]
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
