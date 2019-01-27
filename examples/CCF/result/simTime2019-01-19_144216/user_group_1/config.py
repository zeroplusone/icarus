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
        experiment['cache_placement']['cache_allocation'] = [0.01291957078,0.00003816459366,0.06911909856,0.006835310073,0.00005752527959,0.0001094052406,0.0001993847036,0.00006151351122,0.00008501703038,0.0004309964367,0.0003067051433,0.001295845819,0.0001960971711,0.0002037908799,0.002273068157,0.00002386691722,0.0001716281155,0.6108168951,0.038529368,0.002571146928,0.0001992316331,0.0001175039148,0.00009893780687,0.00006346267011,0.0005022672669,0.01694283063,0.00009850640472,0.0001805665806,0.0001013267855,0.0006842009872,0.00001120136184,0.001283497011,0.0003429776964,0.00009171686952,0.00004084771957,0.0001480598292,0.004295194106,0.0002086990644,0.002080426944,0.001398048389,0.000369562167,0.009744751445,0.00006790365326,0.0002420046862,0.0004375804458,0.000250429378,0.003193855888,0.003628880165,0.0001140990283,0.00003009322562,0.005967447583,0.00008508614805,0.001092804667,0.0002273587381,0.0008066448609,0.00004606610026,0.00006088031726,0.0003853556991,0.0001236590437,0.00001890595095,0.00003804060523,0.001057062157,0.001803834125,0.00002318291573,0.152044426,0.00007084231576,0.00760356447,0.0003472254403,0.0002754453171,0.0005472659752,0.001761251835,0.00024090433,0.0001393853838,0.0001883953841,0.000740249634,0.0007780717883,0.00004149992598,0.00109288212,0.00009152549804,0.0002628079715,0.00004909435113,0.02523416432,0.0005123713049,0.0002593885858,0.00007196767064,0.00003947586951,0.0002877841154,0.00006953065744,0.0003119714759,0.0005276583221,0.0002378884133,0.00002290377691,0.00003437267351,0.00005300998993,0.0004518600655,0.00006601519101,0.0002144206184,0.0001857521532,0.0001259606431,0.00006927537857]
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
