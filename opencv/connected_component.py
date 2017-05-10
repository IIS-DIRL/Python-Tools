import numpy as np
import cv2

def get_component_by(threshold, nth, by):
    '''
    return nth connected component by the value in stat matrix
    in descending sequences
        cv2.CC_STAT_LEFT The leftmost (x) coordinate
        cv2.CC_STAT_TOP The topmost (y) coordinate
        cv2.CC_STAT_WIDTH The horizontal size of the bounding box
        cv2.CC_STAT_HEIGHT The vertical size of the bounding box
        cv2.CC_STAT_AREA The total area (in pixels) of the connected component
    '''
    output = cv2.connectedComponentsWithStats(threshold, 4, cv2.CV_32S)
    assert by in [
        cv2.CC_STAT_LEFT, cv2.CC_STAT_TOP,
        cv2.CC_STAT_WIDTH, cv2.CC_STAT_HEIGHT, cv2.CC_STAT_AREA]
    assert 0 < nth < output[0]

    cond_sequence = [(i ,output[2][i][by]) for i in range(output[0]) if i != 0]
    cond_sequence = sorted(cond_sequence, key=lambda x: x[1], reverse=True)
    return np.where(output[1] == cond_sequence[nth-1][0])
