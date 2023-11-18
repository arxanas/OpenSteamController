import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

# (x_coord, y_coord, x_ampl, y_ampl)
data_lines = """
  0	350	1053	668
300	175	2009	1789
300	350	2403	1748
300	525	1782	986
600	0	572	2028
600	175	1927	2400
600	350	2476	2644
600	525	1699	2748
600	700	1242	3066
900	175	2312	1956
900	350	3034	2306
900	525	2332	2094
1120	350	1875	3008
""".strip().split("\n")
data = np.array([[int(x) for x in line.split()] for line in data_lines if not line.startswith("#")])
x_coord = data[:, 0]
y_coord = data[:, 1]
x_ampl = data[:, 2]
y_ampl = data[:, 3]


# See https://www.geeksforgeeks.org/3d-curve-fitting-with-python/
def func(xy, a, b, c, d, e, f):
    x, y = xy
    return a + (b * x) + (c * y) + (d * x**2) + (e * y**2) + (f * x * y)


(x_popt, x_pcov) = sp.optimize.curve_fit(func, (x_coord, y_coord), x_ampl)
x_errs = [abs(x_ampl[i] - func((x_coord[i], y_coord[i]), *x_popt)) for i in range(len(x_coord))]
print("x errs:", x_errs)
print("Max x-err", max(x_errs))
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
