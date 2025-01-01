# https://github.com/cristobalvch/Music-Lyrics-NLP/blob/master/helpers.py
import os
from dotenv import load_dotenv
load_dotenv()
import lyricsgenius 

import pandas as pd

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer

# nltk.download('stopwords')
# nltk.download('wordnet')   
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')   

gen_client_access_token = os.getenv("GENIUS_CLIENT_TOKEN")
genius = lyricsgenius.Genius(gen_client_access_token)

def match_lyrics(df, frac = 0.3):
    """
    Search lyrics based on provided list of songs
    Args:
        df (DataFrame): df containing song information
        frac (float): fraction of songs to search
    Returns: 
        df (DataFrame): DataFrame containing the lyrics of the songs
    """
    list_lyrics = []
    # get random n songs
    df = df.sample(frac=frac)

    for i, track in df.iterrows():
        title = track['name']
        artist = track['artist']
        lyrics = genius.search_song(title, artist)
        if lyrics:
            list_lyrics.append({
                'title': title,
                'artist': artist,
                'lyrics': lyrics.lyrics
            })
        else:
            list_lyrics.append({
                'title': title,
                'artist': artist,
                'lyrics': "Lyrics unavailable"
            })

    list_lyrics = pd.DataFrame(list_lyrics)
    return list_lyrics

def clean_lyrics(df, column):
    """
    Cleans the words without importance and fix the format of the  dataframe's column lyrics 
    Args:
        df (DataFrame): df containing song information
        column (str): column to clean
    Returns:
        df (DataFrame): DataFrame containing the cleaned lyrics
    """
    df[column] = df[column].str.lower()
    # remove section marker
    df[column] = df[column].str.replace(r"(verse\s?\d*|chorus|bridge|outro|intro)", "", regex=True)
    df[column] = df[column].str.replace(r"(instrumental|guitar|solo)", "", regex=True) 
    df[column] = df[column].str.replace(r"\[.*?\]", "", regex=True)
    # remove new line
    df[column] = df[column].str.replace(r"\n", " ", regex=True)
    # remove special characters
    df[column] = df[column].str.replace(r"[^\w\d'\s]+", "", regex=True)
    df[column] = df[column].str.strip()

    return df

def nltk_pos_tagger(nltk_tag):
    """
    Map NLTK POS tags to WordNet POS tags for lemmatization.
    """
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN  # Default to noun

def tokenize_lyrics(df, column):
    """
    Tokenizes and lemmatizes the lyrics column of a DataFrame.
    
    Args:
        df (DataFrame): df containing song information.
        column (str): column to process
    
    Returns:
        df (DataFrame): DataFrame with tokenized and lemmatized lyrics.
    """
    lemmatizer = WordNetLemmatizer()
    
    def process_lyrics(lyrics):
        tokens = word_tokenize(lyrics)
        # get pos tags
        pos_tags = nltk.pos_tag(tokens)
        # lemmatize words based on pos tags
        lemmatized = [
            lemmatizer.lemmatize(token, nltk_pos_tagger(tag))
            for token, tag in pos_tags
        ]
        return lemmatized
    df['tokens'] = df[column].apply(process_lyrics)
    return df