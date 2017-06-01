# Numpy

## type_conversion

`all_ndarray_to_list(f)`

`f` is a dict and this function will convert all ndarray to list

`coordinate_to_contour)contour`

```python
coor = (array(coor_y, ...), array(coor_x, ...))
cnt = [
    [[coor_x1, coor_y1]],
    [[coor_x2, coor_y2]],
    ..., dtype='int32'
]
cnt.shape = (len(coor[0]), 1, 2)
```