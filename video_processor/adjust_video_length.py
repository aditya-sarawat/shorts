import os
from moviepy.editor import VideoFileClip
from util.logger import get_logger
from util.check_dir import ensure_directory_exists

logger = get_logger()

BASE_PATH = "./__temp__/"

def trim_and_rename_video(video_path, target_duration):
    try:
        temp_path = BASE_PATH + "trimmer.mp4"
        video_clip = VideoFileClip(video_path)
        trimmed_clip = video_clip.subclip(0, target_duration)
        
        # Ensure the output directory exists
        ensure_directory_exists(temp_path)
        
        trimmed_clip.write_videofile(
            temp_path, codec="libx264", audio_codec="aac", verbose=False, logger=None
        )
        
        # Close the video clips to release resources
        video_clip.close()
        trimmed_clip.close()
        
        # Rename the trimmed video to the original filename
        os.rename(temp_path, video_path)
        
        return True
    except Exception as e:
        logger.error(f"Error trimming and renaming video: {e}")
        return False

def adjust_video_length_for_quote(video_path, quote):
    try:
        video_duration = VideoFileClip(video_path).duration
        quote_length = len(quote.split())
        required_duration = max((quote_length * 0.8) + 4, 15)
        
        if video_duration < required_duration:
            return video_duration, required_duration
        else:
            if trim_and_rename_video(video_path, target_duration=required_duration):
                logger.info("Trimming video according to quote")
                return video_duration, required_duration
            else:
                logger.warning("Failed to trim and rename video.")
                return None, None
    except Exception as e:
        logger.error(f"Error processing video for quote: {e}")
        return None, None
