from scipy.interpolate import interp1d
import numpy as np

a = np.array([[1, -0.08, -0.16], [1, -0.08, -0.08], [1, 0.03, 0.34], [1, -0.16, -0.08]])

x = np.array(range(a.shape[0]))

# define new x range, we need 7 equally spaced values
xnew = np.linspace(3)

# apply the interpolation to each column
f = interp1d(x, a, axis=0)

print(f)

# get final result
print(f(xnew))