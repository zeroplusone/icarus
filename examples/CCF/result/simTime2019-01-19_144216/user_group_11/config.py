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
        experiment['cache_placement']['cache_allocation'] = [0.02445908366,0.00001944612375,0.0004256199219,0.00004805286082,0.00002046113841,0.0001647236999,0.00006205197044,0.003259969555,0.0003081812834,0.0001006478853,0.001179253759,0.0002690308908,0.001724793666,0.0001027712224,0.00001811125209,0.0001188204482,0.0001608368507,0.00277376591,0.0002109562331,0.0005923551737,0.00005065458261,0.0001593290278,0.0001992974824,0.00003533001625,0.0677161678,0.00005720138545,0.00003752836117,0.00005348943185,0.0001641653155,0.0003071355141,0.001812937429,0.00003728080669,0.00008654837082,0.001098128067,0.000218200068,0.0006054581058,0.000659574554,0.03820434207,0.00008994493069,0.00008086197729,0.00629203061,0.003966220994,0.00002828503793,0.00001959689258,0.00003826825367,0.009519802217,0.0009947720228,0.00002136129048,0.001700567691,0.0005213366987,0.00003395475027,0.007517383078,0.00002474684806,0.00007956265335,0.00003135630806,0.004255874439,0.6094637756,0.000101030117,0.00005556914206,0.00009772993834,0.01296946244,0.00004822849079,0.005257969665,0.0003295376106,0.00005879579609,0.0001089944124,0.0001865157203,0.000304433203,0.00009073065316,0.0004915540895,0.00124068587,0.00004081416763,0.002183354307,0.0004915664578,0.0004408762815,0.1539022664,0.0002622228242,0.0004964989492,0.0004081199344,0.00007490595311,0.0006222848248,0.00008393017922,0.0001521468889,0.00002920158129,0.0004316713447,0.0001336779445,0.004406396431,0.00002107810555,0.0009036949688,0.00005331981451,0.0001363021156,0.00001353457273,0.0005231948668,0.002156190825,0.00002277879529,0.0001777650458,0.01709091495,0.0009937701376,0.00009791111818,0.000106968895]
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
