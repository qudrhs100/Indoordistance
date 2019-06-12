from dolfin import *
mesh = UnitSquareMesh(10, 10)
print("Plotting a UnitSquareMesh")
plot(mesh, title="Unit square")