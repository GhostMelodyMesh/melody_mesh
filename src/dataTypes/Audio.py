from abc import ABC, abstractmethod


class Audio(ABC):
    """ Abstract class for audio data """
    def __init__(self, audio=None, format=None, sample_rate=None):
        self._audio = audio
        self._format: str = format
        self._sample_rate: int = sample_rate
    
    @property
    def audio(self):
        return self._audio
    
    @audio.setter
    def audio(self, audio):
        self._audio = audio
    
    @property
    def format(self):
        return self._format
    
    @format.setter
    def format(self, format):
        self._format = format
        
    @property
    def sample_rate(self):
        return self._sample_rate
    
    @sample_rate.setter
    def sample_rate(self, sample_rate):
        self._sample_rate = sample_rate
