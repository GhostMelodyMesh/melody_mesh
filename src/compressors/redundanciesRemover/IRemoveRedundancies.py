from abc import ABC, abstractmethod
from src.dataTypes.Audio import Audio


class IRemoveRedundancies(ABC):        
    @abstractmethod
    def remove_redundancies(self, audio: Audio) -> Audio:
        """ Remove redundancies from the passed audio and return a reference to this original audio """
        pass