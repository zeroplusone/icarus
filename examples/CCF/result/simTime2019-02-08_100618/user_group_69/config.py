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
        experiment['cache_placement']['cache_allocation'] = [0.00956954,0.00980133,0.00993755,0.010187,0.00982219,0.0101751,0.0103608,0.00991664,0.010623,0.0100882,0.010381,0.00988549,0.0105348,0.0111496,0.00902525,0.00935572,0.00975198,0.00974014,0.00897683,0.0099417,0.00979189,0.0109491,0.0103474,0.00959002,0.00959337,0.00951568,0.0104264,0.00946779,0.0090722,0.0103983,0.0107712,0.0103802,0.00987497,0.0114009,0.00947894,0.00806159,0.00977264,0.0100797,0.00998046,0.0099689,0.0104182,0.00978722,0.00920314,0.01079,0.0103149,0.0101338,0.0089903,0.00941311,0.0108734,0.00973782,0.00924453,0.0103342,0.00937208,0.00905244,0.0103081,0.00980662,0.0104491,0.00896422,0.0107599,0.0106016,0.0102034,0.0105646,0.0109163,0.0104032,0.0109898,0.0102414,0.00978076,0.00921519,0.00987303,0.00925221,0.00942963,0.0097679,0.0102094,0.00951072,0.00916775,0.0100815,0.0110401,0.0104214,0.0109772,0.0111485,0.00977035,0.0108245,0.0100233,0.0087799,0.011016,0.00926363,0.00904335,0.0102826,0.00915834,0.0095867,0.0103924,0.0110691,0.00953715,0.00978457,0.0114551,0.0103138,0.00876867,0.0102001,0.0112489,0.00958745]
experiment['cache_placement']['network_cache'] = 0.1

# Set content placement
if READ_FROM_DATA:
        experiment['content_placement']['name'] = 'DATA_TO_CCF'
