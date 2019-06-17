import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
import shapely.geometry
import shapely.ops

points = np.random.random((10, 2))
vor = Voronoi(points)
voronoi_plot_2d(vor)
lines = [
    shapely.geometry.LineString(vor.vertices[line])
    for line in vor.ridge_vertices
    if -1 not in line
]
for poly in shapely.ops.polygonize(lines):
    print(poly)
# print(lines)
