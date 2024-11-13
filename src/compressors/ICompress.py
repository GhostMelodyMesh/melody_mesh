from abc import ABC, abstractmethod


class ICompress(ABC):
    @abstractmethod
    def compress(self, file_path: str) -> str:
        """ Get a file path and save it in /compressedAudio, returns compressed file path """
        pass