from abc import ABC, abstractmethod
from src.dataTypes.Audio import Audio


class IRemoveRedundancy(ABC):
    @abstractmethod
    def remove_redundancy(self, audio: Audio) -> Audio:
        """ Remove redundancies from the passed audio and return a reference to this original audio """
        pass