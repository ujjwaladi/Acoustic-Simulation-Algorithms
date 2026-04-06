import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import sounddevice as sd
from scipy.fft import rfft, rfftfreq


# audio stream config
sample_rate = 44100
chunk_size  = 1024      # samples per grab
channels    = 1         # keep it mono
duration    = 5.0       # capture time

audio_buffer = []

# defaults for the animation (will be overwritten by live data)
top_freqs = [261.63, 329.63, 392.0]
amps      = [1.0, 0.8, 0.7]

def audio_callback(indata, frames, time_info, status):
    # runs in background thread, catching new audio samples
    global audio_buffer
    audio_buffer.extend(indata[:, 0])

# start the mic
stream = sd.InputStream(
    samplerate=sample_rate,
    channels=channels,
    blocksize=chunk_size,
    callback=audio_callback
)

fig = plt.figure(figsize=(10, 8))

# top plot: raw waveform
ax_time = fig.add_subplot(2, 1, 1)
line_time, = ax_time.plot([], [], lw=1.5, color='blue')
ax_time.set_title("Time-Domain Waveform (Most Recent Chunk)")
ax_time.set_xlabel("Time (s)")
ax_time.set_ylabel("Amplitude")
ax_time.set_xlim(0, chunk_size / sample_rate)
ax_time.set_ylim(-1.0, 1.0)
ax_time.grid(True)

# bottom plot: live lissajous
ax_3d = fig.add_subplot(2, 1, 2, projection='3d')
line_3d, = ax_3d.plot([], [], [], lw=2, color='red')
ax_3d.set_xlim([-1, 1])
ax_3d.set_ylim([-1, 1])
ax_3d.set_zlim([-1, 1])
ax_3d.set_xlabel("Freq 1")
ax_3d.set_ylabel("Freq 2")
ax_3d.set_zlabel("Freq 3")
ax_3d.set_title("Real-time 3D Lissajous from Audio FFT")

# static time array to draw the parametric shape
t_param = np.linspace(0, 0.02, 500)

def update(frame):
    global top_freqs, amps, audio_buffer

    # wait until we actually have enough data to process
    if len(audio_buffer) < chunk_size:
        return line_time, line_3d

    # grab the newest chunk
    recent_data = np.array(audio_buffer[-chunk_size:], dtype=np.float32)

    # plot the raw wave
    t_chunk = np.linspace(0, chunk_size/sample_rate, chunk_size, endpoint=False)
    line_time.set_data(t_chunk, recent_data)

    # run the FFT on the chunk
    fft_vals = rfft(recent_data)
    freqs    = rfftfreq(chunk_size, 1/sample_rate)
    magnitudes = np.abs(fft_vals)

    # grab top 3 frequencies (ignoring DC offset at index 0)
    idx = np.argsort(magnitudes[1:])[-3:] + 1
    top_freqs = freqs[idx]
    top_mags  = magnitudes[idx]

    # normalize so it fits nicely in the 3D box
    max_mag = np.max(top_mags)
    amps    = top_mags / max_mag if max_mag > 0 else [1, 1, 1]

    # calculate the live shape
    x = amps[0] * np.sin(2 * np.pi * top_freqs[0] * t_param)
    y = amps[1] * np.sin(2 * np.pi * top_freqs[1] * t_param + np.pi/2)
    z = amps[2] * np.sin(2 * np.pi * top_freqs[2] * t_param + np.pi)

    line_3d.set_data(x, y)
    line_3d.set_3d_properties(z)

    return line_time, line_3d

stream.start()

ani = FuncAnimation(fig, update, frames=int(duration * 100), interval=50, blit=True)

plt.tight_layout()
plt.show()

# cleanup after we close the window
stream.stop()
stream.close()