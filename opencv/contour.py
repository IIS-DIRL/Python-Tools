import numpy as np
import cv2


def coor_to_contour(coor):
    '''
    coor: (array(y_coor), array(x_coor))
    contour = array([
        [[coor[0]]],
        [[coor[1]]],
        ...,
        dtype=int32
    ])
    '''
    coor = list(zip(coor[1], coor[0]))
    contour = np.zeros(shape=(len(coor), 1, 2))
    for i in range(len(coor)): contour[i] = coor[i]
    contour = contour.astype('int32')
    return contour
