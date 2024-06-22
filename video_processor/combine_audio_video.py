import os
from moviepy.editor import VideoFileClip, AudioFileClip
from util.generate_file_name import generate_unique_filename
from util.logger import get_logger
from util.check_dir import ensure_directory_exists

logger = get_logger()


def combine_audio_video(audio_path, video_path, output_dir):
    try:
        ensure_directory_exists(output_dir)
        audio = AudioFileClip(audio_path)
        video = VideoFileClip(video_path)
        audio = audio.set_duration(video.duration)
        video_with_audio = video.set_audio(audio)
        output_path = os.path.join(output_dir, generate_unique_filename("mp4"))
        ensure_directory_exists(output_path)
        video_with_audio.write_videofile(
            output_path,
            codec="libx264",
            audio_codec="aac",
            fps=video.fps,
            verbose=False,
            logger=None,
        )
        return output_path
    except Exception as e:
        logger.error(f"Error combining audio and video: {e}")
        return None
