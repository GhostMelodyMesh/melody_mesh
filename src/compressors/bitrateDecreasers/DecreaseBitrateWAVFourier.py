import scipy.signal
from src.compressors.bitrateDecreasers.IDecreaseBitrate import IDecreaseBitrate
from src.dataTypes.AudioWAV import AudioWAV


class DecreaseBitrateWAVFourier(IDecreaseBitrate):
    def decrease_bitrate(self, audio: AudioWAV, new_sample_rate: int = 4410) -> AudioWAV:
        """ Decrease the bitrate of the passed audio using Fourier transform, [AddTest] """
        
        if (new_sample_rate > audio.sample_rate):
            raise ValueError("The new sample rate must be less than the original sample rate.")
        
        # Reduce the number of samples in the audio file to keep the same duration
        new_n_samples = int(audio.n_samples * new_sample_rate / audio.sample_rate)
        new_audio = scipy.signal.resample(audio.audio, new_n_samples)
        
        audio.audio = new_audio
        audio.sample_rate = new_sample_rate
        audio.n_samples = new_n_samples
        
        return audio
    