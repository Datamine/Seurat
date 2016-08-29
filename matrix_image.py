from PIL import Image
import numpy as np

"""
small library to handle 'drawing' in a matrix
and interfacing with PIL
"""

def clip(value,bound):
    """
    caps a value such that it is in the interval [0,bound). values outside
    the interval get mapped to the appropriate interval extreme.
    - NB: value/bound is assumed to be an integer.
    """
    return max(0, min(value, bound-1))

def make_none_matrix(h,w):
    """
    makes a matrix the size of the image, filled with NaN
    """
    matrix = np.empty((h,w,3))
    matrix[:] = np.NAN
    return matrix

def circle_perimeter(x_bound, y_bound, x0, y0, radius):
    """
    x-bound: represents the width of the image. i.e. x coord can be [0, x).
    y-bound: represents the height of the image. i.e. y coord can be [0, y).
    point: tuple representing the point at the center of which we define a circle
    radius: float
    algorithm: https://en.wikipedia.org/wiki/Midpoint_circle_algorithm
    implementation: http://degenerateconic.com/midpoint-circle-algorithm/
    """
    x = radius/2
    y = 0
    err = 1-x
    while x >= y:
        coords =   [(clip(x0 + x, x_bound), clip(y0 + y, y_bound)),
                    (clip(x0 - x, x_bound), clip(y0 + y, y_bound)),
                    (clip(x0 + x, x_bound), clip(y0 - y, y_bound)),
                    (clip(x0 - x, x_bound), clip(y0 - y, y_bound)),
                    (clip(x0 + y, x_bound), clip(y0 + x, y_bound)),
                    (clip(x0 - y, x_bound), clip(y0 + x, y_bound)),
                    (clip(x0 + y, x_bound), clip(y0 - x, y_bound)),
                    (clip(x0 - y, x_bound), clip(y0 - x, y_bound))]
        y += 1
        if err < 0:
            err += 2*y + 1
        else:
            x -=1 
            err += 2*(y-x+1)
        yield coords

def drawline(imagematrix, x, y0, y1):
    # no need to return: update the object in place
    if y0 < y1:
        low = y0
        high = y1
    else:
        high = y0
        low = y1
    for y in range(low, high + 1):
        imagematrix[x][y] = [4,150,40]

def circle_fill(imagematrix, x_bound, y_bound, x0, y0, radius):
    """
    x-bound: represents the width of the image. i.e. x coord can be [0, x).
    y-bound: represents the height of the image. i.e. y coord can be [0, y).
    point: tuple representing the point at the center of which we define a circle
    radius: float
    algorithm: https://en.wikipedia.org/wiki/Midpoint_circle_algorithm
    """
    """
    for coords in circle_perimeter(x_bound, y_bound, x0, y0, radius):
        for (x,y) in coords:
            imagematrix[x][y] = [15,15,150]
    """
    x = radius/2
    y = 0
    err = 1-x
    while x >= y:
        drawline(imagematrix, clip(x0 + x, x_bound), clip(y0 + y, y_bound), clip(y0 - y, y_bound))
        drawline(imagematrix, clip(x0 - x, x_bound), clip(y0 + y, y_bound), clip(y0 - y, y_bound))
        drawline(imagematrix, clip(x0 + y, x_bound), clip(y0 + x, y_bound), clip(y0 - x, y_bound))
        drawline(imagematrix, clip(x0 - y, x_bound), clip(y0 - x, y_bound), clip(y0 + x, y_bound))
   
        y += 1
        if err < 0:
            err += 2*y + 1
        else:
            x -=1 
            err += 2*(y-x+1)
