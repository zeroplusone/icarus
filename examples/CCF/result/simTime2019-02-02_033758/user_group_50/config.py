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
        experiment['cache_placement']['cache_allocation'] = [0.00862987386708959,0.010325560280259645,0.010654841019998694,0.009146050819922251,0.014118111453242968,0.013604079774824527,0.007659412839955002,0.007882157971311561,0.01007783098623149,0.008069954881959341,0.004928242636340486,0.009685141483393535,0.01263782404741942,0.008837842614705767,0.009543401758087145,0.00827028087861733,0.010333251859379187,0.012301798209444995,0.013329714237155938,0.011430203151973439,0.00912644762202231,0.013000975750089802,0.0024076032037651054,0.004657616805595107,0.008007589130672347,0.008144776654514217,0.008807713218385013,0.013380316159095297,0.01207719790807822,0.008073401615378135,0.006724123088596406,0.015058063921482932,0.01046321032741715,0.010050963320424733,0.007798840972787569,0.007935392744356267,0.010790548932962428,0.007697511104323446,0.011879651940779347,0.011569679645474654,0.013224533166981543,0.01014766088850708,0.00969684393341202,0.01067895213551383,0.011139817242091564,0.01565692389799619,0.007343238307218695,0.008661302309436743,0.009073486083364352,0.011505316799347166,0.008376870169921672,0.007985217208954943,0.00796107627346612,0.012640176822373329,0.00990915533731745,0.008235046845829963,0.01122347412101297,0.007545980906407704,0.012581480381747582,0.007241898470340472,0.014353954553353582,0.015018034468812265,0.009677629389656495,0.011353074773047877,0.011878869026259177,0.011757249083208628,0.011273204089280533,0.007857446016509924,0.009161243587521226,0.006400895360262826,0.0073933202217158255,0.007719227684951125,0.01326182310580131,0.014941865943489195,0.01140521669592971,0.0052708612558842625,0.009015088100664771,0.009993779199379625,0.004225691306957308,0.009748228525724012,0.017000457930804014,0.007420198994496525,0.01033142568659804,0.007040797876736529,0.007499012938377918,0.013278683231001037,0.013886966156643846,0.005837175455018254,0.0112002992118206,0.010969036583348739,0.0068060357950359245,0.007924912478581899,0.014156242695383054,0.010811910579788008,0.009696968466445475,0.010121471113818557,0.009876887118272419,0.012147893460514286,0.009776342786941148,0.012564928913210063]
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
