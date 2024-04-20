import os
import random
import time
from pytube import YouTube
from pydub import AudioSegment
from youtubesearchpython import VideosSearch
from util.random import get_random
from util.logger import get_logger

logger = get_logger()

# Channels to search for copyright-free music
ALLOWED_CHANNELS = [
    "NoCopyrightSounds",
    "Background Music Without Limitations",
    "No Copyright Background Music",
    "Infraction - No Copyright Music",
    "No Copyright Music",
    "MorningLightMusic",
    "BreakingCopyright — Royalty Free Music",
]


def search_videos(tags, max_results=50):
    combined_results = []

    try:
        for tag in tags:
            search_query = f"{tag} no copyright background music"
            videos_search = VideosSearch(search_query, limit=max_results)
            results = videos_search.result()["result"]

            # Filter results by allowed channels
            filtered_results = [
                result
                for result in results
                if result.get("channel")
                and result["channel"].get("name") in ALLOWED_CHANNELS
            ]
            combined_results.extend(filtered_results)

        # If no relevant results are found, search for general NoCopyrightSounds videos
        if not combined_results and "NoCopyrightSounds" not in tags:
            search_query = "no copyright background music"
            videos_search = VideosSearch(search_query, limit=50)
            results = videos_search.result()["result"]

            # Filter results to include only those from the NoCopyrightSounds channel
            filtered_results = [
                result
                for result in results
                if result.get("channel")
                and result["channel"].get("name") in ALLOWED_CHANNELS
            ]
            combined_results.extend(filtered_results)

        if not combined_results:
            logger.warning("No relevant videos found on YouTube.")
            return

        # Select a random video from the combined results
        selected_video = get_random(combined_results)

        return selected_video["id"]
    except Exception as e:
        error_message = f"Error occurred during video search: {e}"
        logger.error(error_message)
        return None
