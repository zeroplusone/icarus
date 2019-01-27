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
        experiment['cache_placement']['cache_allocation'] = [0.01245184116,0.006227379812,0.00009885012814,0.001293860806,0.0001884190475,0.00002218656975,0.002543835783,0.0008435766167,0.001054785076,0.00005384511328,0.0000684112377,0.002541240218,0.0001747843608,0.00006738761888,0.0003354256683,0.00008112590374,0.0006284262324,0.0001023428049,0.005044795829,0.00005968579651,0.00003166337106,0.0003535255374,0.0006886796669,0.00002006278607,0.003678900145,0.003177129813,0.001174602213,0.0002037678949,0.02436240187,0.00007008837378,0.152141216,0.01697133894,0.007555248169,0.00008939472793,0.0006831506143,0.0001644694543,0.001925356692,0.0008970651656,0.0006547935657,0.0003623746886,0.03822866546,0.00008934203568,0.00003571729869,0.009955215276,0.0002279238594,0.00003745971784,0.0001100245867,0.0001439425591,0.000009485145538,0.00002789510375,0.0002689754017,0.00003440631281,0.00006845094511,0.0002725415091,0.001470328239,0.00003236704551,0.00015851197,0.001007473156,0.0002637126429,0.004341836116,0.00003781070777,0.0001276432042,0.0001313152578,0.00006918149676,0.00004901553577,0.00006513160573,0.0001225810066,0.0003188592757,0.0003473249241,0.002868139715,0.00007047672791,0.00002374324199,0.0007910349661,0.0002116304293,0.00004702337069,0.0002060353166,0.00006243143953,0.00007046596004,0.00004226141553,0.0007325342681,0.00006576831045,0.0001335884732,0.0002708090425,0.0682298775,0.0001051078107,0.0001250133706,0.00004849802876,0.0008794492899,0.0003124438383,0.0003957506432,0.002920117623,0.00002367205531,0.001073606694,0.00137058883,0.002088683198,0.00023198807,0.00002300631769,0.6079910978,0.0001103251224,0.001334258259]
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
