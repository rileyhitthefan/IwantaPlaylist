import spotipy
import pandas as pd
from src.spotify_auth import spotify_authenticate

import time
import requests

def recommend(sp, query, limit=30):
    if not sp: 
        sp = spotify_authenticate()
    if len(query) > 250:
        query = query[:250]
    try:
        search_recs = sp.search(q = query, type="track", limit = limit)
        response = search_recs
    except requests.exceptions.RequestException as e:
        if response.status_code == 429:
            retry_after = int(response.headers.get("Retry-After", 60))  # Default to 60 seconds
            print(f"Rate limit reached. Retrying after {retry_after} seconds.")
            time.sleep(retry_after)
            response = sp.search(q = query, type="track", limit = limit)
    # search_recs = sp.search(q = query, type="track", limit = limit)
    recs = []
    for track in search_recs['tracks']['items']:
        recs.append({
            'id': track['id'],
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'release_date': track['album']['release_date'],
            'popularity': track['popularity']
        })
        
    return pd.DataFrame(recs)

def add_playlist(sp, name, tracks):
    if not sp: 
        sp = spotify_authenticate()
    # create playlist
    new_playlist = sp.user_playlist_create(sp.me()['id'], name = name, public=False)
    sp.playlist_add_items(new_playlist['id'], tracks)

    