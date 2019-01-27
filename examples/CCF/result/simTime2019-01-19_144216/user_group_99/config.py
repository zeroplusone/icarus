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
        experiment['cache_placement']['cache_allocation'] = [0.0006487139107,0.0001530586138,0.000220872871,0.00006449894026,0.0002570729689,0.0001770157931,0.0001262153206,0.0009669887039,0.00004125961106,0.00004343830711,0.0008615403124,0.0007621974357,0.00007727225986,0.0001434750902,0.0006865042421,0.000008206527379,0.00003973730301,0.00003551826402,0.03805398912,0.001031625418,0.002306797883,0.0009000813619,0.00006413502433,0.009607018628,0.001243508166,0.00148507335,0.0003584866518,0.001178064583,0.00005155963724,0.00001624021865,0.00006978623074,0.00521671238,0.00004889287166,0.00003823577761,0.00006035136065,0.001117346046,0.00001572335541,0.00002085331463,0.003214996859,0.0002082836018,0.004253085196,0.0000942094914,0.152123622,0.003671141335,0.0002203104894,0.0001331934452,0.00007026287216,0.6080433135,0.001649395801,0.0004016823522,0.0003943933237,0.001067182283,0.00009347970242,0.0001296082295,0.0002529200166,0.02447330514,0.0001260703404,0.00002155978835,0.00005996335677,0.0006141483077,0.0008978789924,0.0007322269206,0.002906580076,0.0001013060079,0.0004401675563,0.00005211342729,0.0002037585702,0.00002366938503,0.0004861785356,0.002190890028,0.0002398389954,0.0001548555798,0.00002420251291,0.0009769245085,0.006273834342,0.00003610957652,0.00008525855719,0.003152671934,0.00005845523581,0.06772522813,0.0002806099808,0.0005192778124,0.0005656649552,0.0004704419216,0.00004687537235,0.0001900050539,0.00006957554821,0.0000797279147,0.009357188261,0.00003472213332,0.0003263180472,0.001351927283,0.00003536765648,0.00003503101309,0.00002113773275,0.0001164635846,0.0001241344341,0.01717540756,0.01248015629,0.0004436232301]
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
