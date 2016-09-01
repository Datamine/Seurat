from PIL import ImageDraw, Image
from matrix_image import *
import random
import math
import numpy as np
import time

def has_neighbors(imagematrix, x_bound, y_bound, x0, y0, circle_radius, circle_mindist):
    """
    check whether a given point has any neighbors. Returns True if so.
    """
    # print x_bound, y_bound, x0, y0, circle_radius, circle_mindist
    # grid check for the moment instead of the maximum efficiency perimeter check,
    # because i'm lazy. gonna see if this is fast enough
    # print circle_radius
    
    # trigonometry: this is as large as you can space out the points (in a grid) while intersecting any circle placed on them
    stepsize = int(math.floor(2**0.5 * circle_radius))
    
    # we add the last element to make sure we exhaust the entire relevant range
    x_range = range(clip(x0 - circle_mindist, x_bound), clip(x0 + circle_mindist, x_bound), stepsize) + [clip(x0 + circle_mindist, x_bound)]
    for x in x_range:
        height = int(math.ceil((circle_mindist**2 - (x-x0)**2 )**0.5))
        y_range = range(clip(y0 - height, y_bound), clip(y0 + height, y_bound), stepsize) + [clip(y0 + height, y_bound)]

        for y in y_range:
            if np.isnan(imagematrix[x][y][0]):
                #print imagematrix[x][y]
                continue
            else:
                # we didnt actually check if the datapoint is in the circle yet.
                # we're doing this grid search so we have to.
                # imagematrix[x][y] = [255,0,0]
                return True
                """
                if ((x-x0)**2 + (y-y0)**2)**0.5 <= circle_mindist:

                else:
                    print imagematrix[x][y]
                    imagematrix[x][y] = [0,0,255]
                    continue
                """
    return False

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
    return tuple(map(int, seed + offset))

def get_poisson_points(image, mindist, radius):
    """
    runs the poisson disc algorithm to generate sample points.
    mindist: minimum distance between samples
    """
    h = image.size[0]
    w = image.size[1]
    output = make_none_matrix(h,w)

    first_point = (random.uniform(0, h), random.uniform(0,w))
    to_process = [first_point]

    while to_process:
        pt = to_process.pop(random.randrange(len(to_process)))
        for _ in range(30):
            new_point = generate_random_point_around(pt, (2*r)+mindist, (3*r)+mindist)
            if (0 <= new_point[0] < h) and (0 <= new_point[1] < w) and (not has_neighbors(output, h, w, new_point[0], new_point[1], radius, radius+mindist)):
                to_process.append(new_point)
                circle_fill(output, h, w, new_point[0], new_point[1], 2*radius)

    """
    print    output.shape
    output = output.reshape((h,w,3))
    print output.shape
    """
    return output

r = 20
mindist = 50

opened = Image.open("bear.jpg")
opened_h = opened.size[0]
opened_w = opened.size[1]
new = Image.new("RGB", opened.size, "white")

# five repetitions
for i in range(1):
    print i
    start = time.time()
    imagelist = get_poisson_points(opened, mindist, r)
    end = time.time()
    print (end-start)
    #print imagelist.shape

    for i in range(len(imagelist)):
        for j in range(len(imagelist[i])):
            #print imagelist[i][j]
            if not np.isnan(imagelist[i][j][0]):
                new.putpixel((i, j), tuple(map(int, imagelist[i][j])))

new.save("output3.png")
