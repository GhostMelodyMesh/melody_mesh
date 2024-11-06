import os
from src.dataTypes.Audio import Audio
from src.dataTypes.AudioWAV import AudioWAV
from src.fileHandlers.AudioFileConverter import AudioFileConverter
from src.fileHandlers.FileHandlerAbstract import FileHandlerAbstract
from scipy.io import wavfile


class AudioFileHandler(FileHandlerAbstract):
    """" Handling of local audio files, reading different file formats, converting them into normalised format, saving them """

    def __init__(self):
        super().__init__()
        pass

    def read_as_wav(self, file_path: str) -> AudioWAV:
        """ Read an audio file as a .wav file """
        
        audioFileConverter = AudioFileConverter()
        temp_path = audioFileConverter.convert_to_wav(file_path)
        
        sample_rate, audio = wavfile.read(temp_path)
        os.remove(temp_path)
        
        audioWAV = AudioWAV()
        audioWAV.audio = audio
        audioWAV.format = 'wav'
        audioWAV.sample_rate = sample_rate
        
        return audioWAV
        
    def write(self, file_path: str, audio: Audio):
        """ Write an Audio object to a file """
        pass