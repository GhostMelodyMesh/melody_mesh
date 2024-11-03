from abc import ABC, abstractmethod
from dataTypes.Audio import Audio


class CompressorAbstract(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def compress(self, file_path: str) -> str:
        """ Remove redundant parts from an audio file, lower its quality and save the compressed file to compressedData, returns the path to the compressed file """
        # fHandler = AudioFileHandler()
        # file, format = fHandler.read(file_path)
        # compressed_file = self.lower_quality(compressed_file)
        # compressed_file = self.remove_redundancy(file)
        # fHandler.write(compressed_file, format)
        pass

    @abstractmethod
    def remove_redundancies(self, file: Audio) -> Audio:
        """ Select one interval from each group of redundant parts to keep """
        pass

    @abstractmethod
    def select_from_redundancy_group(self, file: Audio, group: list[tuple[int, int]]) -> tuple[int, int]:
        """ Remove redundant parts from an audio file, select one interval from each group to keep """
        pass

    @abstractmethod
    def group_redundancies(self, file: Audio) -> list[list[tuple[int, int]]]:
        """ Group redundant parts of an audio file, returns a list of tuples with start and end of each group """
        pass

    @abstractmethod
    def lower_quality(self, file: Audio, sample_rate: int) -> Audio:
        """ Lower the quality of an audio file """
        pass
