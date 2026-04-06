import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# base frequencies for C Major
fC = 261.63
fE = 329.63
fG = 392.00

# tweak these if you want a note to hit harder
AC = 1.0
AE = 0.8
AG = 0.7

# phase offsets to give the lissajous some volume
phiC = 0
phiE = np.pi / 2
phiG = np.pi

# ~0.05 seconds of time base
t_base = np.linspace(0, 0.05, 1000)

def chord_wave(t):
    # summing the individual notes into one complex waveform
    wave_c = AC * np.sin(2 * np.pi * fC * t + phiC)
    wave_e = AE * np.sin(2 * np.pi * fE * t + phiE)
    wave_g = AG * np.sin(2 * np.pi * fG * t + phiG)
    return wave_c + wave_e + wave_g

# parametric functions for the 3D axes
def x_func(t):
    return AC * np.sin(2 * np.pi * fC * t + phiC)

def y_func(t):
    return AE * np.sin(2 * np.pi * fE * t + phiE)

def z_func(t):
    return AG * np.sin(2 * np.pi * fG * t + phiG)

fig = plt.figure(figsize=(12, 5))

# 2D time-domain plot
ax_time = fig.add_subplot(1, 2, 1)
line_time, = ax_time.plot([], [], lw=2, color='blue')
ax_time.set_title("Time-Domain Waveform: C + E + G")
ax_time.set_xlabel("Time (s)")
ax_time.set_ylabel("Amplitude")
ax_time.set_xlim(0, 0.05)
ax_time.set_ylim(-3, 3)
ax_time.grid(True)

# 3D plot
ax_3d = fig.add_subplot(1, 2, 2, projection='3d')
line_3d, = ax_3d.plot([], [], [], lw=2, color='purple')
ax_3d.set_xlim((-1.2, 1.2))
ax_3d.set_ylim((-1.2, 1.2))
ax_3d.set_zlim((-1.2, 1.2))
ax_3d.set_xlabel(f"C = {fC:.1f} Hz")
ax_3d.set_ylabel(f"E = {fE:.1f} Hz")
ax_3d.set_zlabel(f"G = {fG:.1f} Hz")
ax_3d.set_title("3D Lissajous (C Major Chord)")

plt.tight_layout()

def update(frame):
    # time arry shift for motion
    shift = frame * 0.0005
    t_shifted = t_base + shift

    # update 2D wave
    wave_vals = chord_wave(t_shifted)
    line_time.set_data(t_base, wave_vals)

    # update 3D curve
    x_vals = x_func(t_shifted)
    y_vals = y_func(t_shifted)
    z_vals = z_func(t_shifted)

    line_3d.set_data(x_vals, y_vals)
    line_3d.set_3d_properties(z_vals)

    return line_time, line_3d

ani = FuncAnimation(fig, update, frames=200, interval=50, blit=True)
plt.show()