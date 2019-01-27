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
        experiment['cache_placement']['cache_allocation'] = [0.06808336701,0.0001431009472,0.00008280220178,0.0008229966559,0.0002166609923,0.00005504364961,0.00001682960254,0.0001721729899,0.002671144302,0.0008101716223,0.00004960295233,0.00005445919401,0.00005103101575,0.003136926281,0.001036081346,0.02436761679,0.0006662266544,0.001788367498,0.00003947998056,0.0001767849187,0.0004963007987,0.1520811809,0.000009369956428,0.002237237521,0.0001185996808,0.0001657550191,0.0004425820108,0.0002339730649,0.00009511980496,0.00008002663021,0.00157657674,0.001428499477,0.0004185559582,0.01249953028,0.0005387448873,0.0000933020969,0.00005889678313,0.006219883804,0.0001675577123,0.0003331056298,0.0001126910696,0.0001279479802,0.002811152271,0.0004184773225,0.00009047405293,0.0001169126809,0.00007112158181,0.001353848876,0.0006416559244,0.002520657913,0.00004998890816,0.00005998002577,0.00008781981624,0.0006366324543,0.00003757465089,0.00003600320382,0.00005249560958,0.000178128762,0.0005856218493,0.0008270734571,0.0001861058166,0.0001730506485,0.0008305054231,0.0001268928806,0.03813293944,0.007639015811,0.0008606386568,0.00004802710043,0.0001961150798,0.00004940807836,0.0001677400381,0.001658102098,0.00008239813575,0.009534261862,0.0003673788677,0.000174891131,0.001040366584,0.0002550508405,0.00003260854971,0.00007575341077,0.6134174999,0.0000734320523,0.0001516367389,0.0002287269537,0.0001341370634,0.02052571272,0.0002346993309,0.0000348972113,0.0002338861653,0.001596716293,0.0000359168116,0.0007720334452,0.00002961067118,0.0003800974941,0.005097819204,0.000335383884,0.00003725525196,0.0002589581973,0.00007535661446,0.0001630498383]
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
