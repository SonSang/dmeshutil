import numpy as np
import itertools

def sort_and_unique(arrays: np.ndarray):
    '''
    Sort and unique a list of arrays.

    @ arrays: [N, D] numpy array, where N is the number of items and D is the number of elements per item.
    '''

    return np.unique(np.sort(arrays, axis=1), axis=0)

def extract_faces(cells: np.ndarray):
    '''
    Extract faces from a list of cells.

    @ cells: [N, D] numpy array, where N is the number of cells and D is the number of vertices per cell.
    '''

    N, D = cells.shape
    combs = itertools.combinations(range(D), D - 1)

    faces = []
    for comb in combs:
        faces.append(cells[:, comb])
    faces = np.concatenate(faces, axis=0)

    return sort_and_unique(faces)