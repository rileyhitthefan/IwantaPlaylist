import streamlit as st 
from spotify_auth import spotify_auth
from user_data import * # display_user_data, get_playlists, get_playlist_tracks
from lyrics import * # match_lyrics, lyrics_to_words, tokenize_lyrics
from sentiment import sentiment_analysis

# Page title
st.set_page_config(page_title="SpotiMine")
st.title("SpotiMine - Playlist Recommender")

# Spotify Authentication
if "spotify_client" not in st.session_state:
    st.session_state["spotify_client"] = None

if st.session_state["spotify_client"] is None:
    login = st.empty()
    with login.container():
        st.info("Log in to Spotify to get started")
        auth_button = st.button("Login with Spotify")
        
    if auth_button:
        sp = spotify_auth()
        if sp:
            st.session_state["spotify_client"] = sp
            current_user = display_user_data(sp)
            login.empty()
            # User information
            st.success(f"Logged in as {current_user['display_name']}")
            st.image(current_user['images'][0]['url'], width=50)
        else:
            st.error("Login failed.")

if st.session_state["spotify_client"]:
    sp = st.session_state["spotify_client"]
    # Input current music mood
    st.header("Current Mood")
    user_mood = st.text_input("Music mood", "running under the rain so no one knows i'm crying")

    # Get user's playlists
    user_playlists = get_playlists(sp)
    playlist_names = [playlist['name'] for playlist in user_playlists]

    # Display user's playlists for selection
    st.header("Playlists")
    selected_playlist = st.selectbox("Choose a playlist", playlist_names, index = None)
    # Playlist description
    playlist_description = ''.join(p['description'] for p in user_playlists if p['name'] == selected_playlist)
    st.write(playlist_description)
    
    
    # Display playlist tracks
    playlist_id = ''.join(p['id'] for p in user_playlists if p['name'] == selected_playlist)
    if playlist_id:
        tracks = get_playlist_tracks(sp, playlist_id)
        st.write(pd.DataFrame(tracks))
        
        # Match lyrics
        with st.spinner("Matching lyrics..."):
            lyrics_df = match_lyrics(pd.DataFrame(tracks))
            cleaned_lyrics_df = clean_lyrics(lyrics_df, 'lyrics')
            cleaned_lyrics_df = tokenize_lyrics(cleaned_lyrics_df, 'lyrics')
        
        # Sentiment Analysis
        with st.spinner("Analyzing sentiment..."):
            cleaned_lyrics_df['sentiment'] = sentiment_analysis(cleaned_lyrics_df['lyrics'])
            current_mood = [user_mood, selected_playlist, playlist_description]
            current_mood_sentiment = []
            for text, sentiment in zip(current_mood, sentiment_analysis(current_mood)):
                current_mood_sentiment.append({"text": text, "sentiment": sentiment})
            cleaned_lyrics_df['sentiment'] = sentiment_analysis(cleaned_lyrics_df['lyrics'])
            
        st.header("Sentiment Analysis")
        st.write(pd.DataFrame(current_mood_sentiment))
        st.write(pd.DataFrame(cleaned_lyrics_df))