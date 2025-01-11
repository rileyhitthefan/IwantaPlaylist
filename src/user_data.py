import pandas as pd

def display_user_data(sp):
    """
    Display user data from Spotify
    Args:
        sp: Spotify client instance
    """
    user = sp.current_user()
    return user

def get_playlists(sp):
    """
    Fetch user's playlists from Spotify
    Args:
        sp: Spotify client instance
    Returns: 
        playlists (list): list of playlist details
    """
    user_playlists = sp.current_user_playlists()
    playlists = []
    for playlist in user_playlists['items']:
        playlists.append({
            'id': playlist['id'],
            'name': playlist['name'],
            'description': playlist['description'],
            'tracks_count': playlist['tracks']['total']
        })
    return playlists

def get_playlist_tracks(sp, playlist_id):
    """
    Fetch tracks from a playlist
    Args:
        sp: Spotify client instance
        playlist_id (str): playlist ID
    Returns:
        ptracks (list): list of track details
    """
    playlists = sp.playlist(playlist_id)
    ptracks = []
    for item in playlists['tracks']['items']:
        track = item['track']
        ptracks.append({
            'id': track['id'],
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'release_date': track['album']['release_date'],
            'popularity': track['popularity']
        })
    return ptracks

def save_to_csv(data, filename):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)