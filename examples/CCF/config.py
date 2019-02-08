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
IS_BASELINE = True
# If True, read workload and content placement from data 
READ_FROM_DATA = False
IS_ZIPF = True
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
                'alpha':      0.00001,
                'rate':       1,
                'is_random':  True
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
        experiment['cache_placement']['cache_allocation'] = [0.1, 0.3, 0.5, 0.1]
experiment['cache_placement']['network_cache'] = 0.1

# Set content placement
if READ_FROM_DATA:
        experiment['content_placement']['name'] = 'DATA_TO_CCF'
else:
        if IS_ZIPF:
                experiment['content_placement']['name'] = 'WEIGHTED'
                experiment['content_placement']['source_weights'] = {101: 0.007785136677, 102: 0.005283149746, 103: 0.009061968822, 104: 0.007574448096, 105: 0.00725423444, 106: 0.009393646508, 107: 0.00700736773, 108: 0.01243837314, 109: 0.01246692704, 110: 0.008783538223, 111: 0.01275946157, 112: 0.009666397154, 113: 0.01140191967, 114: 0.003759272096, 115: 0.01442036169, 116: 0.01344038014, 117: 0.01159573413, 118: 0.01446527833, 119: 0.004322145284, 120: 0.01097347701, 121: 0.01004006416, 122: 0.008025701606, 123: 0.01272615121, 124: 0.009713088417, 125: 0.01092622981, 126: 0.008260738902, 127: 0.01042551278, 128: 0.01213123997, 129: 0.007348023904, 130: 0.009005312703, 131: 0.01064401864, 132: 0.01414420017, 133: 0.005425245308, 134: 0.009033931834, 135: 0.006145038279, 136: 0.01580703643, 137: 0.006778343122, 138: 0.01020244001, 139: 0.01306157539, 140: 0.01442665532, 141: 0.006787897995, 142: 0.008262193535, 143: 0.009094018497, 144: 0.01100513777, 145: 0.009347095909, 146: 0.008594462195, 147: 0.01048199825, 148: 0.01083881075, 149: 0.008171599929, 150: 0.00978626278, 151: 0.007943543016, 152: 0.009678854437, 153: 0.01156216246, 154: 0.01121877731, 155: 0.005372073955, 156: 0.008256341923, 157: 0.008457713697, 158: 0.01115368648, 159: 0.01397049312, 160: 0.009898031262, 161: 0.007046401255, 162: 0.007892353554, 163: 0.0141771409, 164: 0.008999556744, 165: 0.009650087155, 166: 0.009766191973, 167: 0.006960914188, 168: 0.01269775939, 169: 0.01164652537, 170: 0.005754291872, 171: 0.007994932625, 172: 0.009975776717, 173: 0.01028876742, 174: 0.0140926887, 175: 0.01112302968, 176: 0.0123023708, 177: 0.008706074998, 178: 0.01348827726, 179: 0.008737455614, 180: 0.01087676538, 181: 0.01108501337, 182: 0.01016325548, 183: 0.01095824136, 184: 0.005488905925, 185: 0.009241973264, 186: 0.01098753872, 187: 0.005986082169, 188: 0.007305954283, 189: 0.01446429333, 190: 0.01041947883, 191: 0.01328083758, 192: 0.00910430124, 193: 0.00780550161, 194: 0.008247628431, 195: 0.01065823937, 196: 0.01025900908, 197: 0.01554691216, 198: 0.01251405505, 199: 0.01251060325, 200: 0.01378989316}
                # experiment['content_placement']['name'] = 'UNIFORM'
                # experiment['content_placement']['name'] = 'ZIPF'
                # experiment['content_placement']['alpha'] = 2
                # experiment['content_placement']['is_random'] = True
        else:
                experiment['content_placement']['name'] = 'WEIGHTED'
                experiment['content_placement']['source_weights'] = {101: 0.007785136677, 102: 0.005283149746, 103: 0.009061968822, 104: 0.007574448096, 105: 0.00725423444, 106: 0.009393646508, 107: 0.00700736773, 108: 0.01243837314, 109: 0.01246692704, 110: 0.008783538223, 111: 0.01275946157, 112: 0.009666397154, 113: 0.01140191967, 114: 0.003759272096, 115: 0.01442036169, 116: 0.01344038014, 117: 0.01159573413, 118: 0.01446527833, 119: 0.004322145284, 120: 0.01097347701, 121: 0.01004006416, 122: 0.008025701606, 123: 0.01272615121, 124: 0.009713088417, 125: 0.01092622981, 126: 0.008260738902, 127: 0.01042551278, 128: 0.01213123997, 129: 0.007348023904, 130: 0.009005312703, 131: 0.01064401864, 132: 0.01414420017, 133: 0.005425245308, 134: 0.009033931834, 135: 0.006145038279, 136: 0.01580703643, 137: 0.006778343122, 138: 0.01020244001, 139: 0.01306157539, 140: 0.01442665532, 141: 0.006787897995, 142: 0.008262193535, 143: 0.009094018497, 144: 0.01100513777, 145: 0.009347095909, 146: 0.008594462195, 147: 0.01048199825, 148: 0.01083881075, 149: 0.008171599929,
                                                                     150: 0.00978626278, 151: 0.007943543016, 152: 0.009678854437, 153: 0.01156216246, 154: 0.01121877731, 155: 0.005372073955, 156: 0.008256341923, 157: 0.008457713697, 158: 0.01115368648, 159: 0.01397049312, 160: 0.009898031262, 161: 0.007046401255, 162: 0.007892353554, 163: 0.0141771409, 164: 0.008999556744, 165: 0.009650087155, 166: 0.009766191973, 167: 0.006960914188, 168: 0.01269775939, 169: 0.01164652537, 170: 0.005754291872, 171: 0.007994932625, 172: 0.009975776717, 173: 0.01028876742, 174: 0.0140926887, 175: 0.01112302968, 176: 0.0123023708, 177: 0.008706074998, 178: 0.01348827726, 179: 0.008737455614, 180: 0.01087676538, 181: 0.01108501337, 182: 0.01016325548, 183: 0.01095824136, 184: 0.005488905925, 185: 0.009241973264, 186: 0.01098753872, 187: 0.005986082169, 188: 0.007305954283, 189: 0.01446429333, 190: 0.01041947883, 191: 0.01328083758, 192: 0.00910430124, 193: 0.00780550161, 194: 0.008247628431, 195: 0.01065823937, 196: 0.01025900908, 197: 0.01554691216, 198: 0.01251405505, 199: 0.01251060325, 200: 0.01378989316}
                # experiment['content_placement']['name'] = 'NORMAL'
                # experiment['content_placement']['is_random'] = True

# Set cache replacement policy
experiment['cache_policy']['name'] = 'LRU'

# Set caching meta-policy
experiment['strategy']['name'] = 'LCE'

# Description of the experiment

experiment['desc'] = "Line topology with customized cache"

# Append experiment to queue
EXPERIMENT_QUEUE.append(experiment)
