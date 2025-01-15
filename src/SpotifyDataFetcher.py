import os
import sys
import string
import time
import requests
import pandas as pd
from dotenv import load_dotenv
from abc import ABC, abstractmethod

class DataFetcher(ABC):
    """Abstract base class for data fetching implementations."""

    @abstractmethod
    def fetch_data(self, *args, **kwargs):
        pass

class SpotifyDataFetcher(DataFetcher):
    """Class to fetch data from Spotify's API."""

    def __init__(self, client_id, client_secret, output_file="spotify_tracks.csv"):
        self.client_id = client_id
        self.client_secret = client_secret
        self.output_file = output_file
        self.access_token = self.get_access_token()

    def get_access_token(self):
        """Fetch an access token from Spotify API."""
        try:
            url = "https://accounts.spotify.com/api/token"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = {"grant_type": "client_credentials"}
            response = requests.post(url, headers=headers, data=data, auth=(self.client_id, self.client_secret))
            response.raise_for_status()
            return response.json().get("access_token")
        except Exception as e:
            print("Error obtaining access token:", str(e))
            sys.exit(1)

    def fetch_data(self, limit=1000):
        """Fetch track data from Spotify API using search queries."""
        tracks = {}
        search_queries = list(string.ascii_lowercase)
        search_queries.extend([f"{a}{b}" for a in string.ascii_lowercase for b in string.ascii_lowercase])

        url = "https://api.spotify.com/v1/search"
        headers = {"Authorization": f"Bearer {self.access_token}"}

        for query in search_queries:
            params = {"q": query, "type": "track", "limit": 50}
            try:
                response = requests.get(url, headers=headers, params=params)
                response.raise_for_status()
                results = response.json()

                for item in results.get("tracks", {}).get("items", []):
                    track_id = item.get("id")
                    if track_id not in tracks:
                        tracks[track_id] = {
                            "Title": item.get("name", "Unknown"),
                            "Artists": ", ".join(artist.get("name", "Unknown") for artist in item.get("artists", [])),
                            "Album": item.get("album", {}).get("name", "Unknown"),
                            "Spotify URL": item.get("external_urls", {}).get("spotify", "N/A"),
                        }

                self.update_progress_bar(len(tracks), limit)

                if len(tracks) >= limit:
                    print()  # Move to the next line after the progress bar
                    print(f"Fetched {limit} tracks.")
                    break

                time.sleep(0.1)

            except Exception as e:
                print("Error fetching tracks for query:", query, "Error:", str(e))

        return list(tracks.values())[:limit]

    def save_to_csv(self, data):
        """Save track data to a CSV file."""
        if not data:
            print("No data to save.")
            return

        try:
            df = pd.DataFrame(data)
            df.to_csv(self.output_file, index=False, encoding="utf-8")
            print(f"Data saved to {self.output_file}")
        except Exception as e:
            print("Error saving data to CSV:", str(e))

    @staticmethod
    def update_progress_bar(current, total, bar_length=40):
        progress = current / total
        block = int(bar_length * progress)
        bar = f"[{'#' * block}{'-' * (bar_length - block)}] {current}/{total} ({progress * 100:.2f}%)"
        sys.stdout.write(f"\r{bar}")
        sys.stdout.flush()

if __name__ == "__main__":
    load_dotenv()

    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not CLIENT_ID or not CLIENT_SECRET:
        print("Missing Spotify credentials in .env file.")
        sys.exit(1)

    fetcher = SpotifyDataFetcher(CLIENT_ID, CLIENT_SECRET)
    tracks = fetcher.fetch_data(limit=1000)
    fetcher.save_to_csv(tracks)
