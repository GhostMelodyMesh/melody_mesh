import re
import shutil
from pydub import AudioSegment

class AudioFileConverter:
    """ Class to convert audio files to different formats """

    def __init__(self):
        pass

    def convert_to_mp3(self, file_path: str) -> str:
        """ Convert an audio file to mp3 format, WARNING: after reading the returned path, the temporary file should be deleted """
        extension = re.search(r'\.(\w+)$', file_path).group(1)
        match extension:
            case 'wav':
                audio = AudioSegment.from_wav(file_path)
                file_name = file_path.split('/')[-1]
                temp_file_path = file_path.replace(file_name, 'temp.mp3')
                audio.export(temp_file_path, format='mp3')
                return temp_file_path
            case 'mp3':
                # Copy the file to a temporary file
                file_name = file_path.split('/')[-1]
                temp_file_path = file_path.replace(file_name, 'temp.mp3')
                shutil.copyfile(file_path, temp_file_path)
                return temp_file_path
            case _:
                raise Exception("Unsupported audio file format")

    def convert_to_wav(self, file_path: str) -> str:
        """ Convert an audio file to wav format, WARNING: after reading the returned path, the temporary file should be deleted """
        extension = re.search(r'\.(\w+)$', file_path).group(1)
        match extension:
            case 'wav':
                # Copy the file to a temporary file
                file_name = file_path.split('/')[-1]
                temp_file_path = file_path.replace(file_name, 'temp.wav')
                shutil.copyfile(file_path, temp_file_path)
                return temp_file_path
            case 'mp3':
                audio = AudioSegment.from_mp3(file_path)
                file_name = file_path.split('/')[-1]
                temp_file_path = file_path.replace(file_name, 'temp.wav')
                audio.export(temp_file_path, format='wav')
                return temp_file_path
            case _:
                raise Exception("Unsupported audio file format")

    def convert_to_midi(self, file_path: str) -> str:
        raise Exception("Not implemented")
