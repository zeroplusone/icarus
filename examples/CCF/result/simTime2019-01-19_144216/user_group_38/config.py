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
        experiment['cache_placement']['cache_allocation'] = [0.002474772439,0.003437777783,0.001194049744,0.00006373603739,0.0003517314869,0.00004456939218,0.007536700068,0.00009157708885,0.00003416120682,0.00220232904,0.0002743644233,0.00001748599937,0.0003447257842,0.0009527954111,0.0001687252418,0.0001039794015,0.00008183924744,0.001286390022,0.0003655733024,0.001685373194,0.0001748080157,0.00009979487467,0.00001570647717,0.0001935434665,0.00005439473168,0.00001412406845,0.0007449169661,0.00009401464393,0.0001455839058,0.01704965607,0.00009437493504,0.00004082864555,0.1765819342,0.00001836993535,0.00004515353523,0.001488785691,0.0002662188876,0.0001051489085,0.0006197632152,0.0009948775555,0.00062037026,0.0004405583074,0.00008934693621,0.0003811021131,0.03954289853,0.0000374676433,0.00006377326684,0.00007135470328,0.00004603771653,0.001108678514,0.0004646531674,0.0002199402206,0.0002172839189,0.00005853058034,0.00002788146494,0.00327798605,0.0003722192033,0.0002091549006,0.000609645452,0.0001714619069,0.07266572552,0.00002174271283,0.0001726376606,0.001265743124,0.0001462798027,0.0189851877,0.0008879919806,0.0003144544827,0.0001728039432,0.0002428474192,0.0005350739403,0.0001778119714,0.002758181775,0.00004505480871,0.00005682052068,0.6097048457,0.0001047827766,0.0004907558798,0.0002845181729,0.009536826292,0.00006894712208,0.0001714138485,0.0002174399515,0.004270493308,0.00008238109196,0.0001936649168,0.0002096388195,0.0002268140931,0.0001119570116,0.000129733017,0.0001974392453,0.00005520473441,0.00005469653877,0.00009725218793,0.0005335468058,0.00008078188243,0.00108188551,0.003918350535,0.00003890360318,0.0001043697748]
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
