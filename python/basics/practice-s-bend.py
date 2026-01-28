# S-bend (SiN waveguide) — cubic Bézier 2-segment example
import numpy as np
import matplotlib.pyplot as plt

print("matplotlib works 🎉")

# Segment 1 control points (P0..P3)
P0 = np.array([0.0, 0.0])
P1 = np.array([2.0, 0.0])
P2 = np.array([3.0, 1.5])
P3 = np.array([5.0, 1.0])  # mid point

# Segment 2 control points (Q0..Q3)
Q0 = P3
Q1 = np.array([7.0, 0.5])
Q2 = np.array([8.0, 2.5])
Q3 = np.array([10.0, 2.0])

def cubic_bezier(A, B, C, D, n=300):
    t = np.linspace(0, 1, n)
    return (
        ((1 - t)**3)[:, None] * A +
        (3 * ((1 - t)**2 * t))[:, None] * B +
        (3 * ((1 - t) * t**2))[:, None] * C +
        (t**3)[:, None] * D
    )

c1 = cubic_bezier(P0, P1, P2, P3, n=200)
c2 = cubic_bezier(Q0, Q1, Q2, Q3, n=200)
curve = np.vstack([c1, c2[1:]])  # join without duplicating the midpoint

# Plot: thick centerline as waveguide, plus control polygons/points
plt.figure(figsize=(8, 3.5))
plt.plot(curve[:, 0], curve[:, 1], linewidth=6)  # thick centerline = waveguide
plt.plot([P0[0], P1[0], P2[0], P3[0]], [P0[1], P1[1], P2[1], P3[1]], linestyle='--', marker='o', markersize=4)
plt.plot([Q0[0], Q1[0], Q2[0], Q3[0]], [Q0[1], Q1[1], Q2[1], Q3[1]], linestyle='--', marker='o', markersize=4)

plt.scatter([P0[0], Q3[0]], [P0[1], Q3[1]], zorder=5)
plt.text(P0[0], P0[1]-0.2, "input", va='top')
plt.text(Q3[0], Q3[1]+0.2, "output", va='bottom')

plt.title("S-bend for SiN waveguide (cubic Bézier segments)")
plt.xlabel("x (µm)")
plt.ylabel("y (µm)")
plt.axis('equal')
plt.grid(True)
plt.tight_layout()
plt.show()

