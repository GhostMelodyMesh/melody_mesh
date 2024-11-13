from abc import ABC, abstractmethod
from typing import TypeVar, Generic
import re

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

    @staticmethod
    def _get_extension(file_path: str) -> str:
        extension = re.search(r'\.(\w+)$', file_path).group(1)
        return extension
