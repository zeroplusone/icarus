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
        experiment['cache_placement']['cache_allocation'] = [0.0002368499946,0.00007538629843,0.000158135664,0.0000989367333,0.0005846572021,0.0007674561301,0.0005756334216,0.00009301136172,0.001705935157,0.00002246146424,0.00005798649989,0.003026333465,0.0000572946101,0.06797642738,0.0006902217072,0.01695784208,0.00004407551122,0.0001641518072,0.006219032787,0.003495740501,0.0005002395354,0.0001427086213,0.0002311861021,0.007767248142,0.0001719440095,0.00240186054,0.0006984078949,0.00003901690301,0.009604925734,0.0003595363266,0.0008726480398,0.0003252893106,0.0002950445,0.00001345844442,0.0032957558,0.0002723032951,0.00118001423,0.0002091505404,0.0003028473608,0.0002024260366,0.0003444864628,0.006440997344,0.000102107158,0.001283977177,0.0001017136169,0.003807085081,0.004706821522,0.001120475574,0.0001727017796,0.00004886514168,0.0008588991576,0.00003091891605,0.02489282248,0.0001011250809,0.6079499491,0.0000127801874,0.00002311809931,0.0006243024214,0.001568665538,0.00004623225508,0.0001825150219,0.03883022188,0.0001830573157,0.00003492376218,0.00008423434788,0.00004384419701,0.0003108402342,0.0001205641684,0.0007384838785,0.00003003570775,0.00003968527885,0.0001855457032,0.001018120111,0.0001325930351,0.01273078401,0.0001897085914,0.0001125424208,0.0002561123713,0.00009702423776,0.152767516,0.002233716621,0.0002783881192,0.0001107357314,0.0000899448402,0.00006662792063,0.0006170776981,0.0001399205569,0.0003973408663,0.00004537890801,0.0006043528501,0.00009500712191,0.00007910023133,0.0000214575247,0.00006008849674,0.00005037363179,0.0001570842942,0.0002146290679,0.0003995243003,0.00003269004883,0.00008658372254]
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
