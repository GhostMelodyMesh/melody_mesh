from abc import ABC, abstractmethod
from src.dataTypes.Audio import Audio


class ITrim(ABC):
    def __init__(self):
        super().__init__()
        
    @abstractmethod
    def trim(self, audio: Audio) -> Audio:
        """ Trim the passed audio and return a reference to this original audio """
        pass