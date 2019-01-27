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
        experiment['cache_placement']['cache_allocation'] = [0.00006384606658,0.00006410931585,0.00009028091021,0.0005989224159,0.001370761023,0.0006172448633,0.00005159361176,0.0004137841007,0.00007944568124,0.0004366636179,0.0000304893437,0.001737080775,0.0001681709759,0.03826277374,0.0001695175725,0.0002198275531,0.00007348298558,0.005087717873,0.0007153535076,0.001058579945,0.00004318150469,0.0002330079118,0.0001238935382,0.00008776951295,0.0002803397041,0.0005151756733,0.15219511,0.007540900384,0.003475643847,0.00003973337932,0.00001361164624,0.00001830541586,0.01736465272,0.0008097859414,0.01248042894,0.0004084467839,0.000835037472,0.006394592511,0.0002847877389,0.00002846899532,0.0003988264934,0.006188282777,0.00005417608144,0.002426221284,0.0000566841424,0.00004947327823,0.00002385099977,0.00005389772333,0.0003505994198,0.00003049003552,0.0000667342902,0.005832025377,0.0002052547209,0.0001916682418,0.0001237221232,0.001403923807,0.000222375252,0.00006538209413,0.0002896637322,0.0002216241453,0.00009602673314,0.000185385359,0.0001333669394,0.00212117682,0.0006618162567,0.0009828247974,0.00004102829218,0.0008386715893,0.0001726553856,0.0004181811217,0.0002135110878,0.00001025776551,0.001106547329,0.00002624082816,0.00004244548277,0.00005885100543,0.002736816165,0.02470782121,0.009572236662,0.0699942448,0.6079837394,0.00003318859309,0.00006349495371,0.00001205289015,0.001268231284,0.0000322101765,0.00008385320489,0.000478049552,0.0001655147021,0.0001641068579,0.0004399740188,0.0001981194503,0.001413047253,0.00008756833373,0.0001910338231,0.0000824450845,0.00007116334758,0.0002714565211,0.00005254908754,0.00005070030336]
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
