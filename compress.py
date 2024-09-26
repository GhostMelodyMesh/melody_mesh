import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
from scipy.io import wavfile


def stereo_to_mono(audio_data: np.ndarray) -> np.ndarray:
    """
    Convert stereo audio data to mono audio data.
    """
    if audio_data.ndim == 1:
        return audio_data
    
    return np.mean(audio_data, axis=1).astype(np.int16)

def reduce_sample_rate(audio_data: np.ndarray, sample_rate: int, new_sample_rate: int) -> np.ndarray:
    """
    Reduce the sample rate of the audio data to the given sample rate.
    """
    if (new_sample_rate > sample_rate):
        raise ValueError("The new sample rate must be less than the original sample rate.")
    
    # Calculate new length of the audio data
    new_length = int(len(audio_data) * new_sample_rate / sample_rate)
    compressed = scipy.signal.resample(audio_data, new_length).astype(np.int16)
    
    return compressed

def save_audio_data(filename: str, sample_rate: int, audio_data: np.ndarray):
    """
    Save the audio data to a WAV file.
    """
    wavfile.write(filename, sample_rate, audio_data)
    
def NCC(x: np.ndarray, y: np.ndarray) -> int:
    """
    Calculate the normalized cross-correlation between two signals.
    """
    if np.std(x) == 0 or np.std(y) == 0:
        return np.nan

    x_normalized = (x - np.mean(x)) / np.std(x)
    y_normalized = (y - np.mean(y)) / np.std(y)
    
    cross_correlation = np.correlate(y_normalized, x_normalized, mode='valid')
    
    cross_correlation /= np.sqrt(np.sum(x_normalized**2) * np.sum(y_normalized**2))
    
    return cross_correlation

STARING_PRECISION = 50
PRECISION_REDUCTION = 5
SAMPLE_RATE = 4410
SEGMENT_LENGTH_SECONDS = 1

# Load the data
sample_rate_full, audio_data_full = wavfile.read('full-clip.wav')
# sample_rate_partial, audio_data_partial = wavfile.read('part.wav')

compressed_full = reduce_sample_rate(stereo_to_mono(audio_data_full), sample_rate_full, SAMPLE_RATE)

# Get a random segment of the full audio data
partial_length = SEGMENT_LENGTH_SECONDS * SAMPLE_RATE
starting_time = np.random.randint(0, len(compressed_full) - partial_length)
compressed_partial = compressed_full[starting_time:starting_time + partial_length]

# Remove the partial audio data from the full audio data
compressed_full = np.concatenate((compressed_full[:starting_time], compressed_full[starting_time + partial_length:]))

precision = STARING_PRECISION
similarities = []
offset = 0
while offset < len(compressed_full) - len(compressed_partial):
    segment = compressed_full[offset:offset+len(compressed_partial)]
    similarity = NCC(segment, compressed_partial)
    similarities.append(similarity)
    offset += precision
best_match_index = np.argmax(similarities)
offset = best_match_index * precision
print("precision", precision)
print("offset", offset)

while precision > 1:
    left = max(0, offset - precision)
    right = min(len(compressed_full) - len(compressed_partial), offset + precision)
    if (PRECISION_REDUCTION > precision):
        precision = 1
    else:
        precision //= PRECISION_REDUCTION
    similarities = []
    offset = left
    while offset < right:
        segment = compressed_full[offset:offset+len(compressed_partial)]
        similarity = NCC(segment, compressed_partial)
        similarities.append(similarity)
        offset += precision
    best_match_index = np.argmax(similarities)
    offset = left + best_match_index * precision
    print("precision", precision)
    print("offset", offset)

# Plot the compressed audio data
plt.plot(compressed_full)
augumented = np.concatenate((np.zeros(offset), compressed_partial))
plt.plot(augumented, alpha=0.5)
plt.show()