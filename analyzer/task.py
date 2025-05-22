from celery import shared_task
from .utils import get_youtube_comments, analyze_sentiment

@shared_task
def analyze_video_comments(video_id):
    comments = get_youtube_comments(video_id)
    sentiment_summary = analyze_sentiment(comments)
    return sentiment_summary