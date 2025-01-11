import spotipy
import pandas as pd
from spotify_auth import spotify_authenticate

import time
import requests
from typing import Optional, List
import logging
import backoff
from spotipy.exceptions import SpotifyException

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@backoff.on_exception(
    backoff.expo,
    (SpotifyException, requests.exceptions.RequestException),
    max_tries = 5,
    giveup = lambda e: not(
        getattr(e, 'http_status', None) in [429, 502] or
        isinstance(e, requests.exceptions.RequestException)
    )
)

def recommend(sp, query, limit=30):
    if not sp: 
        sp = spotify_authenticate()
        
    if len(query) > 250:
        query = query[:250]
        
    try:
        search_recs = sp.search(q = query, type="track", limit = limit)
        response = search_recs
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
    
    except SpotifyException as e:
        if getattr(e, 'http_status', None) == 429:
            retry_after = int(e.headers.get('Retry-After', 60))
            logger.info(f"Rate limited. Retrying in {retry_after} seconds.")
            # backoff dec will handle retry
            raise 
        logger.error(e)
        raise 
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise

def add_playlist(sp, name, tracks):
    if not sp: 
        sp = spotify_authenticate()
        
    try:
    # create playlist
        new_playlist = sp.user_playlist_create(sp.me()['id'], name = name, public=False)
        sp.playlist_add_items(new_playlist['id'], tracks)
        logger.info(f"Playlist {name} added.")
        
    except SpotifyException as e:
        logger.error(e)
        raise

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise