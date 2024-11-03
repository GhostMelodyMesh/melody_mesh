from abc import ABC, abstractmethod


class CompressorAbstract(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def compress(self, file_path: str) -> str:
        """ Remove redundant parts from an audio file, lower its quality and save the compressed file to compressedData """
        # fHandler = AudioFileHandler()
        # file, format = fHandler.read(file_path)
        # compressed_file = self.lower_quality(compressed_file)
        # compressed_file = self.remove_redundancy(file)
        # fHandler.write(compressed_file, format)
        pass

    @abstractmethod
    def remove_redundancies(self, file):
        pass

    @abstractmethod
    def remove_redundancy(self, file):
        pass

    @abstractmethod
    def group_redundancies(self, file):
        pass

    @abstractmethod
    def lower_quality(self, file, quality):
        pass
