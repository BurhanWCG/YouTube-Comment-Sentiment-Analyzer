from googleapiclient.discovery import build
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from django.conf import settings

# Download VADER lexicon once
nltk.download('vader_lexicon', quiet=True)

def get_youtube_comments(video_id):
    youtube = build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)
    comments = []
    response = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        textFormat='plainText',
        maxResults=100
    ).execute()

    while response:
        for item in response['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
        if 'nextPageToken' in response:
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                textFormat='plainText',
                pageToken=response['nextPageToken'],
                maxResults=100
            ).execute()
        else:
            break
    return comments

def analyze_sentiment(comments):
    analyzer = SentimentIntensityAnalyzer()
    positive, negative, neutral = 0, 0, 0

    for comment in comments:
        scores = analyzer.polarity_scores(comment)
        compound = scores['compound']
        if compound >= 0.05:
            positive += 1
        elif compound <= -0.05:
            negative += 1
        else:
            neutral += 1

    total = positive + negative + neutral
    if total == 0:
        return {"positive": 0, "neutral": 0, "negative": 0}
    
    return {
        "positive": round((positive / total) * 100),
        "neutral": round((neutral / total) * 100),
        "negative": round((negative / total) * 100)
    }