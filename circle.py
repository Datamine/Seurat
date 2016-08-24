from PIL import Image

def circle(x0, y0, radius):
    """
    adapted from wikipedia article
    """
    x = radius
    y = 0
    err = 0
    while x >= y:
        coords =  [(x0 + x, y0 + y),
                    (x0 - x, y0 + y),
                    (x0 + x, y0 - y),
                    (x0 - x, y0 - y),
                    (x0 + y, y0 + x),
                    (x0 - y, y0 + x),
                    (x0 + y, y0 - x),
                    (x0 - y, y0 - x)]
        y += 1
        err += 1 + 2*y
        if 2*(err-x) + 1 > 0:
            x -= 1
            err += 1 - 2*x
        yield coords

im = Image.new("RGB",(512,512),"white")

for index, next_coords in enumerate(circle(256,256,38)):
    print index
    [im.putpixel((x,y), ((index*10)+10, (index*10)+10, (index*10)+10)) for (x,y) in next_coords]

im.save("asdh.png")
