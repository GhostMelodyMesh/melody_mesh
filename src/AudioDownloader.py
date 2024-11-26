"""
We've got some problems:
1. Yt_dlp library probably doesn't work - it needs to be checked out
2. If we want to download songs from Spotify we need to have Spotify API for that,
and there's probably no way arround it.

Some insights:
1. I've fixed Pool, now it should work. I've just implemented Pool locally in the func.
2. Also, we should write types in functions, it's a better practise imo.
3. I fixed get_links, cuz we need to separate name of the song from the link.
"""

import os
import subprocess 
import random
from abc import ABC, abstractmethod
from spotdl import Spotdl # UPDATE: We need client_id and client_secret from Spotify Dev for it to work....and I don't think there's another way
import yt_dlp # For now the best solution, it works for Youtube and possibly SoundCloud
from yt_dlp.utils import DownloadError
from multiprocessing import Pool # For downloading files concurrently

class DataGenerator(ABC):
    """ Get file links from '.txt' and download them to rawAudio folder """
    @abstractmethod
    def get_links(self, file_path: str) -> list: # It is better to write types of data and return types in the functions
        """Fetch file links from the source"""
        pass 
    
class TxtLinkLoader(DataGenerator):
    """Fetch file links from a .txt file. 'name; URL' format"""
    
    def get_links(self, file_path: str) -> list:
        """Retrieve links line by line from the text file, with ignoring track names"""
        try:
            with open(file_path, "r") as f:
                return [line.split(';')[1].strip() for line in f if ';' in line]
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return []
        
class AudioDownloader:
    """Handles downloading audio files from links"""
    
    # NUM_FILES = 10
    # AUDIO_FOLDER = "rawAudio"
    # LINKS_PATH = "./audioFilesLinks.txt"
    
    def __init__(self, 
                 data_generator: DataGenerator, 
                 audio_folder: str="rawAudio", 
                 num_files: int = 10, 
                 links_path: str ="./audioFilesLinks.txt",
                 client_id: str = None,
                 client_secret: str = None):
        self.audio_folder = audio_folder   # It's better to initiate those here
        self.num_files = num_files
        self.links_path = links_path
        self.data_generator = data_generator
        # self.spotdl = Spotdl(client_id=client_id, client_secret=client_secret) # For Spotify
    
    def folder_exists(self):
        """Ensure that the audio_folder exists."""
        if not os.path.exists(self.audio_folder):
            os.makedirs(self.audio_folder)

    def detect_platform(self, link: str) -> str:
        """Detects the platform based on the link."""
        if "youtube" in link or "youtu.be" in link:
            return "youtube"
        elif "spotify.com" in link:
            return "spotify"
        elif "soundcloud.com" in link:
            return "soundcloud"
        else:
            raise ValueError(f"Unsupported platform: {link}")

    def download_audio(self, link: str):
        """Download audio from the given link."""
        platform = self.detect_platform(link)

        try:
            if platform in ["youtube", "soundcloud"]:
                self.download_with_ytdlp(link)
            elif platform == "spotify":
                self.download_with_spotdl(link)
        except Exception as e:
            print(f"Failed to download {link}: {e}")

    def download_with_ytdlp(self, link: str):
        """Downloading audio using the yt-dlp library"""
        yt_opts = {
            "outtmpl": f"./{self.audio_folder}/%(title)s.%(ext)s",
            "format": "bestaudio",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav", #which extension should we set as default?
            }]
        }
        try:
            with yt_dlp.YouTubeDL(yt_opts) as yt_dl:
                yt_dl.download(link)
        except DownloadError as e:
            print(f"Failed to download {link}")
            return

    def download_with_spotdl(self, link: str):
        """Download audio using the spotdl library"""
        try:
            self.spotdl.download(link)
        except Exception as e:
            print(f"Failed to download {link} with Spotdl: {e}")

    def download_files(self, file_path: str ="audioFilesLinks.txt", num_files: int = 10, seed: int =None, download_all: bool = False):
        """Handle downloading audio files"""
        self.folder_exists()
        urls = self.data_generator.get_links(file_path)

        if not download_all: 
            if seed != None:
                random.seed(seed)
            random_indices = [random.randint(0, len(urls)-1) for i in range(num_files)]
            urls_scraped = []
            for i in range(num_files):
                urls_scraped.append(urls[random_indices[i]])
            with Pool() as pool:
                pool.map(self.download_audio, urls_scraped)  
        else:
            with Pool() as pool:
                pool.map(self.download_audio, urls)


