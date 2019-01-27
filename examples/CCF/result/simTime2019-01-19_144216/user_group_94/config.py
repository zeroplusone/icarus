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
        experiment['cache_placement']['cache_allocation'] = [0.002413215029,0.00001780657187,0.00005578223238,0.0002200750791,0.0003221997631,0.000307071612,0.00004786271693,0.0009028800072,0.00008364641282,0.006167002966,0.01698699675,0.0003670982908,0.0005878093455,0.000932901427,0.000609671439,0.0003049466277,0.0004273158644,0.001233029283,0.0001132119921,0.00009651728127,0.0001249669225,0.0001388578603,0.00006877327422,0.00001872865199,0.0001213681767,0.00001232796894,0.0003282840367,0.00225351784,0.000110360316,0.00003974558576,0.00003214007585,0.0007174921489,0.0000105963286,0.0001478959819,0.00008774613325,0.0009830302731,0.0005993657105,0.6756026814,0.00001804357545,0.00002301144479,0.001182197632,0.0004074855824,0.004351248051,0.00003804359733,0.001906697144,0.001589126343,0.00002193541794,0.002200120703,0.1902903805,0.00005207317761,0.007532903616,0.00006016088912,0.00003751269329,0.00002703122068,0.0004205667218,0.0002237074733,0.0008630962185,0.0001370526869,0.00008300602221,0.009596142282,0.001425335361,0.0001364958987,0.0001421007856,0.00003650033054,0.00001945520445,0.0004235445864,0.0001703299052,0.0008905931523,0.00003302064683,0.000860432019,0.00006400489237,0.00364610314,0.0002911132201,0.00004622700871,0.005126527027,0.0005414969638,0.0016700431,0.002915104726,0.0004052172588,0.0001411103301,0.00006750607325,0.0001413172207,0.0001777285815,0.02447447033,0.000111978884,0.0005945498588,0.001037900836,0.0001711785279,0.003565537847,0.00002232217961,0.01381662916,0.00006233293022,0.0003246443533,0.0001300609562,0.0001026572262,0.0001563769145,0.00002255815895,0.00002880654795,0.001162610905,0.0001876145909]
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
