import os
from src.dataTypes.Audio import Audio
from src.dataTypes.AudioWAV import AudioWAV
from src.fileHandlers.FileHandlerAbstract import FileHandlerAbstract
from src.fileHandlers.AudioWAVFileHandler import AudioWAVFileHandler


class AudioFileHandler(FileHandlerAbstract):
    """ Handling of local audio files, reading different file formats, converting them into normalised format, saving them """

    def __init__(self):
        super().__init__()
        pass

    def read(self, file_path: str) -> Audio:

        if not os.path.exists(file_path):
            raise FileNotFoundError("File not found")

        match self._get_extension(file_path):
            case "wav":
                return AudioWAVFileHandler().read(file_path)
            case "mp3":
                raise ValueError("mp3 format not supported")
            case _:
                raise ValueError("File format not supported")

    def write(self, audio: Audio, file_path: str):
        """ Write an Audio object to a file, file_path must include the file extension """
        match self._get_extension(file_path):
            case "wav":
                if isinstance(audio, AudioWAV):
                    AudioWAVFileHandler().write(audio, file_path)
                else:
                    raise ValueError("Wrong audio extension pair")
            case "mp3":
                raise ValueError("mp3 format not supported")
            case _:
                raise ValueError("File format not supported")
