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
                experiment['content_placement']['source_weights'] =  {101:0.0,102:0.008447358,103:0.0,104:0.045841642,105:0.0,106:0.003184044,107:0.005348435,108:0.000125058,109:0.0,110:0.0,111:0.00932838,112:1.31e-06,113:0.013677369,114:0.0,115:0.027044316,116:0.000251929,117:0.000136219,118:0.0,119:0.003480786,120:0.0,121:0.000198287,122:0.000162088,123:0.043950934,124:3.01e-05,125:0.028252685,126:0.000209236,127:0.018806955,128:0.000104135,129:4.05e-07,130:0.0,131:1.72e-05,132:0.044409564,133:0.03360116,134:0.0,135:4.66e-05,136:0.000616771,137:0.022341551,138:0.045539166,139:0.045175658,140:0.004422285,141:0.0,142:0.010298357,143:0.0,144:0.013512564,145:5.2e-05,146:0.0,147:0.0,148:0.045743145,149:0.0,150:0.0,151:0.004702509,152:0.006804929,153:0.048311543,154:0.001099096,155:0.0,156:0.024609703,157:0.032745939,158:0.001234509,159:0.042346618,160:6.2e-05,161:0.004302548,162:0.034066053,163:0.0,164:0.015607344,165:0.000393632,166:0.036929771,167:0.0,168:8.18e-05,169:0.0,170:0.045889043,171:0.000536801,172:0.021584461,173:0.018997484,174:0.0,175:7.62e-06,176:0.0,177:0.0,178:0.037542617,179:0.047348383,180:7.19e-05,181:0.000993538,182:0.0,183:1.7e-06,184:0.000495404,185:0.001552573,186:0.002281218,187:0.0,188:0.024908951,189:0.00196944,190:0.006807983,191:0.0,192:0.000137496,193:0.002218926,194:0.015364121,195:0.000487703,196:0.0,197:1.75e-08,198:0.0,199:0.009670924,200:0.033476004}
                # experiment['content_placement']['name'] = 'UNIFORM'
                # experiment['content_placement']['name'] = 'ZIPF'
                # experiment['content_placement']['alpha'] = 2
                # experiment['content_placement']['is_random'] = True
        else:
                experiment['content_placement']['name'] = 'WEIGHTED'
                experiment['content_placement']['source_weights'] =  {101:0.0,102:0.008447358,103:0.0,104:0.045841642,105:0.0,106:0.003184044,107:0.005348435,108:0.000125058,109:0.0,110:0.0,111:0.00932838,112:1.31e-06,113:0.013677369,114:0.0,115:0.027044316,116:0.000251929,117:0.000136219,118:0.0,119:0.003480786,120:0.0,121:0.000198287,122:0.000162088,123:0.043950934,124:3.01e-05,125:0.028252685,126:0.000209236,127:0.018806955,128:0.000104135,129:4.05e-07,130:0.0,131:1.72e-05,132:0.044409564,133:0.03360116,134:0.0,135:4.66e-05,136:0.000616771,137:0.022341551,138:0.045539166,139:0.045175658,140:0.004422285,141:0.0,142:0.010298357,143:0.0,144:0.013512564,145:5.2e-05,146:0.0,147:0.0,148:0.045743145,149:0.0,150:0.0,151:0.004702509,152:0.006804929,153:0.048311543,154:0.001099096,155:0.0,156:0.024609703,157:0.032745939,158:0.001234509,159:0.042346618,160:6.2e-05,161:0.004302548,162:0.034066053,163:0.0,164:0.015607344,165:0.000393632,166:0.036929771,167:0.0,168:8.18e-05,169:0.0,170:0.045889043,171:0.000536801,172:0.021584461,173:0.018997484,174:0.0,175:7.62e-06,176:0.0,177:0.0,178:0.037542617,179:0.047348383,180:7.19e-05,181:0.000993538,182:0.0,183:1.7e-06,184:0.000495404,185:0.001552573,186:0.002281218,187:0.0,188:0.024908951,189:0.00196944,190:0.006807983,191:0.0,192:0.000137496,193:0.002218926,194:0.015364121,195:0.000487703,196:0.0,197:1.75e-08,198:0.0,199:0.009670924,200:0.033476004}
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
