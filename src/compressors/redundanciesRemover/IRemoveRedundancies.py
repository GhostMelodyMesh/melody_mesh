from abc import ABC, abstractmethod
from src.dataTypes.Audio import Audio


class IRemoveRedundancies(ABC):
    def __init__(self):
        super().__init__()
        
    @abstractmethod
    def remove_redundancies(self, audio: Audio) -> Audio:
        """ Remove redundancies from the passed audio and return a reference to this original audio """
        pass