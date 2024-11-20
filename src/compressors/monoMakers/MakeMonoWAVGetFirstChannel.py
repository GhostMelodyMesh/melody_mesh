from src.compressors.monoMakers.IMakeMono import IMakeMono
from src.dataTypes.AudioWAV import AudioWAV


class MakeMonoWAVGetFirstChannel(IMakeMono):
    def make_mono(self, audio: AudioWAV) -> AudioWAV:
        """ Remove all channels except the first one """
        audio.audio = audio.audio[:, 0:1]
        audio.n_channels = 1
        
        return audio