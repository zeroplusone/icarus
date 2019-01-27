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
        experiment['cache_placement']['cache_allocation'] = [0.00003361279581,0.003354700966,0.00003373477952,0.0002162529054,0.00008091892171,0.000131053321,0.0001030527712,0.0003590315595,0.0001093552417,0.0003423028544,0.000133652854,0.0002455126466,0.0006988036045,0.0001194236371,0.002002178094,0.0004801996898,0.001449991868,0.0001751813982,0.001120521547,0.0002740972217,0.00001655573453,0.0002436293865,0.00005884455618,0.006945157668,0.002960745502,0.0002864279678,0.001222686659,0.0001336320381,0.0003298132115,0.0001553623878,0.0006374075119,0.0001053632111,0.00005476837377,0.02509470724,0.0000813927485,0.00001644615655,0.00003636372685,0.001577667519,0.0001378826277,0.0001350544741,0.00009592309345,0.03806802879,0.00520761084,0.0003099872195,0.0001370298762,0.00006073254262,0.000116835641,0.00006329043237,0.00003121280181,0.00009524352414,0.0000538098659,0.0004056927468,0.0004852398691,0.6081268965,0.00004989483427,0.00007985723841,0.0003932136093,0.00001259390578,0.0002250011458,0.0006623039577,0.00007985644435,0.0003607842628,0.00008260572848,0.0002629950558,0.0004218483966,0.001716246411,0.00008386009524,0.00006646289869,0.00006400148997,0.004293656431,0.00006024602904,0.0002456589694,0.0009432072308,0.00001836288302,0.0001465438326,0.001234711047,0.0002935139028,0.004281842964,0.06782229035,0.00330046818,0.0003770738569,0.0000209487054,0.008501802421,0.00007828131347,0.003199326525,0.0000247417986,0.0001022787858,0.01243264002,0.0000175453127,0.009564133182,0.01747023996,0.0006053650227,0.002415371802,0.00002338527016,0.0001532712811,0.000221876649,0.00005370723056,0.1522291344,0.0003363713394,0.00001945671511]
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
