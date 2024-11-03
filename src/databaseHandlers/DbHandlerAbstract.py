from abc import ABC, abstractmethod


class DbHandlerAbstract(ABC):
    def __init__(self):
        """ Create a DbProxy and connect to database """
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def write(self):
        pass

    @abstractmethod
    def delete(self):
        pass
