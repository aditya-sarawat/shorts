import random
import requests

PIXABAY_API_KEY = "42518894-e478541da94da97b6ca49eb3f"


def get_random_video_url(video_hits):
    if video_hits:
        random_video_hit = random.choice(video_hits)
        video_url = random_video_hit["videos"]["large"]["url"]
        return video_url
    else:
        return None


def get_top_videos_by_tags(max_videos=10, tag=""):
    URL = f"https://pixabay.com/api/videos/?key={PIXABAY_API_KEY}&safesearch=true&q={tag}&order=popular&per_page={max_videos}"

    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()

        if int(data["total"]) > 0:
            return data["hits"]
        else:
            print(f"No videos found on Pixabay for {tag} tag!")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error during Pixabay API request: {e}")
        return None


def get_top_animated_videos(max_videos=10):
    URL = f"https://pixabay.com/api/videos/?key={PIXABAY_API_KEY}&safesearch=true&order=popular&video_type=animation&per_page={max_videos}"

    try:
        response = requests.get(URL)
        response.raise_for_status()
        data = response.json()

        if int(data["total"]) > 0:
            return data["hits"]
        else:
            print("No animated videos found on Pixabay")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error during Pixabay API request: {e}")
        return None


def get_random_video(tags=[]):
    top_videos = []

    for tag in tags:
        videos_for_tag = get_top_videos_by_tags(30, tag)
        if videos_for_tag:
            top_videos.extend(videos_for_tag)

    if top_videos:
        video_url = get_random_video_url(top_videos)
        return video_url
    else:
        print("No videos found on Pixabay.")
        return None


def get_random_animated_video():
    top_animated_videos = get_top_animated_videos(200)

    if top_animated_videos:
        video_url = get_random_video_url(top_animated_videos)
        return video_url
    else:
        print("No animated videos found on Pixabay.")
        return None
