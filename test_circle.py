from PIL import Image
import numpy as np

def clip(value,bound):
    """
    caps a value such that it is in the interval [0,bound). values outside
    the interval get mapped to the appropriate interval extreme.
    - NB: value/bound is assumed to be an integer.
    """
    return max(0, min(value, bound-1))

def circle_perimeter(x_bound, y_bound, x0, y0, radius):
    """
    x-bound: represents the width of the image. i.e. x coord can be [0, x).
    y-bound: represents the height of the image. i.e. y coord can be [0, y).
    point: tuple representing the point at the center of which we define a circle
    radius: float
    algorithm: https://en.wikipedia.org/wiki/Midpoint_circle_algorithm
    implementation: http://degenerateconic.com/midpoint-circle-algorithm/
    """
    x = radius
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

def circle_perimeter2(x_bound, y_bound, x0, y0, radius):
    """
    x-bound: represents the width of the image. i.e. x coord can be [0, x).
    y-bound: represents the height of the image. i.e. y coord can be [0, y).
    point: tuple representing the point at the center of which we define a circle
    radius: float
    algorithm: https://en.wikipedia.org/wiki/Midpoint_circle_algorithm
    """
    x = radius
    y = 0
    err = 0
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
        err += 1 + 2*y
        if 2*(err-x) + 1 > 0:
            x -= 1
            err += 1 - 2*x
        yield coords

im = Image.new("RGB", (128, 128), "white")
radius = 3

for coords in circle_perimeter(128, 128, 64, 64, radius):
    for (x,y) in coords:
        im.putpixel((x,y),(50, 200, 50))

im.save('ytest.png')
