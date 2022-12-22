from .blocks_github import *
from .utils import *
from .nonlocalfiltering import *
from .ksvd import *
from .pipeline import *

FILE_DIS = '/home/alexkkir/ai-masters/linal/project/data/t1_icbm_normal_1mm_pn3_rf20.mnc'
FILE_REF = '/home/alexkkir/ai-masters/linal/project/data/t1_icbm_normal_1mm_pn0_rf20.mnc'
FILE_VST = '/home/alexkkir/ai-masters/linal/project/data/vst_transform.pickle'

data_dis = get_data(FILE_DIS)
data_ref = get_data(FILE_REF)
data_vst = load_pickle(FILE_VST)
data_vst = np.swapaxes(data_vst, 0, 2)