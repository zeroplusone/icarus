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
        experiment['cache_placement']['cache_allocation'] = [0.007785136676675282, 0.005283149745783625, 0.009061968822243496, 0.007574448096327798, 0.007254234439989959, 0.009393646507826047, 0.007007367729737979, 0.012438373135575406, 0.012466927041800985, 0.008783538222971439, 0.01275946157113067, 0.00966639715387909, 0.011401919670632374, 0.0037592720963470017, 0.014420361690523935, 0.013440380142940342, 0.011595734133595268, 0.014465278326856838, 0.004322145284432624, 0.010973477010680301, 0.010040064162950096, 0.008025701605608834, 0.01272615120645417, 0.009713088417405287, 0.010926229813338451, 0.008260738902492813, 0.010425512782690827, 0.012131239973806881, 0.007348023903693895, 0.009005312702846678, 0.010644018641352544, 0.014144200168270166, 0.005425245308309841, 0.009033931833815113, 0.00614503827856954, 0.015807036434401164, 0.006778343121793816, 0.010202440010991912, 0.013061575394076702, 0.014426655320280958, 0.006787897994852213, 0.008262193535089567, 0.00909401849727308, 0.011005137770088979, 0.009347095908844189, 0.008594462195483491, 0.010481998247182262, 0.010838810748804766, 0.008171599929496853, 0.009786262780138447, 0.007943543016405524, 0.009678854436698945, 0.011562162456303713, 0.011218777308862704, 0.005372073955210914, 0.008256341922865859, 0.00845771369685141, 0.011153686481319782, 0.013970493115218061, 0.009898031262420816, 0.007046401254999441, 0.007892353554222114, 0.014177140903696475, 0.008999556744304684, 0.009650087154609239, 0.009766191972987498, 0.0069609141880179835, 0.012697759389735615, 0.011646525373832591, 0.005754291872461571, 0.00799493262501059, 0.009975776717074723, 0.010288767417449584, 0.014092688696053332, 0.011123029681577551, 0.01230237080330334, 0.008706074997707888, 0.01348827725560945, 0.008737455614201878, 0.010876765377664587, 0.011085013372985775, 0.010163255477675957, 0.010958241357554868, 0.005488905925270465, 0.009241973264155323, 0.01098753871771378, 0.005986082169301273, 0.007305954282792846, 0.014464293333845751, 0.010419478826510812, 0.01328083757759328, 0.00910430123967865, 0.007805501610166856, 0.008247628431284326, 0.010658239369073492, 0.010259009079013762, 0.015546912163028545, 0.012514055047575596, 0.012510603254838241, 0.013789893162908653]
experiment['cache_placement']['network_cache'] = 0.1

# Set content placement
if READ_FROM_DATA:
        experiment['content_placement']['name'] = 'DATA_TO_CCF'
else:
        if IS_ZIPF:
                experiment['content_placement']['name'] = 'WEIGHTED'
                experiment['content_placement']['source_weights'] = {}
                # experiment['content_placement']['name'] = 'UNIFORM'
                # experiment['content_placement']['name'] = 'ZIPF'
                # experiment['content_placement']['alpha'] = 2
                # experiment['content_placement']['is_random'] = True
        else:
                experiment['content_placement']['name'] = 'WEIGHTED'
                experiment['content_placement']['source_weights'] =  {}
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
