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
        experiment['cache_placement']['cache_allocation'] = [0.0007658138705,0.0002611446631,0.00003848286841,0.00004963896052,0.0001106229686,0.00009513213122,0.0000458132305,0.009544524973,0.000396197736,0.00008744309102,0.003303282998,0.0001173989744,0.00006192835081,0.0006168198899,0.00004116078864,0.0003061639082,0.00006644952228,0.002542414964,0.6079526715,0.00004845320465,0.0009166302031,0.0008846448496,0.001610749692,0.0007400003904,0.0003138664152,0.00007930440552,0.00004579015271,0.00002479119224,0.0000726625675,0.0002233729188,0.03676539461,0.0002254774544,0.00009352968142,0.0003441903541,0.000539708602,0.001047988927,0.00003000563145,0.00009270207352,0.0009473983952,0.0004207697175,0.0008559033325,0.001137063154,0.0000387624612,0.0002368758232,0.0002989833865,0.0001821830832,0.00008747369027,0.0009123444486,0.002956497261,0.0001250106546,0.00004729333681,0.0001694883271,0.0000667215573,0.1689238077,0.00007917866828,0.0002010826998,0.0001103134214,0.00004836510614,0.00136284147,0.00004438018879,0.005938575746,0.00002217606636,0.04354539373,0.00007055321384,0.0004001506912,0.002029786046,0.0006330477449,0.00004251363604,0.00001487712119,0.00005546796292,0.001047847717,0.00006800241505,0.0001848762625,0.00002098046877,0.001309222774,0.00003421150257,0.0003507400302,0.000156133155,0.001989403652,0.003728727276,0.00008264329609,0.00004417860276,0.0001502931888,0.000378841288,0.00005209553888,0.00004024114787,0.007636356124,0.0001023684791,0.00009412431688,0.0002026312944,0.0001082643905,0.0001165522929,0.006576257433,0.00002222146179,0.0004153143435,0.004216691233,0.0003682313049,0.00007273243408,0.06785378508,0.00006838294936]
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
