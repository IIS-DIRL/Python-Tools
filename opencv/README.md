# OpenCV

## connected_component

`get_component_by(threshold, nth, by)`

**threshold** is a label matrix which defined background as 0 and object as 1
```
sample:

image = cv2.imread('sample.png')
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, threshold = cv2.threshold(image, 250, 255, cv2.THRESH_BINARY_INV)
image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

# get the component with largest area
component = get_component_by(threshold, 1, cv2.CC_STAT_AREA)

# visualized
cv2.imshow('output', image[component])
k = cv2.waitKey(1)
if k == 27: break
cv2.destroyAllWindows()
```
