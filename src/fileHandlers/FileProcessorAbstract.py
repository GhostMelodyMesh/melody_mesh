from abc import ABC, abstractmethod
from typing import TypeVar, Generic
import re

T = TypeVar('T')


class FileProcessorAbstract(ABC, Generic[T]):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def read(self, file_path: str) -> T:
        pass

    @abstractmethod
    def write(self, obj: T, file_path: str):
        pass
