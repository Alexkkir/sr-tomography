import numpy as np
from .blocks_github import *
from .ksvd import *
from .nonlocalfiltering import *
from .utils import *

def filter_image(image, out_dict, th_ss=0.15, svd_truncate=5):
    D, A, patches_restored, img_restored = ksvd_filtering(image)
    out_dict['ksvd'] = img_restored

    I = get_I(A)
    M = get_M(A)
    CSS = get_CSS(A, M, I)

    CC = get_CC(CSS, patches_restored, th=th_ss)

    without_svd = fake_svd(CC, patches_restored.shape)
    without_svd = pathces2image(without_svd, image.shape)
    out_dict['nonlocal'] = without_svd

    patches_svd = make_svd(CC, patches_restored.shape, n_truncate=svd_truncate)
    out_dict['svd'] = pathces2image(patches_svd, image.shape)

    weighted_image = averaging_patch(A, patches_svd, image.shape)
    out_dict['averaging'] = weighted_image
    return out_dict


