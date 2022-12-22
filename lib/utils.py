import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
import pickle
from .blocks_github import reconstruct_from_patches_2d

def get_data(filename: str) -> np.ndarray:
    file = nib.load(filename)
    data = file.get_fdata()
    return data

def plot_data(data: np.ndarray, scale: float=0.1, dim: int=0, slice: int=50, show=True) -> None:
    shape = list(data.shape)
    shape.pop(dim)
    imgsize = np.multiply(shape, scale)
    if show:
        plt.figure(figsize=imgsize)
    if dim == 0:
        data = data[slice, :, :]
    elif dim == 1:
        data = data[:, slice, :]
    elif dim == 2:
        data = data[:, :, slice]
    else:
        raise ValueError('Wrong dim argument')
    plt.imshow(data)
    if show:
        plt.show()

def load_pickle(filename):
    with open(filename, 'rb') as f:
        out = pickle.load(f)
    return out

def dump_pickle(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)

def plot_image(image, title=None, path=None, size=15):
    plt.figure(figsize=(size, size))
    plt.imshow(image)
    plt.axis('off')
    if title is not None:
        plt.title(title)
    if path is None:
        plt.show()
    else:
        plt.savefig(path)

def pathces2image(patches, shape):
    block_size = int(np.round(np.sqrt(patches.shape[1])))
    patches = patches.reshape(-1, block_size, block_size)
    return reconstruct_from_patches_2d(patches, shape)