from abc import ABC, abstractmethod

class Audio(ABC):
    """ Abstract class for audio data """
    def __init__(self):
        pass

    @abstractmethod
    def get_audio(self):
        """ Return the audio data """
        pass

    @abstractmethod
    def get_format(self) -> str:
        """ Return the format of the audio data """
        pass

    @abstractmethod
    def set_audio(self, audio: str):
        """ Set the audio data """
        pass

    @abstractmethod
    def set_format(self, format: str):
        """ Set the format of the audio data """
        pass