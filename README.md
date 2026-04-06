# Acoustic Simulation and Algorithm Development

This repository contains Python-based digital signal processing (DSP) algorithms developed to model, analyze, and visualize acoustic features, with a focus on frequency decomposition and real-time audio processing.

## Core Features & Scripts

* **`wav_file_fft_analysis.py`**: Utilizes Fast Fourier Transform (FFT) via `scipy.fft` to process complex audio files (e.g., guitar chords), isolating and identifying the constituent peak frequencies. 
* **`realtime_audio_fft_visualizer.py`**: A low-latency embedded application using `sounddevice` to capture real-time audio chunks, compute live FFTs, and map the top harmonic frequencies to a 3D Lissajous curve dynamically.
* **`3d_chord_lissajous_sim.py`**: Models the phase and frequency relationships of multi-frequency audio (C Major Chord) by summing waveforms in the time domain and visualizing their harmonic ratios as parametric 3D Lissajous curves.
* **`2d_lissajous_kinematics.py`**: Simulates and animates the foundational kinematics of orthogonal sinusoidal waves and their resulting phase shifts.

## Technologies Used
* **Languages:** Python
* **Libraries:** NumPy, SciPy (Signal Processing, FFT), Matplotlib (2D/3D Animation), Sounddevice (Real-time Audio I/O).
