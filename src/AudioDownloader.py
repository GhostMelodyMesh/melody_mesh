from abc import ABC, abstractmethod
import yt_dlp # For now the best solution, maybe there's a better library for this
from multiprocessing import Pool # For downloading files concurrently


class DataGenerator(ABC):
    """ Get file links from '.txt' and download them to rawAudio folder """
    
    @abstractmethod
    def get_links(self, file_path):
        """Fetch file links from the source"""
        pass 
    

class TxtLinkLoader(DataGenerator):
    """Fetch file links from a .txt file."""
    
    def get_links(self, file_path):
        """Retrieve links line by line from the text file"""
        try:
            with open(file_path, "r") as f:
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return []
        
class AudioDownloader:
    """Handles downloading audio files from links"""
    
    NUM_FILES = 10
    AUDIO_FOLDER = "rawAudio"
    
    def __init__(self, data_generator: DataGenerator):
        self.data_generator = data_generator
        
    def download_audio(self, link):
        """Download audio from the given link using yt-dlp."""
        ...
        print(f"Downloading: {link}")

    def download_files(self, file_path, num_files=None, seed=None, download_all=False):
        """Handle downloading audio files"""
        ...
        