else:
        if IS_ZIPF:
                experiment['content_placement']['name'] = 'WEIGHTED'
                experiment['content_placement']['source_weights'] =  {101:0.00717587640843523,102:0.011606998319114535,103:0.006016087462422068,104:0.005914283444656411,105:0.006478692947974536,106:0.01701983388614452,107:0.009232771907510715,108:0.010446519914504274,109:0.012372127879358277,110:0.006617389493274116,111:0.013909778865896052,112:0.012293117744125294,113:0.012236466292915643,114:0.012183361995828337,115:0.015368505108308447,116:0.013123931832263479,117:0.010799471293531582,118:0.013102330782238715,119:0.01939242896055647,120:0.008196294857377372,121:0.00471790075319751,122:0.010875036541833309,123:0.010821059995701607,124:0.00837354072923041,125:0.007295098719931155,126:0.006946804843867024,127:0.011753909219172177,128:0.009604436355013266,129:0.007836806421310627,130:0.01097465988128199,131:0.00964887117185679,132:0.011504482358054718,133:0.0053943876535283335,134:0.008443812810819322,135:0.016909371400624356,136:0.010732076877030473,137:0.011717053229578344,138:0.005745317762057413,139:0.014892072467120075,140:0.010792009389835424,141:0.013205419236338799,142:0.012397802550097455,143:0.007625291581446855,144:0.0050816948253824806,145:0.0067734506207572966,146:0.008462165175090275,147:0.009948317059303267,148:0.010741227071503523,149:0.007946667280533799,150:0.011102180621955603,151:0.005938775438089878,152:0.009608452451930346,153:0.009168847873578892,154:0.009311223614989326,155:0.012295813086927884,156:0.007481589727598484,157:0.010286728469988835,158:0.011162487848685008,159:0.013676754515803588,160:0.010087127421981392,161:0.007132288441510841,162:0.011400923071018925,163:0.010120219076405227,164:0.006533076637398351,165:0.007925263632998513,166:0.008923583843611022,167:0.010702836223288955,168:0.007233139106118823,169:0.016158934557966978,170:0.009580761186267864,171:0.010397146483849252,172:0.0070843102475432644,173:0.012476885274924455,174:0.007284960512230228,175:0.016541249446571045,176:0.0089473810424915,177:0.006894718212777233,178:0.009472585767944644,179:0.006426516096867527,180:0.011303822206294285,181:0.007671169926090509,182:0.008678942449546423,183:0.00843142227343899,184:0.007221212944115158,185:0.01018516451130295,186:0.0021447420890588946,187:0.005376540170627375,188:0.01799135205209311,189:0.011631528467686938,190:0.010405364835610043,191:0.013345225581596324,192:0.0111092880809252,193:0.012994163274706077,194:0.007320169720799727,195:0.0105770804803995,196:0.007067522481773677,197:0.009685571549072642,198:0.009007607007003522,199:0.012937671147973099,200:0.012910665438637932}
                # experiment['content_placement']['name'] = 'UNIFORM'
                # experiment['content_placement']['name'] = 'ZIPF'
                # experiment['content_placement']['alpha'] = 2
                # experiment['content_placement']['is_random'] = True
        else:
                experiment['content_placement']['name'] = 'WEIGHTED'
                experiment['content_placement']['source_weights'] =  {101:0.00717587640843523,102:0.011606998319114535,103:0.006016087462422068,104:0.005914283444656411,105:0.006478692947974536,106:0.01701983388614452,107:0.009232771907510715,108:0.010446519914504274,109:0.012372127879358277,110:0.006617389493274116,111:0.013909778865896052,112:0.012293117744125294,113:0.012236466292915643,114:0.012183361995828337,115:0.015368505108308447,116:0.013123931832263479,117:0.010799471293531582,118:0.013102330782238715,119:0.01939242896055647,120:0.008196294857377372,121:0.00471790075319751,122:0.010875036541833309,123:0.010821059995701607,124:0.00837354072923041,125:0.007295098719931155,126:0.006946804843867024,127:0.011753909219172177,128:0.009604436355013266,129:0.007836806421310627,130:0.01097465988128199,131:0.00964887117185679,132:0.011504482358054718,133:0.0053943876535283335,134:0.008443812810819322,135:0.016909371400624356,136:0.010732076877030473,137:0.011717053229578344,138:0.005745317762057413,139:0.014892072467120075,140:0.010792009389835424,141:0.013205419236338799,142:0.012397802550097455,143:0.007625291581446855,144:0.0050816948253824806,145:0.0067734506207572966,146:0.008462165175090275,147:0.009948317059303267,148:0.010741227071503523,149:0.007946667280533799,150:0.011102180621955603,151:0.005938775438089878,152:0.009608452451930346,153:0.009168847873578892,154:0.009311223614989326,155:0.012295813086927884,156:0.007481589727598484,157:0.010286728469988835,158:0.011162487848685008,159:0.013676754515803588,160:0.010087127421981392,161:0.007132288441510841,162:0.011400923071018925,163:0.010120219076405227,164:0.006533076637398351,165:0.007925263632998513,166:0.008923583843611022,167:0.010702836223288955,168:0.007233139106118823,169:0.016158934557966978,170:0.009580761186267864,171:0.010397146483849252,172:0.0070843102475432644,173:0.012476885274924455,174:0.007284960512230228,175:0.016541249446571045,176:0.0089473810424915,177:0.006894718212777233,178:0.009472585767944644,179:0.006426516096867527,180:0.011303822206294285,181:0.007671169926090509,182:0.008678942449546423,183:0.00843142227343899,184:0.007221212944115158,185:0.01018516451130295,186:0.0021447420890588946,187:0.005376540170627375,188:0.01799135205209311,189:0.011631528467686938,190:0.010405364835610043,191:0.013345225581596324,192:0.0111092880809252,193:0.012994163274706077,194:0.007320169720799727,195:0.0105770804803995,196:0.007067522481773677,197:0.009685571549072642,198:0.009007607007003522,199:0.012937671147973099,200:0.012910665438637932}
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
