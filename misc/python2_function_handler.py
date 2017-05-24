# python2 - function handler

from PIL import Image
from skimage.transform import resize
import cv2
import glob
import numpy as np

def rgbImage_equalizeHist(img):
    # input: numpy array (rgb image)
    # return numpy array (rgb image)
    img_YCrCb = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
    c1, c2, c3 = cv2.split(img_YCrCb)
    c1 = cv2.equalizeHist(c1)
    img_back = cv2.merge((c1,c2,c3))
    img_back = cv2.cvtColor(img_back, cv2.COLOR_YCrCb2RGB)
    return img_back


def img_rand_crop(img, crop_range, target_range):
    # img: 3d-array
    # crop_range: tuple
    # target range: tuple
    cx, cy = crop_range
    max_x, max_y = img.shape[0:2]
    img_w, img_h = target_range
    
    # define max border
    anchor_x_range = max_x - cx
    anchor_y_range = max_y - cy
    # random get
    x_left = np.random.randint(anchor_x_range)
    y_top = np.random.randint(anchor_y_range)
    #
    im_get = img[x_left:x_left+cx, y_top:y_top+cy, :]
    im_get = np.array(resize(im_get, (img_w,img_h), mode = 'reflect'))
    return im_get

def img_center_crop(img, target_size):
    # return center cropprd image (not resizing)
    # img should be a PIL image object
    # target size should be a tuple, eg (224, 224)
    width, height = img.size
    left = (width - target_size[0])/2
    right = (width + target_size[0])/2
    top = (height - target_size[1])/2
    bottom = (height + target_size[1])/2
    
    img.crop((left, top, right, bottom))
    return(img)

### Image with t-sne reduction -- visualization module
def min_resize(img, size):
    w, h = map(float, img.shape[:,2])
    if min([w, h]) != size:
            if w <= h:
                img = resize(img, (int(round((h/w)*size)), int(size)))
            else:
                img = resize(img, (int(size), int(round((w/h)*size))))
    return img

def img_resize(img, size):
    img = resize(img, (size, size))

def gray_to_color(img):
    if len(img.shape) == 2:
        img = np.dstack([img] * 3)
    return img

def image_scatter(tsne_features, images, res = 1024, cval = 1.):
    # tsne_features: projection of tsne
    # images: np.array list of images (4-D or 3D, N x img_w x img_h) -- in RGB / gray
    # img_res: single image size
    # res: full image res
    # cval: backgroud color value
    tsne_features = tsne_features.astype('float64')
    images = [gray_to_color(image) for image in images]
    images = np.array(images)
    #images = [min_resize(image, img_res) for image in images]
    
    max_width = max([image.shape[0] for image in images])
    max_height = max([image.shape[1] for image in images])
    
    xx = tsne_features[:, 0]
    yy = tsne_features[:, 1]

    x_min, x_max = xx.min(), xx.max()
    y_min, y_max = yy.min(), yy.max()

    sx = (x_max-x_min)
    sy = (y_max-y_min)
    if sx > sy:
        res_x = sx/float(sy)*res
        res_y = res
    else:
        res_x = res
        res_y = sy/float(sx)*res
    #print(res_x, res_y, max_width, max_height)
    res_x = int(res_x)
    res_y = int(res_y)
    
    canvas = np.ones((res_x+max_width, res_y+max_height, 3))*cval
    x_coords = np.linspace(x_min, x_max, res_x)
    y_coords = np.linspace(y_min, y_max, res_y)

    for x,y,image in zip(xx, yy, images):
        w,h = image.shape[:2]
        x_idx = np.argmin((x - x_coords)**2)
        y_idx = np.argmin((y - y_coords)**2)
        canvas[x_idx:x_idx+w, y_idx:y_idx+h] = image
    return canvas
###

