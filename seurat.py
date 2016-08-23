from scipy.spatial import cKDTree
from PIL import ImageDraw, Image
import random
import math
import numpy as np

def circle_perimeter(x_bound, y_bound, point, radius):
    """
    x-bound: represents the width of the image. i.e. x coord can be [0, x).
    y-bound: represents the height of the image. i.e. y coord can be [0, y).
    point: tuple representing the point at the center of which we define a circle
    radius: float
    """
    

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

def no_neighbors(point, sample_points, tree, mindist):
    """
    returns True if a new point has no neighbors within the mindist distance.
        point : tuple (float, float)
        tree : cKDTree
        mindist : float
    """
    distance, _ = tree.query(point, 1, distance_upper_bound = mindist)
    if distance < mindist:
        return False
    # otherwise distance is inf.
    return True

def get_poisson_points(image, minimum_distance_between_samples, radius):
    """
    runs the poisson disc algorithm to generate sample points.
    """
    h = image.size[0]
    w = image.size[1]
    first_point = (random.uniform(0, h), random.uniform(0,w))
    to_process = [first_point]
    sample_points = [first_point]
    tree = cKDTree(sample_points, compact_nodes=False, balanced_tree=False)

    while to_process:
        pt = to_process.pop(random.randrange(len(to_process)))
        for _ in range(30):
            new_point = generate_random_point_around(pt, radius, 2*radius)
            if (0 <= new_point[0] < h) and (0 <= new_point[1] < w) and \
            (no_neighbors(new_point, sample_points, tree, minimum_distance_between_samples)):
                to_process.append(new_point)
                sample_points.append(new_point)
                tree = cKDTree(sample_points, compact_nodes=False, balanced_tree=False)
    return sample_points

r = 3
mind = 5

def makecircle(image, coord, rad, color):
    # fill with low alpha
    draw.ellipse((coord[0] - rad, coord[1] - rad, coord[0] + rad, coord[1] + rad), fill = color)

opened = Image.open("bear.jpg")
new = Image.new("RGB", opened.size, "white")
draw = ImageDraw.Draw(new)

import time

# five repetitions
for i in range(1):
    print i
    start = time.time()
    sample_points = get_poisson_points(opened, 2*r, mind)
    end = time.time()
    print (end-start)

    for point in sample_points:
        samplecolor = opened.getpixel(point)
        new_point = (int(point[0]), int(point[1]))
        makecircle(new, new_point, r, samplecolor)

new.save("output2.png")
