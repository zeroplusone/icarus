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
        experiment['cache_placement']['cache_allocation'] = [0.00007061809427,0.000227982404,0.001863877281,0.0001649512504,0.00004208570202,0.0007420869596,0.0002569111106,0.6080135829,0.0001440681,0.00390076396,0.0006266225355,0.1057107976,0.02434222315,0.00002219877443,0.00007173338437,0.001714271709,0.0007468009173,0.009512637448,0.0002335048322,0.001198451993,0.01301247806,0.1520170333,0.00006489663643,0.0001289492404,0.001080053463,0.01937075624,0.00005657826856,0.00008431063912,0.00007407521328,0.0007926626009,0.006173641363,0.002050581965,0.0001908960352,0.007522715892,0.0001224266359,0.0000527120292,0.0001335945164,0.0001595065222,0.00008262871721,0.00009338097664,0.00003783564012,0.00002522536676,0.000173808474,0.00008172367754,0.00004315687226,0.0000736925117,0.000115558124,0.0001233539404,0.0001593034397,0.0002191334187,0.001339870071,0.00002668107273,0.0007837037054,0.0001009692393,0.0001160964476,0.0001085928353,0.0005588201611,0.0001332860232,0.00004216375499,0.00002148713182,0.0001121764961,0.0003239599961,0.0003758737987,0.00005689748525,0.00005167836192,0.002507358991,0.0004826948084,0.00003353710092,0.001517984543,0.0004248453698,0.0009693167721,0.001125217827,0.00003510861425,0.0008576555338,0.00003975776982,0.001204319831,0.00008989098365,0.000365334321,0.0009134495107,0.000111522171,0.00002898230324,0.0003725101012,0.0003698146118,0.00002760812017,0.0001038780549,0.0006842010678,0.007411406065,0.00004824977058,0.0003079172179,0.00004908922497,0.00006258524066,0.003714738142,0.0009565501749,0.0001999028199,0.00005629069303,0.0007410117688,0.005154671912,0.0003240375877,0.00003426158361,0.0005992029197]
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
