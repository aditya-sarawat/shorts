import http
import os
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
        credentials = flow.run_local_server(port=9090)

        # Save the refresh token to a file for future use
        with open(credentials_file, "w") as creds_file:
            creds_file.write(credentials.to_json())

    return credentials


def upload_to_youtube(video_path, title, hashtags):
    credentials = authenticate_youtube()
    youtube = build("youtube", "v3", credentials=credentials)

    hashtags_str = " ".join(hashtags)

    request_body = {
        "snippet": {
            "title": title + " #Shorts",
            "description": "Quote: " + title + " " + hashtags_str,
            "categoryId": "22",
        },
        "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False},
    }

    media_file = (
        youtube.videos()
        .insert(
            part="snippet,status",
            body=request_body,
            media_body=video_path
        )
        .execute()
    )

    video_id = media_file["id"]
    print(f"Video uploaded successfully! Video ID: {video_id}")
