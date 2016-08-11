from skimage.io import imread, imsave
from scipy.spatial import cKDTree
import ImageDraw
import random
import math
import numpy as np

import Image

#img = imread(sys.argv[1])[:, :, :3]
# denoised = denoise_bilateral(img, sigma_range=0.1, sigma_spatial=35)

im = Image.new("RGB", (256,256), "white")

def generate_random_point_around(seed, lower_bound_radius, upper_bound_radius):
    """
    generate a point uniformly around a given seed point, from the 
    spherical annulus between two bounding radii
        seed :  tuple (float, float)
        lower_bound_radius : float
        upper_bound_radius : float
    """
    radius = random.uniform(lower_bound_radius, upper_bound_radius)
    angle = random.uniform(0, 2* math.pi)
    offset = np.array([radius * math.sin(angle), radius*math.cos(angle)])
    return tuple(seed + offset)


def get_poisson_points(image, minimum_distance_between_samples, radius):
    h = im.size[0]
    w = im.size[1]
    first_point = (random.uniform(0, h), random.uniform(0,w))
    to_process = [first_point]
    sample_points = [first_point]
    tree = cKDTree(sample_points)

    def no_neighbors(point):
        distances, indexes = tree.query(point, len(sample_points) + 1, distance_upper_bound = minimum_distance_between_samples)
        if len(distances)==0:
            return False
        for dist, index in zip(distances, indexes):
            if np.isinf(dist):
                return True
            if dist < minimum_distance_between_samples:
#                print "thisa actually happens"
                return False

    while to_process:
        pt = to_process.pop(random.randrange(len(to_process)))
        for _ in range(30):
            new_point = generate_random_point_around(pt, radius, 2* radius)
            if (0 <= new_point[0] < h) and (0 <= new_point[1] < w) and (no_neighbors(new_point)):
                to_process.append(new_point)
                sample_points.append(new_point)
                tree = cKDTree(sample_points)
    return sample_points

sample_points = get_poisson_points(im, 20, 30)

draw = ImageDraw.Draw(im)
def makecircle(image, coord, rad):
    draw.ellipse((coord[0] - rad, coord[1] - rad, coord[0] + rad, coord[1] + rad), outline = (255,0,0,0))

for point in sample_points:
    new = (int(point[0]), int(point[1]))
    makecircle(im, new, 10)

im.save("img2.png")
