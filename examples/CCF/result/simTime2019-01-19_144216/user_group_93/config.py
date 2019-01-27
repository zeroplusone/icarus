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
        experiment['cache_placement']['cache_allocation'] = [0.0002290593257,0.0001387601747,0.00004400518371,0.0243354171,0.00008885922391,0.009536357813,0.00129162125,0.000651392604,0.001201948535,0.00009271737375,0.00004807578429,0.6079932297,0.0005476736222,0.0683488542,0.00005675406821,0.0009596901004,0.00005034003645,0.001498434345,0.001323740539,0.00001713214452,0.00007032685452,0.005219407402,0.00007067188638,0.00004347813128,0.00012931798,0.0004168259726,0.0006013564312,0.0001839113045,0.0002054418282,0.0002626488634,0.0001058000535,0.00004506365235,0.0001519876008,0.0001273348243,0.00002619578538,0.003797264505,0.006219121451,0.0006810092814,0.00004584011389,0.0001971866247,0.0002439079431,0.0004128722342,0.0002137911388,0.00005328181576,0.0008552307775,0.000180578631,0.0007828413742,0.00001328106584,0.0002474869476,0.0000438159359,0.00002594675189,0.0006110005464,0.00008891926504,0.0002716679538,0.0006533645458,0.00009530502568,0.0008365989629,0.001401166515,0.00001688676631,0.00001617820375,0.001742950872,0.0003445277433,0.00002454545924,0.00007929114421,0.01735281596,0.004119945978,0.03817268199,0.0003668937982,0.002155586375,0.01259531549,0.002850422695,0.00003148774121,0.00005941241303,0.00006324067832,0.00004061846971,0.00003938475056,0.001091093699,0.001796247671,0.0003312232123,0.00003156372986,0.00008333722424,0.1520293032,0.001237789175,0.007575684104,0.00006337364947,0.00003164859066,0.001975800686,0.00004725531846,0.0006059553191,0.0000755818259,0.004852274639,0.0000215560367,0.0000489061079,0.00004349341617,0.002551539151,0.0003536917093,0.0003878581056,0.0002114828209,0.00006708255277,0.00032876037]
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
