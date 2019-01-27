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
        experiment['cache_placement']['cache_allocation'] = [0.0003810940989,0.00007923370849,0.0007420477568,0.0000987139245,0.002350520831,0.003639163973,0.0009834990763,0.001091663716,0.00004630584512,0.0005634072626,0.00009701564725,0.00009787448748,0.0004722429679,0.0005950795031,0.0001282363576,0.00001565212731,0.00008132023403,0.0001389620463,0.00008342773869,0.0001883788114,0.0001245640207,0.0004680954801,0.0005109011971,0.00003789239985,0.0003000927774,0.0002417515991,0.0004944825211,0.00002329191953,0.0001601685012,0.00005357152627,0.0001097162268,0.0000597969181,0.0004718204931,0.06759812753,0.00007193513649,0.0002673844182,0.0000514116003,0.00007679063533,0.00005145758861,0.00003179552529,0.000191039238,0.0001431061085,0.00005797671807,0.01732335223,0.0001242901066,0.0002072966783,0.0003291247421,0.0003011255999,0.0003433572552,0.00007546075946,0.000185013081,0.01375637417,0.0001331091822,0.0004408862159,0.001189754753,0.002759431937,0.0001492651952,0.00003442599798,0.0002113732381,0.0001286922222,0.0004586982775,0.00003262874491,0.00022253836,0.01252612729,0.00002838037522,0.002237862449,0.0005623975793,0.003293836914,0.000136933484,0.0003895541174,0.0002368496398,0.005270864465,0.00002762821053,0.0009271514861,0.000349375759,0.00003650346491,0.009673799546,0.0244726326,0.00005172912673,0.0003626689808,0.00004239387146,0.00009109656872,0.001990849364,0.00004022558926,0.00148780565,0.00006807995967,0.03801745856,0.005059425198,0.0007479331593,0.0001474175357,0.0008033860157,0.002096747397,0.6080960926,0.0001947185194,0.002856807839,0.0013817986,0.1520964207,0.001807518268,0.00009277994276,0.0004195402079]
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
