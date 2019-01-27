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
        experiment['cache_placement']['cache_allocation'] = [0.00003135880974,0.00001946931819,0.0001338718565,0.0007672002646,0.000309263296,0.0003562140868,0.00964637605,0.001285410057,0.00003417171558,0.0003871255442,0.0001938279428,0.0001460695666,0.00008901177681,0.0002319015168,0.02446875593,0.0001801894108,0.0005348704012,0.003768531859,0.00003411278945,0.0004834674213,0.00003586280404,0.00003493540112,0.03808260563,0.00008460584458,0.004355904524,0.0003884752714,0.000356183055,0.003946361667,0.000153448726,0.0000708746929,0.00001817458046,0.00004242437577,0.00007045410141,0.005245324936,0.001295791912,0.0009223474881,0.0001015096729,0.00008921345643,0.00007424993935,0.0002954319873,0.0002632496447,0.001082535869,0.00007410580406,0.00008816015885,0.00002294829561,0.00003892210652,0.00006328684609,0.00003078691227,0.0005444124841,0.000654685478,0.00005058479286,0.0006708713367,0.06756052002,0.000139325448,0.7660957979,0.0005661000969,0.0003677903142,0.0001242571385,0.0001851340646,0.000358154078,0.0003581949766,0.00001346088069,0.00239302096,0.000135865008,0.0001769402733,0.0008201903114,0.002752459056,0.00211041872,0.0001135402096,0.0004625279896,0.0001941428236,0.001227004896,0.0002587053782,0.0001413620567,0.00006040062413,0.00003734850014,0.001530073332,0.0075462746,0.003756720499,0.00003434031204,0.00003134102978,0.001652653147,0.00003825240903,0.00009293887073,0.00004408406656,0.0002286990067,0.001069707949,0.00003463308711,0.0001108012633,0.00009143765913,0.0001335324774,0.0001970578003,0.00004936313951,0.0003420572412,0.00004204752982,0.001086573928,0.002021719352,0.00008678394824,0.01766274255,0.01311357368]
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
