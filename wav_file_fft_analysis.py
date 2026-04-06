import matplotlib
matplotlib.use('TkAgg')
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.fft import fft, fftfreq
from scipy.signal import find_peaks


wav_file = "Cmaj.wav" # the audio file(feed location based on your audio file)
sample_rate, data = wavfile.read(wav_file)

# reduce to mono if the recording is stereo
if data.ndim == 2:
    data = data.mean(axis=1)

print(f"Loaded '{wav_file}'. Sample Rate: {sample_rate} Hz, Data Shape: {data.shape}")

# fourier transform
N = len(data)
fft_values = fft(data)
freqs = fftfreq(N, 1 / sample_rate)

# positive frequencies
half_N = N // 2
positive_freqs = freqs[:half_N]
positive_magnitude = np.abs(fft_values[:half_N])

#  background noise filtering by setting a height threshold
peaks, properties = find_peaks(positive_magnitude, height=100)
peak_freqs = positive_freqs[peaks]
peak_vals  = positive_magnitude[peaks]

# detect top 3 highest amplitude frequencies (the fundamental notes, C E G for Cmaj Chord )
sorted_indices = np.argsort(-peak_vals)
top_3_indices = sorted_indices[:3]

print("\nTop 3 Peak Frequencies (highest amplitude):")
for i, idx in enumerate(top_3_indices, start=1):
    print(f"{i}. Frequency = {peak_freqs[idx]:.2f} Hz, Amplitude = {peak_vals[idx]:.1f}")

# plot everything
plt.figure(figsize=(10, 5))
plt.plot(positive_freqs, positive_magnitude, label="Spectrum")
plt.plot(peak_freqs, peak_vals, 'rx', label="Detected Peaks")

# top 3 peaks on the graph
for idx in top_3_indices:
    plt.annotate(f"{peak_freqs[idx]:.1f} Hz",
                 (peak_freqs[idx], peak_vals[idx]),
                 textcoords="offset points", xytext=(0,10),
                 ha='center', color='red')

plt.title("Fourier Transform of WAV File")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Magnitude")
plt.xlim(0, 1000)
plt.grid(True)
plt.legend()
plt.show()