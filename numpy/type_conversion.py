import numpy as np


def all_ndarray_to_list(f):
    assert isinstance(f, dict)

    for k,v in f.items():
        if isinstance(v, dict):
            v = all_to_list(v)
        elif isinstance(v, np.ndarray):
            v = v.tolist()
        elif isinstance(v, tuple):
            v = tuple(i.tolist() if isinstance(i, np.ndarray) else i for i in v)
        else:
            print('Not support {} in the type of {}'.format(k, type(v)))

    return f
