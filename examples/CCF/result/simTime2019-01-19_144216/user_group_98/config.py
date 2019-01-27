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
        experiment['cache_placement']['cache_allocation'] = [0.002751531345,0.00001861537104,0.00003467723081,0.00004388833582,0.00003527115181,0.000323593907,0.00003342238021,0.001169433412,0.0002900493847,0.0001286771523,0.00003433396468,0.0006388948915,0.001575636088,0.002138273568,0.0000299856423,0.0002640290308,0.00009888441686,0.001746886148,0.00009215998226,0.0007693858724,0.01292342735,0.00003202014166,0.003095916953,0.0004956090209,0.0003326783143,0.00002693806181,0.001345338456,0.00007223341914,0.00008925430646,0.0001562975513,0.00008476826292,0.0004374440059,0.0007816342301,0.001969091493,0.00004496239547,0.0001381419408,0.00003222416272,0.0001818560767,0.0002508167488,0.0001098890251,0.003617555909,0.0004733155668,0.0002775767017,0.0007884600359,0.009551845785,0.00005751281096,0.0003189781329,0.00008104545527,0.00009626465075,0.0000131627982,0.0004277249924,0.006108833304,0.001879023444,0.0003269250153,0.0011830399,0.0003666660281,0.0001227857497,0.00005499658518,0.0001656269198,0.00001608044438,0.0001811218729,0.0003136273503,0.00004302939264,0.00004626611566,0.0005078094105,0.007770157732,0.03829265693,0.00003022371355,0.00005671747696,0.01697438119,0.00003138812409,0.06758830123,0.0001122161105,0.005906463894,0.00001592092791,0.00006199973556,0.0001458924293,0.00008993079639,0.00006338992722,0.0001036877941,0.0001566434285,0.0000279011431,0.0008771138525,0.000208025208,0.0001855744384,0.03316287779,0.001643961565,0.0007440416717,0.607976024,0.0007307825475,0.0000204742566,0.000167085711,0.00004987911875,0.0001782329514,0.001410566205,0.0002095929651,0.0001236835577,0.1521222106,0.00003273323245,0.0008918222396]
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
