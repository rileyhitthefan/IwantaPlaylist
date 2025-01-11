import os
from dotenv import load_dotenv
load_dotenv()

import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Get Spotify app credentials from .env
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SCOPES = "user-library-read playlist-read-private user-top-read"

def spotify_authenticate():
    """
    Authenticate user and return Spotify client instance
    """
    oauth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPES
    )

    sp = spotipy.Spotify(oauth_manager=oauth_manager)
    return sp