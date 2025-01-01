### Spotify Sentiment-Based Playlist Recommender

#### **1. Project Overview**
- **Objective:** Recommend playlists based on user preferences, playlist sentiment analysis, and related tracks. 
- **Key Features:**
  - User authentication with Spotify.
  - Sentiment analysis of playlist
  - Fetching related tracks for playlist suggestions.
  - User feedback system (like/dislike) for improving recommendations.

#### **2. File Structure**
```
.
├── app.py                      # Main Streamlit app
├── spotify_auth.py             # Spotify authentication logic
├── user_data.py                # Functions for fetching playlists, tracks, and related content
├── lyrics.py                   # Match lyrics with songs
├── sentiment.py                # Sentiment analysis module
├── recommender.py              # Logic for related tracks and playlist recommendations
├── utils.py                    # Utility functions (e.g., data processing)
├── requirements.txt            # Dependencies
└── README.md                   # Project documentation
```

#### **3. Phases and Steps**

**Phase 1: Spotify Authentication and Setup**
1. Set up Spotify Developer account and create an app.
2. Configure the Spotify OAuth process in `spotify_auth.py`.
3. Allow users to log in using their Spotify accounts.

**Phase 2: Fetching Data**
1. Use the Spotify API to:
   - Fetch user's playlists (name, description, and ID).
   - Fetch track details for playlists (names, artists, IDs).
2. Store playlist and track data in session state.

**Phase 3: Sentiment Analysis**
1. Implement sentiment analysis on playlist names and lyrics
2. Categorize playlists based on sentiment (e.g., positive, negative, neutral).\

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

---
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
