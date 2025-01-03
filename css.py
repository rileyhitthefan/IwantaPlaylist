from transformers import pipeline
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def sentiment_analysis(text, model_name = "tabularisai/multilingual-sentiment-analysis"):
    """
    Use pretrained model for multilingual sentiment analysis of lyrics
    Args:
        text (str): lyrics to analyze
        model_name (str): multilingual sentiment analysis model
    Returns:
        df (DataFrame): DataFrame containing the sentiment analysis
    """
    # tokenizer = AutoTokenizer.from_pretrained(model_name)
    # model = AutoModelForSequenceClassification.from_pretrained(model_name)    
    
    def predict_sentiment(texts):
        sentiment_map = {
            0: "crying",
            1: "kinda sad",
            2: "just chillin'",
            3: "i'm cool",
            4: "woohoo"
        }
        pipe = pipeline(model=model_name)
        sentiments = pipe(texts)
        labels = [sentiment['label'][-1] for sentiment in sentiments]
        return [sentiment_map[int(p)] for p in labels]
    
    sentiments = []
    for lyrics in text:
        sentiments.append(predict_sentiment([lyrics[:512]])[0])
    
    return sentiments

def get_embeddings(texts):
    """
    Get embeddings for song lyrics and current mood
    Args:
        texts (str): lyrics and current mood
    """
    