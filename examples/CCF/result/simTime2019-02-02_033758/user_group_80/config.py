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
                'alpha':      0.001,
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
        experiment['cache_placement']['cache_allocation'] = [0.01142849687435521,0.007118444960621031,0.00801701810568377,0.007527778523165233,0.008657326422333472,0.011078105698343983,0.009018995684423235,0.007686700241484026,0.006503228291692657,0.006765810442950122,0.004466265081183447,0.009667705213205983,0.011756914629140731,0.015339706652972896,0.01099772379721283,0.011762730542665486,0.013406487577661788,0.011647960341751104,0.0118274888821313,0.008368749445012638,0.011929576009119893,0.006983923919469124,0.01165044764807367,0.009501215994557988,0.008214028357812465,0.006879150404591585,0.008280490124099895,0.008308210585902975,0.012605201116095335,0.010678671205035725,0.006499446287284153,0.012575086361037283,0.012996581550511678,0.006083807993586188,0.009268380442449509,0.00653957631512672,0.009023258117734436,0.011008985795470397,0.005225489699550998,0.010514770436211915,0.008892291314593978,0.012758927534261234,0.015390201868166933,0.009135768968896374,0.010715575409527061,0.011775571712687003,0.012946861115721528,0.010117717849516665,0.006402222476875331,0.01130134601896301,0.004145381440160864,0.012638243988272608,0.010515608700931073,0.01052772827326625,0.012491966394810731,0.014893093576602606,0.008038831860838033,0.007684703656562692,0.013727275214047882,0.009413847875210093,0.017238618753177306,0.006678279487405518,0.008007461654764927,0.012039865990866828,0.011157049069855658,0.008769981748049546,0.01115714373169865,0.007461752295317582,0.006644621713221858,0.012874563649583002,0.018477411136288955,0.008219077983117256,0.013097427936144915,0.009919024210659978,0.009823439643345538,0.012604865702075158,0.009179576338330175,0.011816705231967,0.009730686461317957,0.00800785186090768,0.007945862001479736,0.01010058267353868,0.007031121339503902,0.012814817506898887,0.008420744423852003,0.007403562729031428,0.011000147969157367,0.01244229311825375,0.0055613292232268895,0.010714685590235404,0.009507078904651701,0.009124532887008027,0.009630394777081289,0.01101473414880652,0.008259910271852723,0.009669003538926354,0.012662429394926926,0.010444267205085423,0.009180980302071545,0.012843016374691324]
experiment['cache_placement']['network_cache'] = 0.1

# Set content placement
if READ_FROM_DATA:
        experiment['content_placement']['name'] = 'DATA_TO_CCF'
else:
        if IS_ZIPF:
                # experiment['content_placement']['name'] = 'UNIFORM'
                # experiment['content_placement']['name'] = 'ZIPF'
                # experiment['content_placement']['alpha'] = 2
                # experiment['content_placement']['is_random'] = True
                experiment['content_placement']['name'] = 'WEIGHTED'
                experiment['content_placement']['source_weights'] =  {101:0.00717587640843523,102:0.011606998319114535,103:0.006016087462422068,104:0.005914283444656411,105:0.006478692947974536,106:0.01701983388614452,107:0.009232771907510715,108:0.010446519914504274,109:0.012372127879358277,110:0.006617389493274116,111:0.013909778865896052,112:0.012293117744125294,113:0.012236466292915643,114:0.012183361995828337,115:0.015368505108308447,116:0.013123931832263479,117:0.010799471293531582,118:0.013102330782238715,119:0.01939242896055647,120:0.008196294857377372,121:0.00471790075319751,122:0.010875036541833309,123:0.010821059995701607,124:0.00837354072923041,125:0.007295098719931155,126:0.006946804843867024,127:0.011753909219172177,128:0.009604436355013266,129:0.007836806421310627,130:0.01097465988128199,131:0.00964887117185679,132:0.011504482358054718,133:0.0053943876535283335,134:0.008443812810819322,135:0.016909371400624356,136:0.010732076877030473,137:0.011717053229578344,138:0.005745317762057413,139:0.014892072467120075,140:0.010792009389835424,141:0.013205419236338799,142:0.012397802550097455,143:0.007625291581446855,144:0.0050816948253824806,145:0.0067734506207572966,146:0.008462165175090275,147:0.009948317059303267,148:0.010741227071503523,149:0.007946667280533799,150:0.011102180621955603,151:0.005938775438089878,152:0.009608452451930346,153:0.009168847873578892,154:0.009311223614989326,155:0.012295813086927884,156:0.007481589727598484,157:0.010286728469988835,158:0.011162487848685008,159:0.013676754515803588,160:0.010087127421981392,161:0.007132288441510841,162:0.011400923071018925,163:0.010120219076405227,164:0.006533076637398351,165:0.007925263632998513,166:0.008923583843611022,167:0.010702836223288955,168:0.007233139106118823,169:0.016158934557966978,170:0.009580761186267864,171:0.010397146483849252,172:0.0070843102475432644,173:0.012476885274924455,174:0.007284960512230228,175:0.016541249446571045,176:0.0089473810424915,177:0.006894718212777233,178:0.009472585767944644,179:0.006426516096867527,180:0.011303822206294285,181:0.007671169926090509,182:0.008678942449546423,183:0.00843142227343899,184:0.007221212944115158,185:0.01018516451130295,186:0.0021447420890588946,187:0.005376540170627375,188:0.01799135205209311,189:0.011631528467686938,190:0.010405364835610043,191:0.013345225581596324,192:0.0111092880809252,193:0.012994163274706077,194:0.007320169720799727,195:0.0105770804803995,196:0.007067522481773677,197:0.009685571549072642,198:0.009007607007003522,199:0.012937671147973099,200:0.012910665438637932}
        else:
                experiment['content_placement']['name'] = 'NORMAL'
                experiment['content_placement']['is_random'] = True

# Set cache replacement policy
experiment['cache_policy']['name'] = 'LRU'

# Set caching meta-policy
experiment['strategy']['name'] = 'LCE'

# Description of the experiment

experiment['desc'] = "Line topology with customized cache"

# Append experiment to queue
EXPERIMENT_QUEUE.append(experiment)
