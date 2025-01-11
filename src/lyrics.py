# https://github.com/cristobalvch/Music-Lyrics-NLP/blob/master/helpers.py
import os
from dotenv import load_dotenv
load_dotenv()
import lyricsgenius 

import pandas as pd
import random

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch

model_name = "tabularisai/multilingual-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

gen_client_access_token = os.getenv("GENIUS_CLIENT_TOKEN")

def match_lyrics(df, frac = 0.3):
    """
    Search lyrics based on provided list of songs
    Args:
        df (DataFrame): df containing song information
        frac (float): fraction of songs to search
    Returns: 
        df (DataFrame): DataFrame containing the lyrics of the songs
    """
    genius = lyricsgenius.Genius(gen_client_access_token, sleep_time=1, timeout=15)
    
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
    df[column] = df[column].str.replace(r"\n", ". ", regex=True)
    # remove special characters
    df[column] = df[column].str.replace(r"[^\w\d'\s.]+", "", regex=True)
    df[column] = df[column].str.strip()

    return df

def summarize_lyrics(text, num_sen = 3):
    """
    Summarize the lyrics column of a DataFrame.
    
    Args:
        text (str): lyrics to summarize
        num_sen (int): number of sentences to summarize
    Returns:
        df (DataFrame): DataFrame with summarized lyrics.
    """        
    languages = stopwords.fileids() # list of supported languages
    stopWords = set(stopwords.words([language for language in languages]))
    
    sentences = []
    for sentence in text.split('.'):
        sentences.append(sentence)
        
    words = word_tokenize(text)
    words = [word for word in words if word not in stopWords]
    
    fdict = FreqDist(words) # frequency distribution
    
    # assign scores to senteces based on word frequencies
    sentence_scores = [sum(fdict[word] for word in word_tokenize(sentence) if word in fdict) for sentence in sentences]
    sentence_scores = list(enumerate(sentence_scores))
    
    # sort descending
    sorted_sentences = sorted(sentence_scores, key = lambda x: x[1], reverse = True)
    
    # Randomly select the top `num_sentences` sentences for the summary
    random_sentences = random.sample(sorted_sentences[:10], num_sen)

    # Sort the randomly selected sentences based on their original order in the text
    summary_sentences = sorted(random_sentences, key=lambda x: x[0])

    # Create the summary
    summary = '.'.join([sentences[i] for i, _ in summary_sentences])

    return summary

def predict_sentiment(texts):
    # sentiment_map = {0: "Somber", 1: "Sad", 2: "Neutral", 3: "Happy", 4: "Estactic"}
    pipe = pipeline(task="sentiment-analysis", model=model_name)
    sentiments = pipe(texts)
    labels = [sentiment['label'] for sentiment in sentiments]
    # return [sentiment_map[int(p)] for p in labels]
    return labels