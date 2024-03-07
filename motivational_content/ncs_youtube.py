import os
import random
import time
from tqdm import tqdm
from pytube import YouTube
from pydub import AudioSegment
from youtubesearchpython import VideosSearch

DESTINATION_FOLDER = "./motivational_content/__temp__"

def search_and_download(tags, max_retries=3, retry_delay=5):
    combined_results = []

    for tag in tags:
        search_query = f"{tag} NoCopyrightSounds"
        videos_search = VideosSearch(search_query, limit=50)
        results = videos_search.result()["result"]
        filtered_results = [
            result
            for result in results
            if result.get("channel")
            and result["channel"].get("name") == "NoCopyrightSounds"
        ]
        combined_results.extend(filtered_results)

    if not combined_results and "NoCopyrightSounds" not in tags:
        search_query = "NoCopyrightSounds"
        videos_search = VideosSearch(search_query, limit=50)
        results = videos_search.result()["result"]
        filtered_results = [
            result
            for result in results
            if result.get("channel")
            and result["channel"].get("name") == "NoCopyrightSounds"
        ]
        combined_results.extend(filtered_results)

    if not combined_results:
        print("No results found.")
        return

    selected_video = random.choice(combined_results)
    retries = 0

    while retries < max_retries:
        try:
            video_url = f'https://www.youtube.com/watch?v={selected_video["id"]}'
            yt = YouTube(video_url)
            video = yt.streams.get_highest_resolution()

            os.makedirs(DESTINATION_FOLDER, exist_ok=True)

            video.download(DESTINATION_FOLDER)

            video_path = os.path.join(DESTINATION_FOLDER, video.default_filename)
            audio = AudioSegment.from_file(video_path)

            mp3_path = os.path.join(DESTINATION_FOLDER, "audio.mp3")
            audio.export(mp3_path, format="mp3")
            os.remove(video_path)

            print(f"Downloaded video: {selected_video['title']}")
            return
        except Exception as e:
            print(f"Error downloading video: {e}")
            retries += 1
            print(f"Retrying ({retries}/{max_retries}) in {retry_delay} seconds...")
            time.sleep(retry_delay)

    print("Max retries reached. Failed to download video.")
