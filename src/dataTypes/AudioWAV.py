from typing import Union
import numpy as np
from src.dataTypes.Audio import Audio


class AudioWAV(Audio):
    def __init__(self):
        super().__init__()
        self._sample_rate: Union[int, None] = None
        
    @property
    def sample_rate(self):
        return self._sample_rate
    
    @sample_rate.setter
    def sample_rate(self, sample_rate):
        self._sample_rate = sample_rate
