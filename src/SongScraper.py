import sys
import string
import time
import requests
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()

# Pobierz dane uwierzytelniające z pliku .env
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    print("Brak wymaganych danych SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET lub SPOTIFY_PLAYLIST_ID w pliku .env.")
    exit()


def update_progress_bar(current, total, bar_length=40):
    progress = current / total
    block = int(bar_length * progress)
    bar = f"[{'#' * block}{'-' * (bar_length - block)}] {current}/{total} ({progress * 100:.2f}%)"
    sys.stdout.write(f"\r{bar}")
    sys.stdout.flush()


def fetch_tracks_via_search(token, n=10000):
    tracks = {}
    try:
        url = "https://api.spotify.com/v1/search"
        headers = {"Authorization": f"Bearer {token}"}

        search_queries = list(string.ascii_lowercase) 
        search_queries.extend([f"{a}{b}" for a in string.ascii_lowercase for b in string.ascii_lowercase])

        for query in search_queries:
            params = {"q": query, "type": "track", "limit": 50} 
            response = requests.get(url, headers=headers, params=params)

            time.sleep(0.1) 
                       
            response.raise_for_status()
            results = response.json()

            for item in results.get("tracks", {}).get("items", []):
                track_id = item.get("id")
                if track_id not in tracks:
                    tracks[track_id] = {
                        "Title": item.get("name", "Unknown"),
                        "Artists": ", ".join(artist.get("name", "Unknown") for artist in item.get("artists", [])),
                        "Album": item.get("album", {}).get("name", "Unknown"),
                        "Spotify URL": item.get("external_urls", {}).get("spotify", "N/A")
                    }

            update_progress_bar(len(tracks), n)
            if len(tracks) >= n:
                print()
                print(f"Osiągnięto wymaganą liczbę utworów: {n}")
                break

        return list(tracks.values())[:n]

    except Exception as e:
        print("Błąd podczas wyszukiwania utworów:", str(e))
        return []

def save_to_csv(tracks, filename="spotify_tracks.csv"):
    if not tracks:
        print("Brak danych do zapisania!")
        return

    try:
        df = pd.DataFrame(tracks)
        df.to_csv(filename, index=False, encoding="utf-8")
        print(f"Dane zapisane do pliku: {filename}")
    except Exception as e:
        print("Błąd podczas zapisywania danych do pliku CSV:", str(e))



def get_access_token(client_id, client_secret):
    try:
        url = "https://accounts.spotify.com/api/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"grant_type": "client_credentials"}

        response = requests.post(url, headers=headers, data=data, auth=(client_id, client_secret))
        response.raise_for_status()

        token_data = response.json()
        return token_data.get("access_token")
    except Exception as e:
        print("Błąd podczas uzyskiwania tokenu dostępu:", str(e))
        exit()

number_of_tracks = 1000
access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
tracks = fetch_tracks_via_search(access_token, number_of_tracks)

save_to_csv(tracks, filename="spotify_random_tracks.csv")