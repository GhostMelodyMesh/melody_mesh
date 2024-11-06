from typing import Union
import numpy as np
from src.dataTypes.Audio import Audio


class AudioWAV(Audio):
    def __init__(self, n_samples: int, n_channels: int):
        super().__init__()
        self._n_samples = n_samples
        self._n_channels = n_channels
        
    @property
    def n_samples(self):
        return self._n_samples
    
    @n_samples.setter
    def n_samples(self, n_samples):
        self._n_samples = n_samples
        
    @property
    def n_channels(self):
        return self._n_channels
    
    @n_channels.setter
    def n_channels(self, n_channels):
        self._n_channels = n_channels
        