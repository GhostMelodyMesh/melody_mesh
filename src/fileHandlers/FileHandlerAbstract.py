from abc import ABC, abstractmethod


class FileHandlerAbstract(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self):
        pass

