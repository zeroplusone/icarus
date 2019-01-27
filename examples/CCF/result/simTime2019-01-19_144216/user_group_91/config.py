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
        experiment['cache_placement']['cache_allocation'] = [0.0005102445759,0.00130356155,0.00005862724065,0.0002534131586,0.0005154905302,0.0006272957404,0.00006993083392,0.002117124579,0.0000901090003,0.02486255461,0.0008585360985,0.00002803133084,0.00004635900161,0.002576660144,0.00001833385054,0.00004998661335,0.00003089896931,0.0002084283628,0.0001417163353,0.000215281851,0.0003587141609,0.0001900474997,0.0002312755921,0.000132671378,0.00003081082203,0.00006914684854,0.06767667058,0.0001092189811,0.0005881294556,0.007812533573,0.000347827824,0.000213072001,0.001645979167,0.00002416232615,0.03920119439,0.0009382774382,0.000120990104,0.000039256045,0.0002004652392,0.0002830525016,0.004663458433,0.6149914985,0.0009419186801,0.001602061338,0.0005387235964,0.00004575958807,0.0000697786401,0.0001232596243,0.00003078765067,0.0001144624275,0.00009016108607,0.1521125097,0.000140995568,0.0003859304285,0.005262963263,0.003235051494,0.0002678287388,0.00009076853259,0.005347158677,0.0002738490995,0.0001115141815,0.00002216700514,0.0005600212873,0.0004034255816,0.0007782355277,0.0001094839744,0.01255794348,0.001552395138,0.0004715621621,0.0001492377512,0.00005923327808,0.00005967435071,0.0004105494631,0.0008002667654,0.00005510350254,0.00003413257548,0.0001306542194,0.000546447592,0.00004507186567,0.0001090188664,0.0007309944062,0.00007139733247,0.00002070025919,0.00005103495486,0.000007786642516,0.00009283683472,0.0002391736702,0.0001821744359,0.009541343487,0.00004232060897,0.0008071485869,0.003619166638,0.00005105346419,0.00003928530669,0.002797645349,0.0004068598729,0.00006862402662,0.00003650439718,0.00006622396875,0.0170365818]
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
