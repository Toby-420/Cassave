# cassave/decoder.py

import numpy as np
from scipy.io import wavfile

# Constants
SAMPLE_RATE = 44100  # Hz
DURATION_PER_CHUNK = 0.8  # seconds
AMPLITUDE_THRESHOLD = 0.05  # Amplitude threshold to detect tones

BASE_FREQ = 800  # Hz
FREQ_STEP = 400  # Hz
NUM_BITS = 8     # bits per chunk

def decode_chunk(chunk):
    """
    Decodes a single audio chunk into a byte.
    """
    bits = []
    t = np.linspace(0, DURATION_PER_CHUNK, int(SAMPLE_RATE * DURATION_PER_CHUNK), endpoint=False)
    
    for i in range(NUM_BITS):
        freq = BASE_FREQ + i * FREQ_STEP
        sine_wave = np.sin(2 * np.pi * freq * t)
        
        # Correlate to see if the tone matches
        correlation = np.dot(chunk, sine_wave)
        
        # Decide bit based on phase
        if correlation > 0:
            bits.append(1)
        else:
            bits.append(0)
    
    # Little-endian
    value = 0
    for i, bit in enumerate(bits):
        value |= (bit << i)
    
    return value

def decode_file(wav_filename: str):
    """
    Decodes a WAV file into raw bytes.
    """
    sample_rate, samples = wavfile.read(wav_filename)
    
    if sample_rate != SAMPLE_RATE:
        raise ValueError(f"Expected sample rate {SAMPLE_RATE}, got {sample_rate}")

    # Normalize if needed (e.g., if 16-bit integers)
    if samples.dtype == np.int16:
        samples = samples.astype(np.float32) / 32767.0

    chunk_size = int(SAMPLE_RATE * DURATION_PER_CHUNK)
    num_chunks = len(samples) // chunk_size

    output_bytes = bytearray()

    for i in range(num_chunks):
        chunk = samples[i * chunk_size : (i + 1) * chunk_size]
        if len(chunk) == chunk_size:
            byte_val = decode_chunk(chunk)
            output_bytes.append(byte_val)
    
    return bytes(output_bytes)
