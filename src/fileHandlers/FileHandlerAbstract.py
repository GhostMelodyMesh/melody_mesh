from abc import ABC, abstractmethod
from typing import TypeVar, Generic

T = TypeVar('T')


class FileHandlerAbstract(ABC, Generic[T]):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def read(self, file_path: str) -> T:
        pass

    @abstractmethod
    def write(self, obj: T, file_path: str):
        pass
