from PIL import ImageFilter, Image
from matrix_image import *
import random
import math
import numpy as np
import time

def has_neighbors(imagematrix, x_bound, y_bound, x0, y0, circle_radius, circle_mindist):
    """
    check whether a given point has any neighbors. Returns True if so.
    """
    # trigonometry: this is as large as you can space out the points (in a grid) while intersecting any circle placed on them
    stepsize = int(math.floor(2**0.5 * circle_radius))
    
    # we add the last element to make sure we exhaust the entire relevant range
    x_range = range(clip(x0 - circle_mindist, x_bound), clip(x0 + circle_mindist, x_bound), stepsize) + [clip(x0 + circle_mindist, x_bound)]
    for x in x_range:
        height = int(math.ceil((circle_mindist**2 - (x-x0)**2 )**0.5))
        
        # we do this particular y range in order not to check the 1/4 of the grid that does not contain the circle.
        y_range = range(clip(y0 - height, y_bound), clip(y0 + height, y_bound), stepsize) + [clip(y0 + height, y_bound)]
        for y in y_range:
            if np.isnan(imagematrix[x][y][0]):
                continue
            else:
                return True
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
                color = image.getpixel(new_point)
                circle_fill(color, output, h, w, new_point[0], new_point[1], radius)
    return output

r = 3
mindist = 5

opened = Image.open("bear.jpg")
opened_h = opened.size[0]
opened_w = opened.size[1]
#new = Image.new("RGBA", opened.size, (255,255,255,255))
new = opened.filter(ImageFilter.GaussianBlur(radius=4))
#ew = new.convert("RGBA")

# five repetitions
rangelim = 5
for layer in range(rangelim):
    layer_image = Image.new("RGB", opened.size)
    # print layer_image.getpixel((0,0))
    print "layer", layer
    start = time.time()
    imagelist = get_poisson_points(opened, mindist, r)
    end = time.time()
    print (end-start)

    for i in range(len(imagelist)):
        for j in range(len(imagelist[i])):
            if not np.isnan(imagelist[i][j][0]):
                layer_image.putpixel((i, j), tuple(map(int, imagelist[i][j])))
            else:
                layer_image.putpixel((i,j), new.getpixel((i,j)))
                #print layer_image.getpixel((i,j))
    #           could put the pixel from the previous layer here... but that would hit the blur and hurt the alpha overlay strategy.
    # layer_image = layer_image.filter(ImageFilter.GaussianBlur(radius=2))
    new = layer_image
    """
    for i in range(len(imagelist)):
        for j in range(len(imagelist)):
            
    R, G, B, A = layer_image.split()
    print A.getpixel((0,0))
    layer_image = Image.merge("RGB", (R,G,B))
    mask = Image.merge("L", (A,))
    new.paste(layer_image, (0,0), mask)
    """
    #new = Image.composite(layer_image, new,  mask)
    #new = Image.alpha_composite(new, layer_image)
    #new = Image.blend(new, layer_image, 0.05)
    #new.paste(layer_image, (0, 0), layer_image)
    if layer == rangelim-1:
        new = new.filter(ImageFilter.GaussianBlur(radius=1))
    new.save("output"+str(layer)+".png")
