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
        experiment['cache_placement']['cache_allocation'] = [0.00009672812835,0.002569163769,0.00003136967618,0.00008411141993,0.01699759902,0.000447807811,0.00002106601043,0.007588668463,0.000591840923,0.00008171473874,0.00006149845816,0.1527080083,0.0001595528618,0.00004312344879,0.0001627381765,0.00003446460629,0.000546034913,0.005144489496,0.00001349656186,0.00001093319372,0.0002594295776,0.000130067384,0.0001991921967,0.02205417831,0.0001253567718,0.00004174913446,0.00004210606628,0.000197528017,0.001274602912,0.00008173641501,0.0676243064,0.0009628505528,0.0001615882464,0.00065804187,0.00001775070961,0.00003067304278,0.004242428257,0.03825762336,0.00004542832458,0.0006678356172,0.00005103423197,0.0008996561988,0.00007484773766,0.0001100725111,0.00246299888,0.001414317371,0.0004198123741,0.0002565970551,0.0003377350393,0.001015931708,0.00002721887058,0.0001305833424,0.00004136737406,0.0001026609572,0.0001561373925,0.00004992310867,0.00009704796482,0.0003491185742,0.0002210150084,0.00003263650447,0.006169127261,0.001928246014,0.00003535994112,0.00002787548376,0.00006553831048,0.0002684171689,0.0003927014974,0.0001614362302,0.00006852065754,0.001044074627,0.00006043819193,0.0001203512576,0.0002660101658,0.00004459674278,0.0003127102112,0.001970792374,0.0001869472711,0.0007190589723,0.0001926464866,0.0004283233927,0.0001245357663,0.00002891145181,0.004709370882,0.02915794108,0.00006084455816,0.0006428497266,0.002467351605,0.00001793821402,0.00009979729429,0.6079805346,0.0004171745093,0.0003455025048,0.0003869554648,0.0005452244875,0.002981029088,0.0004460462957,0.0008103753834,0.000319609378,0.001192345458,0.00008289465963]
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
