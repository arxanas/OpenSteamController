import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

# (x_coord, y_coord, x_ampl, y_ampl)
data_lines = """
  0     350    1362     574
300     525    1944    1446
300     350    2375    2135
300     175    2020    1848
600     700    1172    2838
600     525    1908    2556
600     350    2719    3271
600     175    2133    2460
600       0     518    1950
900     525    2037    2260
900     350    2923    2212
900     175    2319    2015
1125    350    1553    2813
""".strip().split("\n")
data = np.array([[int(x) for x in line.split()] for line in data_lines])
x_coord = data[:, 0]
y_coord = data[:, 1]
x_ampl = data[:, 2]
y_ampl = data[:, 3]


# See https://www.geeksforgeeks.org/3d-curve-fitting-with-python/
def func(xy, a, b, c, d, e, f):
    x, y = xy
    return a + b * x + c * y + d * x**2 + e * y**2 + f * x * y


(x_popt, x_pcov) = sp.optimize.curve_fit(func, (x_coord, y_coord), x_ampl)
(y_popt, y_pcov) = sp.optimize.curve_fit(func, (x_coord, y_coord), y_ampl)

fig = plt.figure(2)

x_grid = np.linspace(0, max(x_coord), 4 * len(x_coord))
y_grid = np.linspace(0, max(y_coord), 4 * len(y_coord))
X, Y = np.meshgrid(x_grid, y_grid, indexing="xy")

# Render X amplitude interpolated curve:
x_plt = fig.add_subplot(121, projection="3d")
x_plt.scatter3D(x_coord, y_coord, x_ampl, c="r")
Z = func((X, Y), *x_popt)
x_plt.plot_wireframe(X, Y, Z, alpha=0.2)
x_plt.plot_surface(X, Y, Z, alpha=0.2)

# Render Y amplitude interpolated curve:
y_plt = fig.add_subplot(122, projection="3d")
y_plt.scatter3D(x_coord, y_coord, y_ampl, c="r")
Z = func((X, Y), *y_popt)
y_plt.plot_wireframe(X, Y, Z, alpha=0.2)
y_plt.plot_surface(X, Y, Z, alpha=0.2)

fig.show()
plt.show()
