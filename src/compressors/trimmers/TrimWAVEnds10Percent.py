import numpy as np
from src.compressors.trimmers.ITrim import ITrim
from src.dataTypes.AudioWAV import AudioWAV


class TrimWAVEnds10Percent(ITrim):
    def trim(self, audio: AudioWAV) -> AudioWAV:
        """ Remove 10% of the audio from the beginning and the end, [AddTest] """
        start, end = int(audio.n_samples * 0.1), int(audio.n_samples * 0.9)
        audio.audio = audio.audio[start:end, :]
        audio.n_samples = end - start
        
        return audio
