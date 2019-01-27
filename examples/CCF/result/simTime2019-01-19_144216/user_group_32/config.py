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
        experiment['cache_placement']['cache_allocation'] = [0.0001067780231,0.0004926712628,0.00001860444187,0.007558567845,0.00007591990355,0.0009330185614,0.0001984059436,0.0001747803097,0.0001377141432,0.00005045111123,0.0003194151968,0.000026988412,0.0004898923576,0.0000518578909,0.006897031585,0.00005899655181,0.00112414257,0.001278763128,0.0001132291812,0.0001025344072,0.0002107597186,0.0006500707319,0.001077228192,0.003135312244,0.00002888114781,0.006541897158,0.0000544212277,0.0000654615855,0.001443305314,0.0001240521491,0.00003767161886,0.003115795563,0.0001775170497,0.00004739621147,0.0003813790626,0.00002733222254,0.0001446850152,0.001600722291,0.00005930390752,0.0001046095389,0.0005055905315,0.005056898353,0.00003856090253,0.02483149484,0.00002707847268,0.0002864271494,0.00003640987744,0.005225570862,0.000329712712,0.03934344746,0.0007944683322,0.00045614871,0.0002327928778,0.00006098263776,0.0001458265423,0.00009098363718,0.00003083909316,0.0003350126186,0.00007771899565,0.0002780571199,0.00005708986951,0.000166724868,0.00006502936542,0.0007569264971,0.0002382231554,0.0001085928298,0.0116310185,0.0124827292,0.0000972589521,0.00004855553637,0.00001828272311,0.00002273748136,0.0005959737713,0.01691542517,0.0000387535566,0.002455956421,0.00003092186731,0.0009793660334,0.0003074665275,0.001910475136,0.0003279033403,0.00008208830396,0.00002075201179,0.0002046826203,0.0002114688504,0.0001097572397,0.06773328106,0.00001872695372,0.0006862578991,0.1522478853,0.0002299401848,0.6090484783,0.0002828506787,0.0008832652205,0.000123575392,0.0002967330056,0.0001825986098,0.0001647446505,0.00004909494079,0.0007468215145]
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
