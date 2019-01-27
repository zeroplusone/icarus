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
        experiment['cache_placement']['cache_allocation'] = [0.003120475555,0.0001219874161,0.00002386457105,0.0007708563323,0.6081842132,0.0002331150962,0.06759294127,0.0001204402181,0.0006222327964,0.0006028120239,0.001184523836,0.0004757566027,0.0001725301875,0.0006249159072,0.002823734022,0.000237501416,0.000452117898,0.00007772490939,0.001028064848,0.0002384848592,0.00001812766729,0.002944906551,0.02443292415,0.00004870854634,0.00005911975869,0.0002729265092,0.0003536087145,0.004243899764,0.00007900525453,0.0004640416347,0.00007950186392,0.00002728239417,0.005790629005,0.00008401535549,0.00008819032291,0.0000535834737,0.03840528926,0.002439791541,0.00065776087,0.01729841032,0.0002663442224,0.01338673831,0.00002907211215,0.0001125411827,0.009693030113,0.0001063554386,0.006635418722,0.0001411606018,0.001650859811,0.0001092743015,0.0001279423694,0.00005890398577,0.0005928396192,0.0000569342405,0.0003040900845,0.00004889126998,0.0001170548371,0.000541607747,0.00004791632752,0.00006206296478,0.0001073983336,0.00006241790808,0.1523615619,0.00004772796504,0.0002100896158,0.0001083249671,0.0000509217576,0.0004748699613,0.0002128409726,0.00005893840725,0.00022076093,0.00213545136,0.006123686034,0.0001440358736,0.0003633021923,0.00002011674777,0.0002344766155,0.0003845587886,0.0001999169515,0.00006072735836,0.00001797059096,0.00003437181815,0.00007835591343,0.0001813793394,0.0001401052609,0.003283463816,0.0003855473212,0.0004328280861,0.00004505534733,0.00007605211747,0.00002331343224,0.0003828008485,0.0006588363055,0.000161015074,0.0006017882585,0.00003818829382,0.001541958872,0.00002512073915,0.00004409819495,0.007626571605]
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
