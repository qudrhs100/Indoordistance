from shapely import wkt
from shapely.geometry import multilinestring,MultiLineString,Polygon
from shapely.ops import linemerge, unary_union, polygonize



poly_coords=[(0, 0), (2, 0), (2, 2), (0, 2),(0, 0)]
POLY = Polygon(poly_coords)
# print (tuple(poly_coords))

coords = [((-1, 1), (3, 1)), ((1, 3), (1, -3))]

coords.append(tuple(poly_coords))
print(coords)
MULT = MultiLineString(coords)


# merged = linemerge([POLY.boundary, list(MULT.coords)])

#
borders = unary_union(MULT)
polygons = polygonize(borders)
for p in polygons:
    print(p)

