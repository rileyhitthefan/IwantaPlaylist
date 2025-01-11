### Spotify Mood-Based Playlist Recommender

----
#### **Project Overview**
- **Objective:** Recommend playlists based on user specified mood and their chosen tracks 
- **Key Features:**
  - User authentication with Spotify.
  - Summarization and sentiment analysis of user's tracks.
  - Fetching related tracks for playlist suggestions.
  - User feedback system (like/dislike) for improving recommendations.

#### **1. File Structure**
```
.
├── app.py                      # Main Streamlit app
├── spotify_auth.py             # Spotify authentication logic
├── user_data.py                # Functions for fetching playlists, tracks, and related content
├── lyrics.py                   # Match lyrics with songs and process lyrics
├── recommend.py                # Logic for related tracks and playlist recommendations
├── requirements.txt            # Dependencies
└── README.md                   # Project documentation
```

#### **2. Installation and Usage**
- Download the repo or clone to your local environment
   ```
   git clone https://github.com/rileyhitthefan/SpotiMine.git
   ```
- Install required libraries
   ```
   pip install -r requirements.txt
   ```
- Create an .env file in the home folder and store your client information for [Spotify](https://developer.spotify.com/documentation/web-api) and [Genius](https://docs.genius.com/#/getting-started-h1)
   ```
   GENIUS_CLIENT_ID = your_genius_client_id_here
   GENIUS_CLIENT_SECRET = your_genius_client_secret_here
   GENIUS_CLIENT_TOKEN = your_genius_client_token_here
   SPOTIFY_CLIENT_ID = your_spotify_client_id_here
   SPOTIFY_CLIENT_SECRET = your_spotify_client_secret_here
   SPOTIPY_REDIRECT_URI = http://localhost:8888/callback
   ```
- Run Streamlit application
   ```
   streamlit run ./src/app.py
   ```
----
#### **Phases and Steps**

**Phase 1: Spotify Authentication and Setup**
1. Set up Spotify Developer account and create an app.
2. Configure the Spotify OAuth process in `spotify_auth.py`.
3. Allow users to log in using their Spotify accounts.

**Phase 2: Fetching Data**
1. Use the Spotify API to:
   - Fetch user's playlists (name, description, and ID).
   - Fetch track details for playlists (names, artists, IDs).
2. Store playlist and track data in session state.

**Phase 3: Contextual Semantic Search**
1. Embed lyrics and mood information
2. Use similarity measure such as cosine to retrieve most relevant songs/playlists

**Phase 4: Recommendation System**
1. Use the Spotify API to fetch related tracks based on:
   - Sentiment of playlists.
   - Similarity of track features (e.g., genre, artist, popularity).
2. Generate recommendations for playlists with 30 tracks each.

**Phase 5: Feedback System**
1. Implement a like/dislike button for each recommended playlist.
2. Store feedback for analysis and refining recommendations.

#### **4. Tools and Technologies**
- **Back-End:** Spotipy (Spotify API Python library)
- **Sentiment Analysis:** Transformer, NLTK (VADER)
- **Front-End:** Streamlit

----
### OAuth
https://medium.com/@ruixdsgn/a-guide-to-implementing-oauth-authorization-using-spotipy-for-a-playlist-generator-app-6ab50cdf6c3

### NLTK -- Natural Language Toolkit
Provides corpora and lexical resources annd text processing libraries for a various tasks (classification, stemming, parsing, semantic reasoning...)

### Sentiment Analysis
VADER (Valence Aware Dictionary and sEntiment Reasoner) is a lexicon and rule-based sentiment analysis tool.
- Sentiment lexicon is a list of lexical features labeled according to semantic orientation as positive/negative
For multilingual use case: https://huggingface.co/tabularisai/multilingual-sentiment-analysis

### Contextual Semantic Search (CSS)
Search and find information by considering meaning and context to deliver more relevant results. A prompt is analyzed with respect to its sentiment, emotion and intent.
