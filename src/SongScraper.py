import sys
import string
import time
import requests

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


number_of_tracks = 1000
tracks = fetch_tracks_via_search(access_token, number_of_tracks)

save_to_csv(tracks, filename="spotify_random_tracks.csv")