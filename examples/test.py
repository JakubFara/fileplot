import numpy as np
import matplotlib.pyplot as plt

# Create a figure of size 8x6 inches, 80 dots per inch
plt.figure(figsize=(8, 6), dpi=80)

# Create a new subplot from a grid of 1x1
plt.subplot(1, 1, 1)

X = np.linspace(-np.pi, np.pi, 256)
C = np.cos(X)
t = 2 * np.pi / 3


plt.plot([t, t], [0, np.cos(t)], color="blue", linewidth=2.5, linestyle="--")


plt.plot(X, C)

plt.show()
