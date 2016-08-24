from scipy.spatial import cKDTree
from PIL import ImageDraw, Image
import random
import math
import numpy as np

def make_none_matrix(h,w):
    """
    makes a matrix the size of the image, filled with NaN
    """
    matrix = np.empty((h,w,))
    matrix[:] = np.NAN
    return matrix

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

def drawline(imagematrix, x0, y0, x1, y1):


def circle_fill(imagematrix, x_bound, y_bound, x0, y0, radius):
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
        drawline(imagematrix, (clip(x0 + x, x_bound), clip(y0 + y, y_bound)))
        drawline(imagematrix, (clip(x0 - x, x_bound), clip(y0 + y, y_bound)))
        drawline(imagematrix, (clip(x0 + x, x_bound), clip(y0 - y, y_bound)))
        drawline(imagematrix, (clip(x0 - x, x_bound), clip(y0 - y, y_bound)))
        drawline(imagematrix, (clip(x0 + y, x_bound), clip(y0 + x, y_bound)))
        drawline(imagematrix, (clip(x0 - y, x_bound), clip(y0 + x, y_bound)))
        drawline(imagematrix, (clip(x0 + y, x_bound), clip(y0 - x, y_bound)))
        drawline(imagematrix, (clip(x0 - y, x_bound), clip(y0 - x, y_bound)))
        y += 1
        err += 1 + 2*y
        if 2*(err-x) + 1 > 0:
            x -= 1
            err += 1 - 2*x

def check_candidate(imagematrix, x_bound, y_bound, x0, y0, radius):
    """
    check whether a given point has any neighbors. Returns False if so.
    """
    # we use a generator to iteratively check the points on the perimeter
    # rather than generating them all at once, which would take much longer. 
    for coords in circle_perimeter(x_bound, y_bound, x0, y0, radius):
        for (x,y) in coords:
            # we set all pixels in the imagematrix to None at first.
            if np.isnan(imagematrix[x][y]):
                return False
    return True

def generate_random_point_around(seed, lower_bound_radius, upper_bound_radius):
    """
    generate a point uniformly around a given seed point, from the 
    spherical annulus between two bounding radii
        seed :  tuple (float, float)
        lower_bound_radius : float
        upper_bound_radius : float
    """
    radius = random.uniform(lower_bound_radius, upper_bound_radius)
    angle = random.uniform(0, 2 * math.pi)
    offset = np.array([radius * math.sin(angle), radius * math.cos(angle)])
    return tuple(seed + offset)

def get_poisson_points(image, minimum_distance_between_samples, radius):
    """
    runs the poisson disc algorithm to generate sample points.
    """
    h = image.size[0]
    w = image.size[1]
    output = make_none_matrix(h,w)

    first_point = (random.uniform(0, h), random.uniform(0,w))
    to_process = [first_point]
    #tree = cKDTree(sample_points, compact_nodes=False, balanced_tree=False)

    while to_process:
        pt = to_process.pop(random.randrange(len(to_process)))
        for _ in range(30):
            new_point = generate_random_point_around(pt, radius, 2*radius)
            if (0 <= new_point[0] < h) and (0 <= new_point[1] < w) and \
            check_candidate(output, w, h, new_point[0], new_point[1], radius):
                to_process.append(new_point)
                circle_fill(output, w, h, new_point[0], new_point[1], radius)
                #tree = cKDTree(sample_points, compact_nodes=False, balanced_tree=False)
    # return a list
    output.flatten()
    return output

r = 3
mind = 5

opened = Image.open("bear.jpg")
opened_h = opened.size[0]
opened_w = opened.size[1]
new = Image.new("RGB", opened.size, "white")
draw = ImageDraw.Draw(new)

import time

# five repetitions
for i in range(1):
    print i
    start = time.time()
    imagelist = get_poisson_points(opened, 2*r, mind)
    end = time.time()
    print (end-start)

    for i in range(len(imagelist)):
        if not np.isnan(imagelist[i]):
            x_coord = i / w
            y_coord = i % w
            new.putpixel((x_coord, y_coord), imagelist[i])

new.save("output2.png")
