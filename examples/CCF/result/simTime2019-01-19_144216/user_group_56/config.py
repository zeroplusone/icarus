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
        experiment['cache_placement']['cache_allocation'] = [0.0001117100103,0.005040259035,0.00007603818052,0.001641118071,0.0001619076567,0.001120412558,0.0006899393039,0.0000873651822,0.01272946515,0.0004935667776,0.0000285659544,0.00002116411033,0.0001160259523,0.00002303315912,0.0006426710731,0.0001981341297,0.00002559418683,0.02475205423,0.6081089392,0.00071505374,0.03807228051,0.0001352869958,0.001176998385,0.0001263880019,0.0007331190434,0.001338385743,0.00004536712489,0.0008275862519,0.00003024247319,0.0001983205849,0.00003668397191,0.0004618722115,0.009578764366,0.00005134782028,0.0000355729687,0.00003913372794,0.00006638453797,0.00007289352039,0.002174446605,0.00001267939206,0.00005080570579,0.0005027905724,0.0007181759432,0.0001883495537,0.00004913892405,0.000102965872,0.00004877752051,0.002544616328,0.00003717580887,0.0001582596028,0.0001997972787,0.001576185555,0.01695613262,0.000761465655,0.005378576186,0.0002412190522,0.001330197621,0.00004313562782,0.000029139425,0.006345451013,0.003960372126,0.0676803169,0.00005670874167,0.00005212844859,0.0000204231604,0.00008048739321,0.00003767666996,0.002834220322,0.00142414966,0.00005256545763,0.000393585796,0.00004443492222,0.001198130264,0.00007857752439,0.00006904409316,0.0005504321194,0.0001818475047,0.00004067193765,0.00112688542,0.0005657033883,0.00003768438621,0.000111477448,0.00004716636192,0.00003697028347,0.0001691813731,0.00008129264191,0.000133729917,0.0000345722692,0.0007833587328,0.000425165858,0.152054557,0.004343545876,0.009577419504,0.0006496652448,0.0001303175248,0.0005961893583,0.0002186279169,0.0006669602963,0.00004210293806,0.0001525254831]
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
