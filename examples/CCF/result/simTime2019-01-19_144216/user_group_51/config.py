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
        experiment['cache_placement']['cache_allocation'] = [0.00005048337513,0.001148952141,0.005153853637,0.00004471663184,0.0003143970729,0.00002938942767,0.002125935143,0.0007399541628,0.03190774568,0.0001821401054,0.002300145811,0.00001765301765,0.003252695146,0.0007421288736,0.000167247541,0.000103077623,0.00021539191,0.0002018992038,0.0000168365211,0.06805579772,0.002297490404,0.0001161202848,0.00008038011953,0.002438168986,0.0005240803111,0.0001129701791,0.0003239722504,0.0003744200308,0.00004740887955,0.001054892157,0.6090723996,0.01122283938,0.0001209495318,0.0001362635966,0.0009133814782,0.00001831446398,0.00003707149515,0.002857837691,0.001285754964,0.00005450411774,0.000983693599,0.0007206360736,0.0006487268638,0.00005320102589,0.000194925293,0.00002620319374,0.0002078632095,0.00007774983072,0.0001531425496,0.1521280626,0.00002789556626,0.0001263693214,0.00009615793176,0.00040128759,0.00007733909309,0.000357349674,0.000218084408,0.001937520261,0.0001268973116,0.00004290022892,0.0004313793445,0.004309339404,0.0002019203441,0.0003604490671,0.00029482537,0.0007789049131,0.0000290074179,0.000183112738,0.03804446168,0.00005170815814,0.0002924515079,0.0000421956095,0.0001473639611,0.0009978395412,0.006189260685,0.00008129999739,0.0001304260482,0.0001249352132,0.0006855205746,0.001636494772,0.00007358668289,0.01716079038,0.0002746817421,0.0002734964154,0.00003939491119,0.000459235495,0.0002085003607,0.000213609887,0.01261515337,0.00004333653018,0.0001193706717,0.00003191141997,0.00003785676975,0.003618166475,0.00004313581088,0.0005478307644,0.0000469681959,0.00008591544567,0.0001806881613,0.0004478079548]
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
