from PIL import ImageDraw, Image
from matrix_image import *
import random
import math
import numpy as np
import time

def check_candidate(imagematrix, x_bound, y_bound, x0, y0, radius):
    """
    check whether a given point has any neighbors. Returns False if so.
    """
    
    # we use a generator to iteratively check the points on the perimeter
    # rather than generating them all at once, which would take much longer. 
    #print ">>>", x_bound, y_bound
    for coords in circle_perimeter(x_bound, y_bound, x0, y0, radius):
        for (x,y) in coords:
            # we set all pixels in the imagematrix to None at first.
            if np.isnan(imagematrix[x][y][0]):
                #imagematrix[x][y] = [0,0,255]
                continue
            else:
                imagematrix[x][y] = [255,0,0]
                return False

    # gotta check inside as well
    if not np.isnan(imagematrix[x0][y0][0]):
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
            new_point = generate_random_point_around(pt, r+mindist, 2*(r+mindist))
            if (0 <= new_point[0] < h) and (0 <= new_point[1] < w) and check_candidate(output, h, w, new_point[0], new_point[1], radius+mindist):
                to_process.append(new_point)
                circle_fill(output, h, w, new_point[0], new_point[1], radius)

    output = output.reshape((h,w,3))
    return output

r = 3
mindist = 150

opened = Image.open("bear.jpg")
opened_h = opened.size[0]
opened_w = opened.size[1]
new = Image.new("RGB", opened.size, "white")

# five repetitions
for i in range(1):
    print i
    start = time.time()
    imagelist = get_poisson_points(opened, mindist, 2*r)
    end = time.time()
    print (end-start)
    #print imagelist.shape

    for i in range(len(imagelist)):
        for j in range(len(imagelist[i])):
            #print imagelist[i][j]
            if not np.isnan(imagelist[i][j][0]):
                new.putpixel((i, j), tuple(map(int, imagelist[i][j])))

new.save("output3.png")
