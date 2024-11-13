from src.dataTypes.AudioWAV import AudioWAV
from src.fileHandlers.FileHandlerAbstract import FileHandlerAbstract
from scipy.io import wavfile
import numpy as np


class AudioWAVFileHandler(FileHandlerAbstract):
    def __init__(self):
        pass

    def read(self, file_path: str):
        """ Read an audio file as a .wav file with normalised audio data in range (-1, 1) of type float32 """
        sample_rate, audio = wavfile.read(file_path)
        data_number_type = audio.dtype

        match data_number_type:
            case 'float32':
                audio = audio
            case 'int32':
                audio = audio / 2 ** 31
            case 'int16':
                audio = audio / 2 ** 15
            case 'uint8':
                audio = (audio - 128) / 128
            case _:
                raise ValueError("Data type not supported")

        audio = audio.astype(np.float32)

        n_samples, n_channels = audio.shape

        audioWAV = AudioWAV(audio=audio, format='wav', sample_rate=sample_rate, n_samples=n_samples,
                            n_channels=n_channels)

        return audioWAV

    def write(self, audio: AudioWAV, file_path: str):
        """ Write an Audio object to a file, file_path must include the file extension """
        match self._get_extension(file_path):
            case "wav":
                wavfile.write(file_path, audio.sample_rate, audio.audio)
            case _:
                raise ValueError("File format not supported")
            