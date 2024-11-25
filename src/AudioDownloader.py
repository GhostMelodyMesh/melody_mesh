import os
from abc import ABC, abstractmethod
from spotdl import Spotdl # It finds songs from the Spotify playlists on Youtube and downloads them
import yt_dlp # For now the best solution, it works for Youtube and possibly SoundCloud
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
        # self.spotdl = Spotdl() # For Spotify
    
    def folder_exists(self):
        """Ensure that the AUDIO_FOLDER exists."""
        if not os.path.exists(self.AUDIO_FOLDER):
            os.makedirs(self.AUDIO_FOLDER)

    def detect_platform(self, link):
        """Detects the platform based on the link."""
        if "youtube" in link or "youtu.be" in link:
            return "youtube"
        elif "spotify.com" in link:
            return "spotify"
        elif "soundcloud.com" in link:
            return "soundcloud"
        else:
            raise ValueError(f"Unsupported platform: {link}")

    def download_audio(self, link):
        """Download audio from the given link."""
        platform = self.detect_platform(link)

        try:
            if platform == "youtube" or platform == "soundcloud":
                self.download_with_ytdlp(link)
            elif platform == "spotify":
                self.download_with_spotdl(link)
        except Exception as e:
            print(f"Failed to download {link}: {e}")

    def download_with_ytdlp(self, link):
        """Downloading audio using the yt-dlp library"""
        ...

    def download_with_spotdl(self, link):
        """Download audio using the spotdl library"""
        ...

    def download_files(self, file_path, num_files=None, seed=None, download_all=False):
        """Handle downloading audio files"""
        self.folder_exists()
        ...
        