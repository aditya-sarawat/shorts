from motivational_content import generate_motivational_content
from upload_shorts_on_yt import upload_to_youtube

if __name__ == "__main__":
    video_path, title, tags = generate_motivational_content()
    upload_to_youtube(video_path, title, tags)
    