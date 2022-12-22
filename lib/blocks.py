import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

def split_data_to_blocks_2d(data: np.ndarray, block_size, stride):
    tmp = sliding_window_view(data, (block_size, block_size))[::stride, ::stride]
    shape = tmp.shape
    tmp = tmp.reshape(tmp.shape[0] * tmp.shape[1], tmp.shape[2] * tmp.shape[3])
    return tmp, shape

def split_data_to_blocks_3d(data: np.ndarray, block_size, stride):
    return sliding_window_view(data, (block_size, block_size, block_size))[::stride, ::stride, ::stride]

def merge_blocks_2d_no_overlap(blocks, shape):
    x = blocks.reshape(shape)
    x = x.swapaxes(1, 2)
    x = x.reshape((shape[0] * shape[2], shape[1] * shape[3]))
    return x

def _combine_blocks_2d_to_layers_with_stride_1(blocks, shape):
    blocks = blocks.reshape(shape)
    n, m, block_size, _ = shape
    n = (n + block_size - 1)
    m = (m + block_size - 1)
    x = blocks.reshape(shape)
    layers = [None] * (block_size ** 2)
    for layer_id in range(len(layers)):
        i = layer_id // block_size
        j = layer_id % block_size
        layer = blocks[i::block_size, j::block_size]
        layer = layer.swapaxes(1, 2)
        layer = layer.reshape((layer.shape[0] * layer.shape[1], layer.shape[2] * layer.shape[3]))
        layer = np.pad(
            layer, 
            ((i, n - layer.shape[0] - i), (j, m - layer.shape[1] - j)),
            mode='constant',
            constant_values=np.nan # values for which we don't have value we mask with np.nan
        )
        layers[layer_id] = layer
    return layers

def _merge_layers_2d_stide_1(layers):
    layers = np.array(layers)
    mask = ~np.isnan(layers)
    layers[~mask] = 0
    mask = mask.mean(axis=0)
    layers = layers / mask
    layers = layers.mean(axis=0)
    return layers

def merge_blocks_2d_stide_1(blocks, shape):
    layers = _combine_blocks_2d_to_layers_with_stride_1(blocks, shape)
    merged = _merge_layers_2d_stide_1(layers)
    return merged