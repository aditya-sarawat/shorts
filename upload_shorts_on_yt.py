import os
import youtube_dl
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

PIXABAY_API_KEY = os.getenv('YOUTUBE_API_KEY')

def authenticate_youtube():
    api_key = "YOUR_API_KEY"  # Replace "YOUR_API_KEY" with your actual API key
    return api_key

def upload_to_youtube(video_path, title, tags):
    api_key = authenticate_youtube()
    youtube = build("youtube", "v3", developerKey=api_key)

    request_body = {
        "snippet": {
            "title": title,
            "description": "Uploaded using YouTube API",
            "tags": tags,
            "categoryId": "27",
        },
        "status": {
            "privacyStatus": "public",
        },
    }

    media_file = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=video_path
    ).execute()

    video_id = media_file["id"]
    print(f"Video uploaded successfully! Video ID: {video_id}")
