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
        experiment['cache_placement']['cache_allocation'] = [0.001342491771,0.00004075805339,0.0001677233226,0.0003355627934,0.001043240328,0.00009143955708,0.0002369129918,0.0003328332221,0.00004006785657,0.0000633821709,0.0001728019936,0.00005844144031,0.00005232493837,0.00008080796555,0.00006006494252,0.00002927278977,0.0001175810815,0.00006017882825,0.0004088945507,0.00003261434545,0.00003112502962,0.0001145509006,0.0001773276651,0.002675417531,0.006821682998,0.007587012854,0.1055790651,0.0001256752098,0.01251189242,0.00008547391643,0.0009986668307,0.0009405667229,0.6081251673,0.003729580205,0.0001881240711,0.00003526725031,0.00005175937988,0.00004518140506,0.0002343717556,0.000956036255,0.00004013843724,0.00001939765783,0.0003286051129,0.006117765702,0.0001866579123,0.00002978610159,0.00009886909942,0.00008846254909,0.0001271614795,0.00005804664086,0.005870572663,0.000102265982,0.00003442323338,0.0001743018314,0.0001460515633,0.00002117331751,0.0000538978429,0.001524413324,0.00006913326131,0.0007020895001,0.002199840755,0.0001101397405,0.0003838228053,0.00006029565672,0.0006167453781,0.0007231632665,0.001597162146,0.0002672517504,0.0000503168742,0.1524595426,0.01702533679,0.009608856361,0.003131916981,0.0001062587591,0.001174962993,0.0000533830508,0.005068756528,0.00004183511306,0.0003859551417,0.0004790812712,0.0001670618149,0.0003261658251,0.000522028644,0.00014906999,0.001533341121,0.00007605208979,0.00005035016915,0.001081391127,0.0001913256572,0.00002157869601,0.0004241439207,0.000583936307,0.00008754250543,0.0004980509336,0.0001188463848,0.0002012990836,0.00002474564131,0.0000548088635,0.002273521991,0.02449556228]
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
