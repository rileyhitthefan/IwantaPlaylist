from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_name = "tabularisai/multilingual-sentiment-analysis"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

def sentiment_analysis(text):
    """
    Use pretrained model for multilingual sentiment analysis of lyrics
    Args:
        text (str): lyrics to analyze
    Returns:
        df (DataFrame): DataFrame containing the sentiment analysis
    """
    def predict_sentiment(text):
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = model(**inputs)
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        sentiment_map = {
            0: "sombre",
            1: "sad",
            2: "neutral",
            3: "happy",
            4: "ecstatic"
        }
        return [sentiment_map[p] for p in torch.argmax(probabilities, dim=-1).tolist()] 
    
    sentiments = []
    for lyrics in text:
        sentiments.append(predict_sentiment([lyrics])[0])
    
    return sentiments