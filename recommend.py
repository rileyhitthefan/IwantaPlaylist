import spotipy
import pandas as pd
import spotify_auth

def recommend(sp, query, limit=30):
    if not sp: 
        sp = spotify_auth()
    if len(query) > 250:
        query = query[:250]
    search_recs = sp.search(q = query, type="track", limit = limit)
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
    # create playlist
    new_playlist = sp.user_playlist_create(sp.me()['id'], name = name, public=False)
    sp.playlist_add_items(new_playlist['id'], tracks)