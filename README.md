### Spotify Mood-Based Playlist Recommender

----

[Link to article](https://emobitsh.notion.site/IwantaPlaylist-NLP-based-music-recommender-178d590d474f80209641c2ab728bd1a4)

#### **Project Overview**
- **Objective:** Recommend playlists based on user specified mood and their chosen tracks 
- **Key Features:**
  - User authentication with Spotify.
  - Summarization and sentiment analysis of user's tracks.
  - Fetching related tracks for playlist suggestions.

----

#### **1. File Structure**
```
.
├── .env                        # Environment variables 
├── src/                        # Application source code
│   ├── app.py                  # Main Streamlit app
│   ├── spotify_auth.py         # Spotify authentication logic
│   ├── user_data.py            # Get user's Spotify playlists
│   ├── lyrics.py               # Match lyrics with songs and process lyrics
│   ├── recommend.py            # Tracks recommendation
├── requirements.txt            # Dependencies
└── README.md                   # Documentation
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
2. Configure the Spotify OAuth process.
3. Allow users to log in using their Spotify accounts.

**Phase 2: Fetching Data**
1. Use the Spotify API to:
   - Fetch user's playlists (name, description, and ID).
   - Fetch track details for playlists (names, artists, IDs).
2. Store playlist and track data in session state.

**Phase 3: Contextual Semantic Search**
1. Embed lyrics and mood information.
2. Use similarity measure such as cosine to retrieve most relevant songs.
3. Summarize song lyrics and user input to create query.

**Phase 4: Recommendation System**
1. Use the Spotify API to fetch related tracks based on:
   - Summary of tracks lyrics and user's mood.
   - Similarity of track features (e.g., genre, artist, popularity).
2. Generate recommendations for playlists with 30 tracks each.

----

#### **Tools and Technologies**
- **Back-End:** Spotipy (Spotify API Python library)
- **Sentiment Analysis:** Transformer, NLTK (VADER)
- **Front-End:** Streamlit

----

#### Notes

**OAuth**
https://medium.com/@ruixdsgn/a-guide-to-implementing-oauth-authorization-using-spotipy-for-a-playlist-generator-app-6ab50cdf6c3

**NLTK -- Natural Language Toolkit**
Provides corpora and lexical resources annd text processing libraries for a various tasks (classification, stemming, parsing, semantic reasoning...)

**Sentiment Analysis**
VADER (Valence Aware Dictionary and sEntiment Reasoner) is a lexicon and rule-based sentiment analysis tool.
- Sentiment lexicon is a list of lexical features labeled according to semantic orientation as positive/negative
For multilingual use case: https://huggingface.co/tabularisai/multilingual-sentiment-analysis

**Contextual Semantic Search (CSS)**
Search and find information by considering meaning and context to deliver more relevant results. A prompt is analyzed with respect to its sentiment, emotion and intent.

**Evaluation**
Two common metrics are BLEU and ROUGE scores
- BLEU (Bilingual Evaluation Understudy): widely used for machine translation tasks

$$ 0 <= BLEU = BP*(\sum(wn*pn))^e <= 1 $$

  - Measures the similarity between machine-translated and human reference translations using n-grams --> Precision of n-grams
  - The precision of n-grams in machine translation is applied with a brevity penalty on translations shorter than reference
    - BP (Brevity penalty) = min(1, ref_len/trans_len)
    - pn (Precision of n-grams) = len(common_ngrams)/len(total_ngrams)
      - w (Weights of precision of n-grams)
  - Simple and effective way to assess quality of machine translations
    - Relies heavily on n-grams and not overall meaning or fluency of translation

- ROUGE (Recall-Oriented Understudy for Gisting Evaluation): commonly used for text summarization tasks
 
$$ 0 <= \sum(rn) <= 1 $$
 
  - Evaluates quality by comparing to reference summaries provided by humans
  - Uses overlapping n-grams to measure similarity and calculate recall of n-grams
  - rn (Recall of n-grams): len(common_ngrams)/len(ref_ngrams)
  - ROUGE scores are branched into ROUGE-N, ROUGE-L, ROUGE-S
    - ROUGE-N: measures and computes precision, recall and F1 based on n-gram overlap (consider grammatical correctness and fluency)
    - ROUGE-L: measures longest common subsequence (regardless of word order) and computes precision, recall, F1 based on length LCS (evaluate semantic similarity and content coverage)
    - ROUGE-S: measures skip-bigram (at most 1 intervening word) and computes precision, recall and F1 (evaluate coherence and local cohesion for adjacent words)
  - Objectively (?) assesses quality of machine summaries, flexible n for n-grams
    - May not fully capture semantic meaning or coherence
    - Relies heavily on n-gram overlap