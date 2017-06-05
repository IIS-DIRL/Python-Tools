import numpy as np


def all_ndarray_to_list(f):
    assert isinstance(f, dict)

    for k,v in f.items():
        if isinstance(v, dict):
            f.update({k: all_to_list(v)})
        elif isinstance(v, np.ndarray):
            f.update({k: v.tolist()})
        elif isinstance(v, tuple):
            v = tuple(i.tolist() if isinstance(i, np.ndarray) else i for i in v)
            f.update({k: v})
        else:
            print('Not support {} in the type of {}'.format(k, type(v)))

    return f

def coordinate_to_contour(coor):
    '''
    coor = (array(coor_y, ...), array(coor_x, ...))
    cnt = [
        [[coor_x1, coor_y1]],
        [[coor_x2, coor_y2]],
        ...
    ]
    cnt.shape = (len(coor[0]), 1, 2)
    '''
    cnt = list(contour)
    cnt.reverse()
    cnt = np.array(cnt)
    cnt = cnt.transpose()
    cnt = cnt.reshape((cnt.shape[0], 1, 2))
    cnt = cnt.astype('int32')
    return cnt
