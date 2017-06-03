# -*- coding: utf-8 -*-
"""
Book Cover Perspective transformation
Task:
    1) Judge the book cover is flat (2D) or volume (3D)
    2) If it is a 3D cover, transform it

2017/05/15 -- Sean
"""

#%%
# Libraries import
import os
import numpy as np
import scipy as sp
from scipy import ndimage
import math
import cv2
import glob
import sys

from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.axes_grid1 import ImageGrid

from skimage import filters
import skimage.morphology
from skimage import io as skio
from skimage.feature import corner_harris, corner_subpix, corner_peaks
from skimage.transform import (hough_line, hough_line_peaks, probabilistic_hough_line)
from skimage.segmentation import clear_border, boundaries
from skimage import measure
from skimage.color import label2rgb
from skimage.draw import polygon

def do_perspective_transform(im_path, out_name):
    img = skio.imread(im_path, as_grey=1)

    sobel = filters.sobel(img)
    thres = 0.015 ### this is an important parameter
    sobel[sobel > thres] = 1.
    sobel[sobel <= thres] = 0.

    eroded = ndimage.binary_erosion(sobel)
    reconstruc = ndimage.binary_propagation(eroded, mask=sobel)
    reconstruc = ndimage.binary_closing(reconstruc, iterations=2)

    im_dilation = skimage.morphology.binary_dilation(reconstruc)
    #plt.imshow(im_dilation, cmap = 'gray')
    #plt.show()

    im_dilation = clear_border(im_dilation)
    contours = measure.find_contours(im_dilation, 0.1)
    label_image = measure.label(im_dilation)
        
    region = measure.regionprops(label_image)[0]
    minr, minc, maxr, maxc = region.bbox
    rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                              fill=False, edgecolor='red', linewidth=2)

    #fig, ax = plt.subplots()
    #ax.imshow(img, cmap = 'gray')
    #ax.plot(contours[0][:, 1], contours[0][:, 0], linewidth = 2)
    #ax.set_xlim([0,255])
    #ax.set_ylim([255, 0])
    #ax.add_patch(rect)
    #ax.set_axis_off()
    #plt.show()

    # do rotation estimation 
    middle = 128
    msk = np.zeros((255, 255))
    rr, cc = polygon(contours[0][:, 1], contours[0][:, 0])
    msk[cc, rr] = 1
    plt.imshow(msk, cmap = 'gray')
    plt.show()

    ex = msk.mean(axis= 0)
    ey = msk.mean(axis= 1)

    ex_diff = abs(np.diff(ex))
    ey_diff = abs(np.diff(ey))
    est_long = msk.sum(axis=0)
    plt.plot(ex, 'b')
    plt.plot(ey, 'r')
    plt.show()
    #plt.plot(ey_diff)
    # upper / lower points
    ul_line1 = ey_diff[:middle].argmax()
    ul_line2 = middle + ey_diff[middle:].argmax()

    # add judgement crit (false mask)
    x_dis = np.where(ex > 0)[0]
    if x_dis[-1] - x_dis[0] < 256/4: # quarter of full image size
        print('fail') # should return None in a function

    # add flat view simple task    
    xp = np.diff(ex)
    loc1 = np.where(xp == xp.max())[0][0] + 1 # left side
    loc2 = np.where(xp == xp.min())[0][0] # right side
    x_rect = np.zeros(ex.shape)

    x_rect[loc1:loc2] = np.mean([ex[loc1], ex[loc2]])
    if np.mean(abs(x_rect - ex)) > 0.1:
        print('fail')

    # once True, slide to right
    if ex[:middle].max() > ex[middle:].max():
        # left larger than right
        short_side = middle + ex_diff[middle:].argmax() - 2
    else:
        short_side = ex_diff[:middle].argmax() + 2
    long_side = np.where(est_long == est_long.max())[0][0]
        
    short_side_y = msk[:,short_side].nonzero()[0]
    out_pt1 = (short_side, short_side_y[0])
    out_pt2 = (short_side, short_side_y[-1])
    out_pt3 = (long_side, ul_line1)
    out_pt4 = (long_side, ul_line2)

    #plt.imshow(img, cmap = 'gray')
    #plt.axhline(ul_line1)
    #plt.axhline(ul_line2)
    #plt.axvline(short_side)
    #plt.axvline(long_side)

    #plt.show()
    #plt.axvline(lr_pt1)
    #plt.axvline(lr_pt2)

    if ex[:middle].max() > ex[middle:].max():
        p1 = out_pt3
        p2 = out_pt1
        p3 = out_pt4
        p4 = out_pt2
    else:
        p1 = out_pt1
        p2 = out_pt3
        p3 = out_pt2
        p4 = out_pt4

    #plt.imshow(img, cmap = 'gray')
    #plt.plot(p1[0], p1[1], 'ro')
    #plt.plot(p2[0], p2[1], 'bo')
    #plt.plot(p3[0], p3[1], 'go')
    #plt.plot(p4[0], p4[1], 'mo')
    #plt.show()

    img = cv2.imread(im_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    approx = np.float32([p1, p2, p3, p4 ])
    if ex[:middle].max() > ex[middle:].max():
        l_adj = np.ceil(pt_distance(p1, p2))
        new_p2 = [p1[0] + l_adj, p1[1]]
        new_p4 = [p3[0] + l_adj, p3[1]]
        to_pts = np.float32([p1, new_p2, p3, new_p4])
    else:
        l_adj = np.ceil(pt_distance(p1, p2))
        new_p2 = [p1[0] + l_adj, p1[1]]
        new_p4 = [p3[0] + l_adj, p3[1]]
        to_pts = np.float32([p1, new_p2, p3, new_p4])

    M = cv2.getPerspectiveTransform(approx, to_pts)
    dst = cv2.warpPerspective(img, M, (256, 256) )
    #plt.imshow(dst)
    #plt.show()

    test = masking_image(dst, to_pts)
    #plt.imshow(test)
    skio.imsave(arr= test, fname=out_name)
    return True
#

def masking_image(img, pt_array):
    y_min = pt_array[:, 0].min()
    y_max = pt_array[:, 0].max()
    x_min = pt_array[:, 1].min()
    x_max = pt_array[:, 1].max()
    msk = np.zeros(img.shape, dtype = 'bool')
    msk[x_min:x_max, y_min:y_max, :] = True
    img = img * msk
    img[~msk] = 255
    return img

def pt_distance(pt1, pt2):
    return math.sqrt( (pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2 )