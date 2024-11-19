from abc import ABC, abstractmethod
from src.dataTypes.Audio import Audio


class IMakeMono(ABC):        
    @abstractmethod
    def make_mono(self, audio: Audio) -> Audio:
        """ Change the passed audio to mono and return a reference to this original audio """
        pass