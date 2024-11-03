import numpy as np
from dataTypes import Audio


class AudioWAV(Audio):
    def __init__(self):
        super().__init__()
        pass
    
    # TODO: define attributes
    
    def get_audio(self) -> np.ndarray:
        """ Return the audio data """
        pass

    def get_format(self) -> str:
        """ Return the format of the audio data """
        pass

    def set_audio(self, audio: str):
        """ Set the audio data """
        pass

    def set_format(self, format: str):
        """ Set the format of the audio data """
        pass