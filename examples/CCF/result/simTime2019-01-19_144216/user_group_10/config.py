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
        experiment['cache_placement']['cache_allocation'] = [0.0002149708916,0.02464292277,0.0002431494444,0.0001076379193,0.0004814471172,0.0003091457288,0.001051288995,0.0004596543405,0.00004371727793,0.001289426612,0.00004988829826,0.001804041561,0.0001116059431,0.00007503313205,0.0005944217693,0.00002608493115,0.06826513339,0.005578429866,0.004029206389,0.00009109630566,0.00006896789235,0.00005456330313,0.6079918908,0.0005156718532,0.00003491312107,0.00002857485502,0.00006853695823,0.00008785425611,0.00007219956784,0.0003815696514,0.004309738776,0.004589460033,0.000125955587,0.006212353408,0.0002374649123,0.00003322501481,0.00002115874913,0.007753793898,0.000114485135,0.1520638596,0.00004691800672,0.00001207433012,0.0001714156458,0.0002647268925,0.004113684938,0.00009153344684,0.001556404757,0.0003610889538,0.0002169906704,0.00003174248191,0.00002961897181,0.0001562589553,0.00007170226206,0.0001894156231,0.0001168503785,0.00004389471045,0.0002618354348,0.00006142060549,0.000353236268,0.01335061675,0.0001109449491,0.0005700196169,0.0008762622582,0.001582714298,0.0007729886065,0.00003541572897,0.00005502990871,0.0001125095627,0.000109933591,0.0001831986515,0.00002502843051,0.00003597798121,0.00006421497018,0.002569759247,0.03822723056,0.00002979941808,0.00006006715953,0.003657336178,0.00005949504584,0.00009718625331,0.0007007464857,0.0000911581037,0.00005183650009,0.0001455002841,0.0004969459817,0.00003778158881,0.01716168637,0.0002954512644,0.00006645145959,0.0002438456682,0.001499806323,0.00129736166,0.0007118064806,0.00002038214087,0.0004667264853,0.0003368762604,0.009929550921,0.001190490483,0.0001303324584,0.0001541805249]
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
