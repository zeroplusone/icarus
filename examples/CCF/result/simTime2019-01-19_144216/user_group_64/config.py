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
        experiment['cache_placement']['cache_allocation'] = [0.001793565921,0.00007171748961,0.00005892796141,0.0007002256527,0.00004754657651,0.00009631970601,0.0001129809848,0.000070122135,0.0001916481496,0.001191577713,0.00002465519125,0.00240381529,0.000303272111,0.003633318281,0.0002207981159,0.00005374439795,0.00001725421851,0.01281378354,0.0007602568749,0.0001148737338,0.006246796765,0.000114859149,0.6079701255,0.002729079757,0.00002879768981,0.0001054566645,0.0243409283,0.001567725232,0.0000258974775,0.00001832814571,0.001829269664,0.00009186072834,0.0003146253556,0.0002555108619,0.0002083736539,0.00008550131881,0.0000293925675,0.00001575017259,0.00008384607188,0.0002038168578,0.00001085577894,0.0005765222236,0.0008327564401,0.0004431034163,0.03807042035,0.00002812875986,0.00004190178499,0.0001659648969,0.007710078491,0.0001210439756,0.00006742019038,0.009546825519,0.0004092118819,0.000129675398,0.06780042537,0.005114986243,0.00002947199738,0.0005097993057,0.006613600494,0.0001375277441,0.0001141624402,0.00004595295354,0.001119913625,0.0005150045837,0.0001707103461,0.0002392333958,0.002401880983,0.0002007658917,0.0002016912362,0.0004462540217,0.0001075415744,0.0001348928194,0.0003200433527,0.0001610665666,0.0002073767885,0.0002633288688,0.001548351192,0.00001297566501,0.004254779732,0.002243440567,0.01692882657,0.00194721053,0.0001193802656,0.0002262663585,0.0008047280234,0.00001862530858,0.0003676953983,0.000206776333,0.0001396560261,0.00004233294174,0.00006131108225,0.1520812555,0.00004714684788,0.0009835384147,0.0001765952136,0.0008649328733,0.000101054584,0.0002026459337,0.0006190080453,0.00004558092789]
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
