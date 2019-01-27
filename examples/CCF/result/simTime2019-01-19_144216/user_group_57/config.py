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
        experiment['cache_placement']['cache_allocation'] = [0.00004217299477,0.00001658510052,0.0001004764845,0.03177886686,0.0001065557152,0.0001183533774,0.0001492014642,0.002170760979,0.1521972438,0.00001722697085,0.0002103270522,0.0001418302511,0.0008041889779,0.0001801088469,0.0005287316324,0.0007700835032,0.0002987404885,0.0003663610534,0.6081844819,0.000440185955,0.00006457549563,0.00003844237689,0.0003504463513,0.0006573088468,0.0001499102721,0.005059765164,0.07083559395,0.00008103423393,0.0001593403487,0.00005782926956,0.009575473842,0.001270004901,0.00006324249212,0.001275336852,0.0000586166806,0.0001463300128,0.005547614817,0.01286736754,0.002027216698,0.00008401981107,0.00006862077193,0.0002455954356,0.0004589071663,0.003631051686,0.00006774059101,0.00001728027902,0.00004295420796,0.000423639679,0.00007629912001,0.00005298963366,0.0001644797447,0.0007982043298,0.002258001399,0.0002350335438,0.003366420147,0.0002630131477,0.0000400732043,0.000711466367,0.00009520395868,0.0001036972555,0.0001971460206,0.0001353601029,0.00005446453249,0.00005091838098,0.0004522242372,0.000245961655,0.0002079489649,0.00004776274078,0.0001024965833,0.0001510736101,0.0001800231718,0.000140045522,0.0002025073359,0.00003502377103,0.00002841271015,0.0001649342135,0.0005294532667,0.00005340006957,0.01691652021,0.003206515836,0.00004043653613,0.0002458240035,0.0001930941144,0.00005095670184,0.00012234626,0.0002343088497,0.0000276106985,0.000537315894,0.007624840026,0.0008555749713,0.0001073024653,0.0007059907194,0.0001473220582,0.04188403683,0.00006346239162,0.00005561136129,0.00005531251528,0.0002971891424,0.00147565317,0.00006099339987]
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
