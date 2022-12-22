import numpy as np
from numba import jit
from tqdm import tqdm
from .ksvd import _get_weights
from .blocks_github import reconstruct_from_patches_2d

def get_I(A):
    I = {}
    for i in range(len(A)):
        I[i] = list(np.nonzero(A[i])[0])
    return I

def get_M(A):
    M = {}
    for i in range(len(A)):
        M[i] = np.argmax(np.abs(A[i]))
    return M

def get_CSS(A, M, I):
    CSS = {}
    for i in tqdm(range(A.shape[0]), 'CSS'):
        CSS[i] = []
        for j in M:
            if M[j] in I[i]:
                CSS[i].append(j)
    return CSS

def get_CC(CSS, y, th=0.1):
    CC = {}
    for i in tqdm(CSS, 'SS'):
        CC[i] = []
        for j in CSS[i]:
            if np.linalg.norm(y[i] - y[j]) / np.linalg.norm(y[i]) < th:
                CC[i].append(y[j])
    return CC

def fake_svd(CC, shape):
    out = np.zeros(shape)
    for i in CC:
        group = np.array(CC[i])
        group = group.mean(axis=0)
        out[i] = group
    return out

def make_svd(CC, shape, n_truncate=10):
    out = np.zeros(shape)
    for i in CC:
        group = CC[i]
        U, S, Vt = np.linalg.svd(group, full_matrices=False)
        S[n_truncate:] = 0
        group = U * S @ Vt
        group = group.mean(axis=0)
        out[i] = group
    return out

def averaging_patch(A, patches, shape):
    weights = _get_weights(A)
    weights /= np.linalg.norm(weights)
    blocks_weights = 1 - np.abs(A @ weights) / np.linalg.norm(A, axis=1)
    weighted_im = reconstruct_from_patches_2d((patches * blocks_weights[:, None]).reshape(-1, 4, 4), shape)
    weights_for_im = reconstruct_from_patches_2d((np.ones_like(patches) * blocks_weights[:, None]).reshape(-1, 4, 4), shape)
    image = weighted_im / weights_for_im
    return image
