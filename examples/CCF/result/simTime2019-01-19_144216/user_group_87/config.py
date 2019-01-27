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
        experiment['cache_placement']['cache_allocation'] = [0.00003161332447,0.00008545014848,0.06756238358,0.001124900722,0.001554994255,0.0005022309521,0.0002425435804,0.0001223567376,0.0004470745545,0.0001789908245,0.007530133634,0.0001827731323,0.00006963366202,0.0006575330789,0.00008531291861,0.0005990184639,0.00004192356555,0.00007369535123,0.003230806517,0.00001108490929,0.0002055349842,0.00002777941251,0.0002083706247,0.00002793247742,0.003621122036,0.001484190874,0.00009332252765,0.0001590579656,0.003371585859,0.001942701856,0.00001871731159,0.00006797786555,0.00002307251593,0.006384244473,0.00746979731,0.01243286199,0.0004419531612,0.0001217408853,0.000223345403,0.002313373936,0.00006838023389,0.00001127790383,0.01691970715,0.0002150354644,0.0001401727712,0.009717093136,0.0001193028085,0.001378069635,0.0001446620586,0.00002529335589,0.0001482030151,0.000121011214,0.00002734854779,0.00008228575932,0.0002572557032,0.0007529808271,0.00003865156763,0.00006458433385,0.0005758934199,0.0003559114651,0.00001875974722,0.00007470950298,0.0002981996754,0.0003674441483,0.00005747381467,0.00007069128422,0.00009955588516,0.0004084682106,0.002434537114,0.1520170176,0.000152286886,0.00009465465174,0.00007391043818,0.0001332666857,0.0000549511411,0.00008025431814,0.0007619697866,0.0004821834925,0.00002139336591,0.00005020608543,0.6083517216,0.00009589681649,0.003316546578,0.0004811337164,0.0007712774129,0.02480887571,0.0003001892415,0.00007883308204,0.00006971182431,0.00001894539215,0.03809786361,0.00001319270214,0.0006150727701,0.001399315211,0.002199885993,0.004699962916,0.0002415284214,0.0003725291876,0.0001045884207,0.00007473781874]
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
