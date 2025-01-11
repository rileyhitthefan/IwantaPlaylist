import streamlit as st 
import time
from spotify_auth import spotify_authenticate
from user_data import * # display_user_data, get_playlists, get_playlist_tracks
from lyrics import * # match_lyrics, clean_lyrics, summarize_lyrics, predict_sentiment
from recommend import * # recommend, add_playlist

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
        sp = spotify_authenticate()
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
    user_mood = st.text_input("What's the occasion?", "falling in love with the guy across the room")

    start_time = time.time() # keep track of calls to spotify api
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
        tracks = pd.DataFrame(tracks)
        st.write(tracks)
        
        # Match lyrics
        with st.spinner("Matching lyrics..."):
            lyrics_df = match_lyrics(tracks.sample(50) if len(tracks) > 50 else tracks)
            lyrics_df = clean_lyrics(lyrics_df, 'lyrics')
        st.write("Lyrics found!")
        
        # Sentiment Analysis
        with st.spinner("Summarizing your playlist..."):
            summaries = []
            for lyrics in lyrics_df['lyrics']:
                summaries.append(summarize_lyrics(lyrics))
            lyrics_df['summary'] = summaries
            random_sample = len(lyrics_df)//2
            lyrics_sample = lyrics_df.sample(random_sample)['summary']
        
        user_mood = user_mood + ". " + playlist_description + ". " + ".".join(lyrics_sample) 
            
        st.header("Summarization completed!")
        st.write(summarize_lyrics(user_mood))
            
        st.header("Here's your playlist")
        with st.spinner("Recommending..."):
            elapsed_time = time.time() - start_time
            if elapsed_time < 30:
                time.sleep(30 - elapsed_time)
            recs = recommend(sp, user_mood)
            st.write(recs)
        
        if st.button("Add playlist", type="primary"):
            playlist_name = st.text_input("Give your playlist a name", user_mood[:30])
            rec_tracks = recommend(sp, user_mood)
            add_playlist(sp, playlist_name, recs['id'].tolist())