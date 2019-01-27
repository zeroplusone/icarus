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
        experiment['cache_placement']['cache_allocation'] = [0.0001505010514,0.002538926432,0.0002039670371,0.0001682185083,0.0003158857051,0.00008313386187,0.0001362792556,0.00002943208657,0.001259948127,0.00008480469167,0.00002658807636,0.00001250877722,0.00004615457408,0.0008760297438,0.0004691843957,0.00129759647,0.0001438173659,0.01259205285,0.00001693919586,0.0009699669201,0.0000675878151,0.000176156648,0.0001146021749,0.000915018007,0.00009272351883,0.0005453389618,0.0001270138471,0.00004627188431,0.0003204131632,0.000219084467,0.00006463847035,0.00006709974936,0.1541080904,0.005098606404,0.0001150531126,0.007682771823,0.006184910943,0.001919136442,0.003993962566,0.00004119118134,0.03903045349,0.001159347595,0.000544408107,0.0000334282075,0.00094119455,0.0002938884791,0.0002698955353,0.0006634898055,0.001549694681,0.0003013399701,0.0001187773807,0.0006057542301,0.0004991525979,0.00008614788029,0.0003356838616,0.000174940046,0.0003383019319,0.00007619982205,0.02472515245,0.00003242206596,0.000838697667,0.00007125796041,0.01135932401,0.00001951407158,0.00006557891241,0.0002025377858,0.0003468257096,0.0002093544666,0.0001743866813,0.00005712226376,0.00003325702526,0.01697004279,0.0001363745045,0.6079588529,0.0002821759809,0.009514706678,0.00006006170191,0.00004596419095,0.00006991308029,0.00001970055921,0.000132848315,0.002015123355,0.0002031531398,0.0002423194312,0.0004004842991,0.0001032958101,0.002261279116,0.0002214654403,0.06757221873,0.00008215619141,0.0002257357606,0.0003543207895,0.0001510829537,0.00001895194159,0.0005373330095,0.00007453696013,0.001594551773,0.00007144155191,0.00003862242842,0.0001621506425]
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
