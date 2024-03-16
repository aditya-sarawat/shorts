import os
import youtube_dl
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

def authenticate_youtube():
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    credentials_file = "credentials.json"

    if os.path.exists(credentials_file):
        credentials = Credentials.from_authorized_user_file(credentials_file)
    else:
        flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", scopes)
        credentials = flow.run_console()
        
        # Save the refresh token to a file for future use
        with open(credentials_file, "w") as credentials_file:
            credentials_file.write(credentials.to_json())

    return credentials

def upload_to_youtube(video_path, title, tags):
    credentials = authenticate_youtube()
    youtube = build("youtube", "v3", credentials=credentials)

    request_body = {
        "snippet": {
            "title": title,
            "description": "Uploaded using YouTube API",
            "tags": tags,
            "categoryId": "27",  # Category ID for Shorts
        },
        "status": {
            "privacyStatus": "public",
        },
    }

    media_file = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=video_path,
    ).execute()

    video_id = media_file["id"]
    print(f"Video uploaded successfully! Video ID: {video_id}")

