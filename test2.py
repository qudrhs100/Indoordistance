

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
points = np.random.random((10, 2))
print(len(points))
# points = np.array([[0, 0], [0, 1.1], [1, 0], [1, 1]])
tri = Delaunay(points)
# for poly in tri.simplices.copy():
#     print(poly)
print(type(points))
print(points)
print(points[:,0])
print(points[:,1])
plt.triplot(points[:,0], points[:,1], tri.simplices.copy())
plt.plot(points[:,0], points[:,1], 'o')
plt.show()