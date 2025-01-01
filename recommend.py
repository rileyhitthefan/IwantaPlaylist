def get_related_tracks(sp, track_ids, sentiment):
    """
    Get related tracks based on sentiment and seed tracks.
    
    Args:
        sp (Spotify): Spotify client instance.
        track_ids (list): List of track IDs to use as seeds.
        sentiment (str): Sentiment ("positive", "neutral", "negative").
    
    Returns:
        list: List of recommended tracks.
    """
    seed_tracks = track_ids[:5]  # Spotify allows max 5 seed tracks
    sentiment_filter = {"positive": "happy", "negative": "sad", "neutral": "calm"}
    
    recommendations = sp.recommendations(seed_tracks=seed_tracks, limit=30)
    return [
        {"name": track["name"], "artists": ", ".join(artist["name"] for artist in track["artists"])}
        for track in recommendations["tracks"]
        if sentiment_filter[sentiment] in track["name"].lower()
    ]
