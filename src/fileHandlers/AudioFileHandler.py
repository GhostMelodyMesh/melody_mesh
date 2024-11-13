import os
from src.dataTypes.Audio import Audio
from src.dataTypes.AudioWAV import AudioWAV
from src.fileHandlers.AudioWAVFileProcessor import AudioWAVFileProcessor
from src.utilities.get_extension import get_extension


class AudioFileHandler:
    """ Handling of local audio files, reading different file formats, converting them into normalised format, saving them """

    def __init__(self):
        pass

    @staticmethod
    def read(file_path: str) -> Audio:
        """ Read an audio file from a file path, file_path must include the file extension """
        if not os.path.exists(file_path):
            raise FileNotFoundError("File not found")

        match get_extension(file_path):
            case "wav":
                return AudioWAVFileProcessor().read(file_path)
            case "mp3":
                raise ValueError("mp3 format not supported")
            case _:
                raise ValueError("File format not supported")

    @staticmethod
    def write(audio: Audio, file_path: str):
        """ Write an Audio object to a file, file_path must include the file extension """
        match get_extension(file_path):
            case "wav":
                if isinstance(audio, AudioWAV):
                    AudioWAVFileProcessor().write(audio, file_path)
                else:
                    raise ValueError("Wrong audio extension pair")
            case "mp3":
                raise ValueError("mp3 format not supported")
            case _:
                raise ValueError("File format not supported")
