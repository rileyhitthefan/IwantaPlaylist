import spotipy
import pandas as pd

def recommend(sp, query, limit=30):
    search_recs = sp.search(q = query, type="track", limit = limit)
    recs = []
    for track in search_recs['tracks']['items']:
        recs.append({
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'release_date': track['album']['release_date'],
            'popularity': track['popularity']
        })
        
    return pd.DataFrame(recs)