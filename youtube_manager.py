from typing import Optional, Tuple, List
from py_youtube import Search
import logging
import threading
import yt_dlp

logger = logging.getLogger(__name__)

class YouTubeManager:
    """Handles YouTube search and download operations"""

    @staticmethod
    def search(query: str, limit: int = 9) -> List[Tuple[str, str, str]]:
        """Search YouTube and return (id, title, thumbnail) results"""
        try:
            results = Search(query, limit=limit).videos()
            return [(v["id"], v["title"], v["thumb"][0]) for v in results]
        except Exception as e:
            logger.error(f"YouTube search failed: {str(e)}")
            return []

    @staticmethod
    def get_stream_url(video_id: str, media_type: str) -> Optional[str]:
        """Get direct stream URL for YouTube content"""
        ydl_opts = {
            'quiet': True,          # Suppress output
            'no_warnings': True,   # Ignore warnings
            'format': media_type,      # Select the best quality single-file format (video + audio)
            'outtmpl': '%(title)s.mp4' if format == "best" else '%(title)s.mp3'
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"https://youtu.be/{video_id}", download=False)
                return info.get("url")
        except Exception as e:
            logger.error(f"Stream URL fetch failed: {str(e)}")
            return None
    
    @staticmethod
    def download(stream_id, media_type):
        print(media_type)
        ydl_opts = {
            'quiet': True,          # Suppress output
            'no_warnings': True,   # Ignore warnings
            'format': media_type,      # Select the best quality single-file format (video + audio)
            'outtmpl': '%(title)s.mp4' if media_type == "best" else '%(title)s.mp3'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(stream_id)
            ydl.download(stream_id)
            print("The file has been downloaded successfully")
