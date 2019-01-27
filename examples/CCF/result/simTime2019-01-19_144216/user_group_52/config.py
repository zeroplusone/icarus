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
        experiment['cache_placement']['cache_allocation'] = [0.003390765948,0.002240260215,0.00007723978033,0.0001479825464,0.0002428485539,0.00008138735832,0.00003275503906,0.00002792421384,0.00002049974274,0.0007870757356,0.0009377676997,0.0001484517968,0.0001494250507,0.0002706886883,0.001195871443,0.00008301578601,0.003658141732,0.156345147,0.000657423266,0.00007995021487,0.002672049866,0.0001236914728,0.00007712115047,0.00008027633754,0.0002207336658,0.0004593579502,0.0008013729822,0.0004604623898,0.00009787262196,0.00008928555003,0.0004129517665,0.0001681416148,0.003291193284,0.00001494639309,0.00004035257603,0.0001228485173,0.00002726301048,0.001355350416,0.002019124745,0.0007033658125,0.001420869419,0.00007562407931,0.02521444853,0.0000664288566,0.03866622519,0.00008913778373,0.0006132753157,0.01252675725,0.0001268276474,0.0000616816618,0.001002377694,0.00006562089312,0.0003197216284,0.0005646628667,0.0001000902038,0.001646115091,0.0000333668095,0.009624226822,0.00004792372022,0.01717815303,0.0001280291272,0.06763425269,0.6079530675,0.0008190053948,0.005045569195,0.003230834458,0.0001063730357,0.00007016740219,0.000109443717,0.0002786038638,0.0002168081936,0.0003613244065,0.0002004997293,0.0001743869405,0.00007278820905,0.001377077035,0.00005620357235,0.0003151942292,0.00003280824829,0.007573541234,0.00007222455252,0.0001690481518,0.0001621272229,0.006618079125,0.00005961657897,0.00006546074864,0.0005474398853,0.00004093823517,0.0001416889848,0.00005442528318,0.000217529869,0.000253603925,0.00007676699648,0.0009248650015,0.00004253596062,0.0004587144296,0.0001405517578,0.00005507853646,0.0007919710816,0.00009543708045]
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
