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
        experiment['cache_placement']['cache_allocation'] = [0.009889674212,0.00006481304584,0.0006911024604,0.0002470946972,0.001286392412,0.0172480442,0.001181892942,0.00003569429587,0.0009097280884,0.00002520066435,0.0002464967074,0.002765649899,0.0006315962834,0.001518326425,0.00004866872632,0.0000959836804,0.0004394946892,0.0007056996639,0.00001482662733,0.00003115813456,0.00006121422613,0.00007531322407,0.0002012560646,0.0001970841559,0.0001275125744,0.00006911193779,0.0001206170982,0.0002543949818,0.001685452539,0.00004123718817,0.00003730990817,0.0001056886213,0.0002412865865,0.00006724445047,0.0001320022986,0.0001296784478,0.002317068242,0.00001721970028,0.0004164857758,0.0003323192297,0.0001188395685,0.06757968575,0.0007049364068,0.000613976578,0.0003116388636,0.0003724215651,0.00008817598422,0.00003712636901,0.00000734127933,0.0002261382366,0.0004865017254,0.00008720857324,0.0179510387,0.001966681843,0.00004974973653,0.00007873292752,0.0006160199465,0.003629361417,0.0001324723681,0.00001076115586,0.006155903526,0.0004418883788,0.0003120097752,0.000118380997,0.001268489732,0.002270220231,0.02444359146,0.0001016918857,0.000039959186,0.0001291744649,0.0000458695157,0.00004170285205,0.00006512709477,0.0002285859981,0.0009969862098,0.0003144281486,0.00001489911085,0.00006372620853,0.0001514477935,0.0004249586443,0.0002135828321,0.0001765932203,0.0001442046212,0.03840191852,0.00005835772731,0.00004711020094,0.001442499895,0.0001110581506,0.6080108808,0.0005604010032,0.0005123521235,0.00007144867231,0.0003618858647,0.007505483264,0.00009805191081,0.0002227353937,0.00003881199158,0.0082847843,0.1562864712,0.00004648298934]
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
