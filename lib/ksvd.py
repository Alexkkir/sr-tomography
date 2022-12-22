import numpy as np
from ksvd import ApproximateKSVD
import nibabel as nib
import matplotlib.pyplot as plt
from .blocks_github import extract_patches_2d, reconstruct_from_patches_2d


def build_ksvd(blocked, n_components=30, n_nonzero=None):
    aksvd = ApproximateKSVD(
        n_components=n_components, 
        # transform_n_nonzero_coefs=n_nonzero
    )
    dictionary = aksvd.fit(blocked).components_
    gamma = aksvd.transform(blocked)
    error = np.abs(gamma @ dictionary - blocked).mean()
    print('MAE: {:.3f}, Nonzero: {}'.format(error, len(np.nonzero(gamma[0]))))
    return dictionary, gamma

def _get_weights(gamma):
    tmp = (gamma != 0).sum(axis=0)
    tmp = tmp / tmp.sum()
    return tmp

def make_weighted_dict(dictionary, gamma, delta=8):
    weights = _get_weights(gamma)
    dictionary_new = dictionary * (1 + delta * weights).reshape(-1, 1)
    return dictionary_new

def ksvd_filtering(image, patch_size=4, n_components=20, n_nonzero=None, delta=2):
    blocked = extract_patches_2d(image, (patch_size, patch_size)).reshape(-1, patch_size ** 2)
    mean = np.mean(blocked, axis=1)[:, np.newaxis]
    # std = np.std(blocked, axis=1)[:, np.newaxis]

    blocked = (blocked - mean)
    D, A = build_ksvd(blocked, n_components=n_components, n_nonzero=n_nonzero)
    D = make_weighted_dict(D, A, delta=delta)
    patches = (A @ D + mean)
    img_modif = reconstruct_from_patches_2d(patches.reshape(-1, patch_size, patch_size), image_size=image.shape)
    return D, A, patches, img_modif
