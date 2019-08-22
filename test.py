import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
# points = np.random.random((10, 2))
# points = np.array([[0, 0], [0, 1.1], [1, 0], [1, 1]])
points = np.array([
    [0, 130],
    [50, 130],
    [50, 50],
    [310, 50],
    [310, 30],
    [350, 30],
    [350, 0],
    [390, 0],
    [390, 50],
    [600, 50],
    [600, 90],
    [410, 90],
    [410, 110],
    [320, 110],
    [320, 90],
    [90, 90],
    [90, 260],
    [50, 260],
    [50, 170],
    [0, 170]
])
for i in range(0,22):
    print(i+1," ",i," ",i+1," ",2)

tri = Delaunay(points,furthest_site=False)
# plt.plot(points[:,0], points[:,1], tri.simplices.copy())
print(tri.simplices.copy())
plt.triplot(points[:,0], points[:,1],color='red')
plt.show()