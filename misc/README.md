# Python-Tools-misc
### Python (version2.7) useful functions

#### python2_function_hander.py
See the script to get how to use it  
 - rgbImage_equalizeHist  
 do image equalize histogram to the RGB image  
 - img_rand_crop  
 random crop a image  
 - img_center_crop  
 crop the image by center  
 - image_scatter  
 plot t-sne scatter plot (especially for plot keras model)  

#### img_resize.py
A script to resize multiple image
```
usage: img_resize.py [-h] [-i IMAGE [IMAGE ...]]
                     [-r RECURSIVE [RECURSIVE ...]] [--height HEIGHT]
                     [--width WIDTH]

interactive graph cut for moth image

optional arguments:
  -h, --help            show this help message and exit
  -i IMAGE [IMAGE ...], --image IMAGE [IMAGE ...]
                        process input image
  -r RECURSIVE [RECURSIVE ...], --recursive RECURSIVE [RECURSIVE ...]
                        process all image in given directory
  --height HEIGHT       the height of resized image
  --width WIDTH         the width of resized image
```
