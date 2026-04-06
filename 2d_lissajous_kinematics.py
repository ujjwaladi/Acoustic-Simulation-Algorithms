import matplotlib
matplotlib.use('QtAgg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# tweak frequencies for better understanding of parametrisation
a, b = 10, 10
delta = np.pi/2   # phase shift
A, B = 1.0, 1  # amplitudes
L = 1000          # frames
t = np.linspace(0, 2 * np.pi, L)

x = A * np.sin(a * t)
y = B * np.sin(b * t + delta)

fig = plt.figure(figsize=(8, 8))

# the lissajous plot
ax_lissajous = fig.add_axes([0.2, 0.3, 0.6, 0.6])
line_lissajous, = ax_lissajous.plot([], [], lw=2, color='purple')
point_lissajous, = ax_lissajous.plot([], [], 'ro')
ax_lissajous.set_xlim(-1.2, 1.2)
ax_lissajous.set_ylim(-1.2, 1.2)
ax_lissajous.set_title("Lissajous Curve")
ax_lissajous.grid(True)

# x(t) wave aligned underneath
ax_x = fig.add_axes([0.2, 0.1, 0.6, 0.15])
line_x, = ax_x.plot([], [], lw=2, color='blue')
point_x, = ax_x.plot([], [], 'ro')
ax_x.set_xlim(0, 2 * np.pi)
ax_x.set_ylim(-1.2, 1.2)
ax_x.set_title("x(t) = sin(3t)")
ax_x.set_xlabel("Time (t)")
ax_x.grid(True)

# y(t) wave aligned to the left
ax_y = fig.add_axes([0.05, 0.3, 0.15, 0.6])
line_y, = ax_y.plot([], [], lw=2, color='green')
point_y, = ax_y.plot([], [], 'ro')
ax_y.set_xlim(-1.2, 1.2)
ax_y.set_ylim(0, 2 * np.pi)
ax_y.set_title("y(t) = sin(4t + π/2)")
ax_y.set_ylabel("Time (t)")
ax_y.grid(True)

# visual trackers
h_line, = ax_lissajous.plot([], [], 'k--', lw=1)
v_line, = ax_lissajous.plot([], [], 'k--', lw=1)

def update(frame):
    # to prevent indexing errors on frame 0
    if frame <= 0:
        line_x.set_data([], [])
        point_x.set_data([], [])
        line_y.set_data([], [])
        point_y.set_data([], [])
        line_lissajous.set_data([], [])
        point_lissajous.set_data([], [])
        h_line.set_data([], [])
        v_line.set_data([], [])
        return line_x, point_x, line_y, point_y, line_lissajous, point_lissajous, h_line, v_line

    # update standard waveforms
    line_x.set_data(t[:frame], x[:frame])
    point_x.set_data([t[frame - 1]], [x[frame - 1]])

    line_y.set_data(y[:frame], t[:frame])
    point_y.set_data([y[frame - 1]], [t[frame - 1]])

    # update lissajous
    line_lissajous.set_data(x[:frame], y[:frame])
    point_lissajous.set_data([x[frame - 1]], [y[frame - 1]])

    # update connecting trackers
    h_line.set_data([x[frame - 1], x[frame - 1]], [-1.2, y[frame - 1]])
    v_line.set_data([-1.2, x[frame - 1]], [y[frame - 1], y[frame - 1]])

    return line_x, point_x, line_y, point_y, line_lissajous, point_lissajous, h_line, v_line

ani = FuncAnimation(fig, update, frames=L, interval=20, blit=True)
plt.show()