import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def upload_to_youtube(video_path, title, hashtags):
    try:
        credentials = authenticate_youtube()
        youtube = build("youtube", "v3", credentials=credentials)

        hashtags_str = " ".join(hashtags)

        request_body = {
            "snippet": {
                "title": title[:67] + "..." if len(title) > 70 else title + " #shorts",
                "description": f"Quote: {title} {hashtags_str}",
                "categoryId": "22",
            },
            "status": {"privacyStatus": "public", "selfDeclaredMadeForKids": False},
        }

        media_file = (
            youtube.videos()
            .insert(part="snippet,status", body=request_body, media_body=video_path)
            .execute()
        )

        video_id = media_file["id"]
        logger.info(f"Video uploaded successfully! Video ID: {video_id}")
    except Exception as e:
        logger.error(f"Error uploading video to YouTube: {e}")
