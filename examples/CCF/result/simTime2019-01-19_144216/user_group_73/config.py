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
        experiment['cache_placement']['cache_allocation'] = [0.000980437806,0.00004252608244,0.0004594540882,0.00009196194775,0.0005128900377,0.00008916198932,0.00008193033259,0.0001111142235,0.0002669891345,0.002730930533,0.000184939687,0.0007496622606,0.00001661763012,0.004177390188,0.01260562313,0.00003650738321,0.0001882864561,0.0000506390976,0.00003685405555,0.00004841014663,0.00005616793618,0.0001167883983,0.001901299246,0.000176149035,0.0005160738118,0.0001077772316,0.00002741497735,0.0001192933562,0.00006696107612,0.00004750496156,0.001429791534,0.00008015251586,0.007539177789,0.0005147317777,0.0006910103093,0.00003624572587,0.001251260278,0.00004882210594,0.0005566934066,0.00008475453222,0.000500302515,0.001988210925,0.001814017386,0.00008797206174,0.003315809095,0.0002412489035,0.0000282941624,0.00004759544249,0.0007049072435,0.00158234173,0.0008601353968,0.0001664694664,0.000024880084,0.0686253033,0.001576110214,0.00300816766,0.0003788512437,0.000170017653,0.000115399218,0.00003612438931,0.1520598915,0.00004054247356,0.0002333442765,0.0001222591291,0.00004880594213,0.000311121792,0.00005692435551,0.0003851560965,0.0003326076287,0.01402891262,0.0004013644593,0.0000516364706,0.6080242515,0.00009478811045,0.0001896015823,0.0170871167,0.0001121563982,0.000265765673,0.0001018708016,0.0001339378734,0.0001723713231,0.0001306284072,0.00008900741093,0.0002596138875,0.03829979147,0.02434431845,0.000835867484,0.0004599610497,0.005075241296,0.0000349172617,0.001382353425,0.00014234927,0.0000788374201,0.0000967255579,0.0001731685373,0.00005690853284,0.00006605008341,0.001326994655,0.006343421847,0.002446862907]
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
