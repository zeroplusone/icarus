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
        experiment['cache_placement']['cache_allocation'] = [0.00008923666682,0.0001228543471,0.0001164039841,0.0004934949689,0.0001005464756,0.00004679189589,0.00002586340065,0.00004482767001,0.00007867852827,0.06765430456,0.0001294868276,0.0003427667467,0.0001356402575,0.0004206514711,0.6083693199,0.000092351109,0.00003991420014,0.00004905914594,0.0003261675617,0.00009838024543,0.000607377893,0.003515759975,0.0005835561691,0.0002629418478,0.0002041773647,0.00008113166278,0.02473041655,0.00002906707506,0.00006538399936,0.0001480269791,0.0003092528229,0.004843499802,0.0000186982502,0.0001473402303,0.00002941999151,0.0003468143968,0.1521508158,0.0006497844247,0.00003022220448,0.01710126317,0.00008572994887,0.001553964597,0.0001005761437,0.00001324814433,0.0001124521903,0.0003333449973,0.00005691863451,0.0002387302911,0.0001796730246,0.0002252353748,0.007061773951,0.0002471642885,0.002000600131,0.0006869053181,0.00003385481445,0.0001550758606,0.0002932061999,0.00005320397781,0.00004210220316,0.0005459169487,0.001541390029,0.00002513392474,0.0003297566499,0.009530518078,0.00008110203248,0.00002802307168,0.007550902194,0.01370776933,0.03818123047,0.001216200013,0.00001945053301,0.002405131615,0.0003120760726,0.0002250152595,0.00001031285218,0.0003192846209,0.0001639193371,0.007091509674,0.00004814225019,0.0001615786895,0.0004465280665,0.000247290675,0.0001858590589,0.0003898871263,0.00106593557,0.0009270706628,0.00003122982716,0.000106622355,0.0001774723986,0.00006929709574,0.002817391819,0.00003297035806,0.003349157179,0.004521430497,0.0008181496341,0.0002792685759,0.0009778653714,0.0001946704426,0.0007213619878,0.001040726935]
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
