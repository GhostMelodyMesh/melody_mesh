import re
from dataTypes.Audio import Audio
from dataTypes.AudioWAV import AudioWAV
from src.fileHandlers.FileHandlerAbstract import FileHandlerAbstract
from scipy.io import wavfile


class AudioFileHandler(FileHandlerAbstract):
    """" Handling of local audio files, reading different file formats, converting them into normalised format, saving them """

    def __init__(self):
        super().__init__()
        pass

    def read(self, file_path: str) -> Audio:
        """ Read an audio file and return an Audio object and its format (included in Audio type) """
        extension = re.search(r'\.(\w+)$', file_path).group(1)
        match extension:
            case 'wav':
                return self._read_wav(file_path)
            case _:
                raise Exception("Unsupported audio file format")

    def write(self, file_path: str, audio: Audio):
        """ Write an Audio object to a file """
        pass

    def _read_wav(self, file_path: str) -> AudioWAV:
        """ Read a .wav file and return an AudioWAV object """
        wav = AudioWAV()
        # read file
        sample_rate, data = wavfile.read(file_path)
        # set audio data
        wav.set_audio(data)
        # set format
        wav.set_format('wav')
        # set sample rate
        wav.set_sample_rate(sample_rate)
        return wav