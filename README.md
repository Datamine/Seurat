# Seurat
Stylizes an image in the pointillist style of Georges Seurat

## Use

`source venv/bin/activate`

## Credits

code partially adapted from http://codegolf.stackexchange.com/questions/50299/draw-an-image-as-a-voronoi-map

## Design Decisions

Using a cKDTree here is suboptimal because you have to reconstruct it on every iteration. This becomes especially tedious
when working with a large image, since that requires a large tree construction. I thought about using an R*-Tree instead, but
couldn't find a Python implementation. Then I realized that of course I don't need the fully abstract solution, but could do
an iterative solution with pixel-checking using the midpoint circle algorithm to check along the perimeter of a proposed
circle.
