from time import time
from typing import Optional
import logging
import vlc

logger = logging.getLogger(__name__)


class MediaController:
    """Handles all media playback operations using VLC"""

    def __init__(self):
        self.Instance = vlc.Instance()
        self.player: Optional[vlc.MediaPlayer] = None
    
    def play(self):
        self.media_player_is_playing()
        self.player.play()

    # Pause button
    def pause(self):
        self.media_player_is_playing()
        self.player.pause()
    
    #Stop button
    def stop(self):
        try:
            self.player.pause()
            self.media_player_is_playing()
            self.player.stop()
            self.player.release()
        except Exception as e:
            logger.error(f"Error stopping the video: {str(e)}")
    
    # Update the volume with the scale
    def volume_scale(self, volume):
        self.player.audio_set_volume(volume)

    # Methods related to the scale of the video duration
    
    '''def on_tick(self):
        if self.player:
            lenght = self.player.get_length() * 1e-3  # to seconds
            if lenght > 0:
                self.slider_video_duration.configure(to=lenght)

                t = self.player.get_time() * 1e-3  # to seconds
                if t > 0 and time() > (self.time_slider_update + 2):
                    self.slider_video_duration.set(t)
                    self.time_slider_last = int(self.time_var.get())

                    if self.time_var.get() + 0.1 >= lenght:
                        self.stop_btn()
                        return 0

        self.after(100, self.on_tick)

    def on_time(self, *unused):
        if self.player:
            t = self.time_var.get()
            if self.time_slider_last != int(t):
                self.player.set_time(int(t * 1e3))
                self.time_slider_update = time()
    
    def update_video_slider(self, t):
        if self.slider_video_duration.get() == t:
            self.stop_btn()'''
    
    def media_player_is_playing(self) -> bool:
        if self.player.is_playing() == 0:
            return True
        else:
            return False

    def video(self, frame_display, video):
        self.player = self.Instance.media_player_new()
        Media = self.Instance.media_new(video)
        self.player.set_hwnd(frame_display.winfo_id())
        self.player.set_media(Media)

    # Show an instance of an audio
    def audio(self, audio):
        # Playing the audio
        self.player = self.Instance.media_player_new()
        Media = self.Instance.media_new(audio)
        self.player.set_media(Media)
