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
        experiment['cache_placement']['cache_allocation'] = [0.0002101135217,0.6082562668,0.03857189737,0.00004981853032,0.0006005563813,0.0169184181,0.00008647448666,0.004257583882,0.0001756155631,0.00006524634707,0.003657859627,0.001393059081,0.00005585397377,0.01292141039,0.006165269272,0.005209250103,0.00002259781056,0.0002286898127,0.0116164286,0.00005975367482,0.0001284879887,0.00001786402514,0.000718426869,0.00005118447243,0.0006645350713,0.0000772088932,0.00002458688153,0.0005132720311,0.00003508453982,0.00004554853202,0.00009211371975,0.0001969561337,0.0001612898018,0.00002980757841,0.00005866105367,0.00008027044436,0.0001954769123,0.0001200307092,0.0001993727762,0.0000725302059,0.0001337280118,0.0001588052841,0.00008673589685,0.0002720947117,0.00006437012664,0.0005777822024,0.002882822812,0.0002540124454,0.0001730436472,0.000134275949,0.0000442033696,0.00003179549217,0.001164580821,0.0002066465916,0.00003995396717,0.1530278018,0.0006425132509,0.001924727511,0.0003296177032,0.003175659548,0.002259282406,0.0002899148333,0.0001478302174,0.00008758312817,0.00002446643423,0.0001531460185,0.00005287616619,0.00008794944809,0.00003705302592,0.0001111616481,0.00002873429206,0.0005252378621,0.02607198254,0.0001311417656,0.0003473082682,0.0005487202532,0.0001261456846,0.00007562674141,0.000031517898,0.0002473079294,0.003630551184,0.001206155224,0.0004023992141,0.0002021155777,0.00003591414207,0.0006197152273,0.06761841119,0.0001806576793,0.002480595524,0.001241333842,0.0001055132112,0.00007075609403,0.008037563548,0.0008442009859,0.0003132208999,0.00001987762696,0.0006846066838,0.00006778418224,0.001492145717,0.0000314526393]
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
