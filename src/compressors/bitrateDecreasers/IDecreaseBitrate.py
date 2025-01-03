from abc import ABC, abstractmethod
from src.dataTypes.Audio import Audio


class IDecreaseBitrate(ABC):        
    @abstractmethod
    def decrease_bitrate(self, audio: Audio, new_sample_rate: int) -> Audio:
        """ Decrease the bitrate of the passed audio and return a reference to this original audio """
        pass