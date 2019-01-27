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
        experiment['cache_placement']['cache_allocation'] = [0.00005083162342,0.001423434941,0.00005804200059,0.6079674841,0.0002502970671,0.0000793213825,0.00002027850228,0.0001679270069,0.00002644930776,0.00006570490085,0.0002604252194,0.00003403010595,0.0003300767451,0.00004907262784,0.0002991782069,0.00026457799,0.00008511069094,0.0001924668226,0.00011132727,0.00006003195681,0.008568958856,0.00390459358,0.0008369442567,0.00002265195159,0.00003413394931,0.0001919937615,0.00005157461758,0.00004708536482,0.0002776601733,0.0004433513492,0.0001959942856,0.0008625123908,0.00003217908599,0.00005915824243,0.001904461128,0.0008389952259,0.004245483277,0.0002417201307,0.00235386969,0.017168816,0.00003815843504,0.001534105421,0.000389876016,0.00002851429283,0.00004763451357,0.00006445494125,0.00005872527113,0.00004348115604,0.00006801652772,0.00004468421597,0.00005101305237,0.001619225696,0.0001939021853,0.009726912819,0.0001355509811,0.00007851830501,0.0006338821531,0.0001141705599,0.00006514327894,0.0007318742566,0.0002863844864,0.0001324950207,0.002453520013,0.00517530374,0.0008355699309,0.002431033347,0.0007645898843,0.0130004478,0.0009668469005,0.00232266666,0.0005830789899,0.0001220329969,0.003221911572,0.00002073202996,0.00007920981605,0.00003118257997,0.00003108893767,0.03822055742,0.0001356158663,0.00008754030188,0.00006167116889,0.0001523038817,0.0004706653784,0.0002512450126,0.06766002948,0.1521695848,0.00002372277787,0.00002078636189,0.00006041126336,0.001238662812,0.00002477989523,0.0001436156453,0.001700984569,0.0006364315198,0.02441972077,0.00004693885632,0.00001106709687,0.003746727862,0.006116428651,0.0003963640962]
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
