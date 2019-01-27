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
        experiment['cache_placement']['cache_allocation'] = [0.00009559222668,0.0007307757227,0.005313036171,0.002120756774,0.007562627512,0.003836040818,0.00008900902347,0.0001378680156,0.00006177645065,0.0007441123314,0.00003315306733,0.00007260872846,0.0002408807979,0.6079905203,0.001661854712,0.0003122590123,0.00001022114408,0.0003314617363,0.009604530691,0.0001454767493,0.0001174873071,0.001056800041,0.0001801688109,0.0000564150644,0.00236393925,0.02436025525,0.0006615564738,0.0002732421449,0.00009819466664,0.0001760023981,0.00005325085583,0.00006874287422,0.0004410277431,0.001069488387,0.004388515948,0.1520581464,0.003275750265,0.0001601796506,0.00001160756467,0.0001042958988,0.0005209574459,0.03812504632,0.00006340500264,0.0001928721196,0.00002607663155,0.001405467458,0.00003186899673,0.00008145861478,0.001067807685,0.00002629173601,0.00001293675062,0.0001408932481,0.0004881679469,0.000797308642,0.01245410828,0.00127463356,0.0001142221809,0.0004000388443,0.006174751246,0.0009352147202,0.00004825492742,0.00001798644694,0.000716373689,0.0005224669489,0.01691015953,0.00004530468778,0.00006978544,0.00002972727581,0.00003459758229,0.000110674121,0.0004394876094,0.000136390974,0.0004378017789,0.0001178203404,0.0004647181137,0.00003212820921,0.06761666204,0.0003747693372,0.0004792467048,0.001777661001,0.00003970966713,0.0002324204449,0.00004825705384,0.0001307570199,0.002823567093,0.0001751282522,0.00005566344686,0.003801195408,0.0001396466225,0.0000319287745,0.0002249977591,0.0008089396406,0.0001518756067,0.00005219242493,0.00227808481,0.00006369220114,0.001256490489,0.0001683388075,0.0001121038835,0.0006198374458]
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
