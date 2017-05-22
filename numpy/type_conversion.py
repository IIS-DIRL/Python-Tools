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
