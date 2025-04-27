# cassave/encoder.py

import numpy as np
from scipy.io.wavfile import write as write_wav

# Constants
SAMPLE_RATE = 44100  # Hz
DURATION_PER_CHUNK = 0.003  # seconds
AMPLITUDE = 0.5

BASE_FREQ = 800  # Hz
FREQ_STEP = 400  # Hz
NUM_BITS = 8     # bits per chunk

def generate_sine_wave(frequency, duration, sample_rate, amplitude=1.0):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return wave

def encode_byte(byte_val):
    """
    Encodes one byte into 8 tones using differential Manchester encoding.
    """
    freqs = []
    # Build the list of frequencies for each bit
    for i in range(NUM_BITS):
        bit = (byte_val >> i) & 0x1  # get bit i (little endian bit order)
        freq = BASE_FREQ + i * FREQ_STEP
        freqs.append((bit, freq))
    
    # Generate the combined waveform
    t = np.linspace(0, DURATION_PER_CHUNK, int(SAMPLE_RATE * DURATION_PER_CHUNK), endpoint=False)
    signal = np.zeros_like(t)
    
    for bit, freq in freqs:
        if bit == 1:
            # No transition at start → positive sine
            wave = generate_sine_wave(freq, DURATION_PER_CHUNK, SAMPLE_RATE, AMPLITUDE)
        else:
            # Transition at start → flip phase
            wave = generate_sine_wave(freq, DURATION_PER_CHUNK, SAMPLE_RATE, -AMPLITUDE)
        signal += wave
    
    # Normalize slightly to avoid any clipping if multiple tones align
    signal /= NUM_BITS
    return signal

def encode_file(input_bytes: bytes):
    """
    Encodes a whole file into an audio waveform.
    """
    full_signal = []
    for byte in input_bytes:
        encoded_chunk = encode_byte(byte)
        full_signal.append(encoded_chunk)
    
    # Flatten into one big array
    return np.concatenate(full_signal)

def save_wav(filename: str, samples: np.ndarray):
    """
    Saves the generated samples to a WAV file.
    """
    # Scale to int16 range
    samples_int16 = np.int16(samples * 32767)
    write_wav(filename, SAMPLE_RATE, samples_int16)

