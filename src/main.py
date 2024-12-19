import time
import chromadb
import logging
import os
from typing import Optional


def connect_to_chroma(max_retries: int = 5, retry_delay: int = 2) -> Optional[chromadb.HttpClient]:
    """
    Próbuje połączyć się z bazą Chroma z mechanizmem ponawiania prób
    """
    host = os.getenv("CHROMA_HOST", "chroma-db")
    port = os.getenv("CHROMA_PORT", "8000")

    for attempt in range(max_retries):
        try:
            client = chromadb.HttpClient(host=host, port=port)
            # Sprawdź czy połączenie działa
            client.heartbeat()
            print(f"Połączono z bazą Chroma na {host}:{port}")
            return client
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = retry_delay * (attempt + 1)
                print(f"Próba {attempt + 1} nieudana. Ponowna próba za {wait_time}s...")
                time.sleep(wait_time)
            else:
                print(f"Nie udało się połączyć z {host}:{port} po {max_retries} próbach.")
                raise


def main():
    try:
        client = connect_to_chroma()
        # Tutaj dalsza logika aplikacji...
    except Exception as e:
        print(f"Wystąpił błąd: {e}")
        exit(1)


if __name__ == "__main__":
    main()