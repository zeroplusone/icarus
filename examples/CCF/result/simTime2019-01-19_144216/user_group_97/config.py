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
        experiment['cache_placement']['cache_allocation'] = [0.0005100422165,0.0002980016258,0.0004898746805,0.0005501045268,0.00002918465381,0.001490779238,0.0001699110087,0.0002365173671,0.000008439863287,0.000247848482,0.0006705602131,0.000161357059,0.0004946094368,0.00003838201315,0.0003065446457,0.0001909677057,0.00001532076855,0.00003664302665,0.00009774473539,0.0001128290757,0.002445695344,0.01267554928,0.0002152057981,0.007689630548,0.00005907597298,0.001349723902,0.001993612166,0.00008456971097,0.0001594842787,0.0001036780765,0.00006767226033,0.004328512583,0.003872923167,0.00007166347422,0.0006382393087,0.06815404027,0.1520494561,0.00005770307937,0.000319732972,0.0004212068396,0.0009546130261,0.00001224836171,0.00009969284683,0.0001527747472,0.00004089017359,0.0001317135442,0.00002697956438,0.000166182364,0.0001090312228,0.00009159099367,0.04035332714,0.00009825931269,0.0001861192937,0.001375204512,0.0004796049248,0.000124177428,0.0001859951503,0.001551643854,0.0007004598724,0.00006834894813,0.00003690010918,0.00004424582748,0.001131417115,0.00006666544492,0.0002566672434,0.0001632117515,0.009791773575,0.0001913359766,0.000120316722,0.0001232485586,0.00008344187777,0.00004571732382,0.0002170379586,0.0001939654809,0.003142376439,0.00001682252667,0.0002520171132,0.0001404709061,0.00141571243,0.6082884812,0.006182358513,0.0002838467212,0.00005257121336,0.001032488173,0.00004336569455,0.002825183164,0.0005615692928,0.005975776712,0.00009996519143,0.00007044264137,0.0006762397357,0.00004032338743,0.0001733001455,0.00004860327376,0.0169193057,0.02433491398,0.00366928714,0.00007269947329,0.0007212617545,0.0006727777377]
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
