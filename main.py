import image_database
import youtube_manager
import vlc_manager
import os

from time import time
from threading import Thread
from tkinter import *
from tkinter import ttk
import customtkinter
from tkinter.filedialog import askopenfilename
from PIL import Image
import PIL.Image
import PIL.ImageTk

from pathlib import Path
import logging

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"

# Configure application appearance
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("dark-blue")

# Constants
APP_NAME = "PyPlayer"
WINDOW_WIDTH = 1180
WINDOW_HEIGHT = 620
IMAGE_DIR = Path(__file__).parent / "Images"
IMAGE_EXTENSIONS = (
            ("image files", ".png .jpg .gif"),
            ("all files", "*.*"))
SUPPORTED_VIDEO = (".mp4", ".webm", ".mpg", ".flv", ".mkv")
SUPPORTED_AUDIO = (".mp3", ".ogg", ".wav")

logger = logging.getLogger(__name__)


class PyPlayer(customtkinter.CTk):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title(APP_NAME)
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.gridrows = self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12), weight=1)
        self.gridcolumns = self.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1)

        # Initialize components
        self.image_db = image_database.ImageDatabase()
        self.yt_manager = youtube_manager.YouTubeManager()
        self.media_manager = vlc_manager.MediaController()
        
    
        #Options
        def _menu_options(choice) -> None:
            color = "dark"
            if choice == "Select a video or audio file":
                self._video_file()
            elif choice == "Select a background image":
                self._select_background_image()
            elif choice == "Change app color":
                if color == "dark":
                    color = "light"
                    customtkinter.set_appearance_mode(color)
                else:
                    color = "dark"
                    customtkinter.set_appearance_mode(color)

        #Menu
        default_value = customtkinter.StringVar(value="Options")
        self.menu = customtkinter.CTkOptionMenu(master=self,
                                                height=28,
                                                font=("arial", 14),
                                                dropdown_font=("arial", 14),
                                                values=["Select a video or audio file", 
                                                        "Select a background image",
                                                        "Change app color"],
                                                command=_menu_options,
                                                variable=default_value)
        self.menu.grid(row=0, column=0, pady=5)

        #Create main frame for the player
        self.frame_main_frame = customtkinter.CTkFrame(master=self,
                                                        height=470,
                                                        #fg_color="blue",
                                                        corner_radius=10,)
        self.frame_main_frame.grid(row=1, column=0, rowspan=9, columnspan=12, padx=10, sticky="nsew")
        #Configure grid
        self.frame_main_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1)
        self.frame_main_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11), weight=1)

        #Create main frame for the buttons
        self.frame_buttons = customtkinter.CTkFrame(master=self,
                                                    height=3,
                                                    corner_radius=10,)
                                                    #fg_color="blue")
        self.frame_buttons.grid(row=10, column=0, rowspan=3, columnspan=12, padx=10, pady=10, sticky="nsew")
        #Configure grid
        self.frame_buttons.grid_columnconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8), weight=1)
        self.frame_buttons.grid_rowconfigure((0, 1), weight=1)


        #Buttons

        #Video lenght
        self.time_var = DoubleVar()
        self.time_slider_last = 0
        self.time_slider_update = time()
        self.slider_video_duration = customtkinter.CTkSlider(master=self.frame_buttons,
                                            from_=0, to=1000,
                                            height=30,
                                            command=self._on_time,
                                            variable=self.time_var)
        self.slider_video_duration.grid(row=0, column=0, columnspan=9, padx=10, pady=10, sticky="ew")

        #play button
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Images")
        print(image_path)
        click__play_btn = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "play.png")),
                                            light_image=Image.open(os.path.join(image_path, "play_dark.png")),
                                            size=(30, 30))
        self.play_button = customtkinter.CTkButton(master=self.frame_buttons,
                                                width=1,
                                                height=1,
                                                corner_radius=5,
                                                fg_color = "transparent",
                                                image=click__play_btn,
                                                hover= False,
                                                text="",
                                                command=self._play_btn)
        self.play_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        #pause button
        click__pause_btn = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "pause.png")),
                                            light_image=Image.open(os.path.join(image_path, "pause_dark.png")),
                                            size=(30, 30))
        self.pause_button = customtkinter.CTkButton(master=self.frame_buttons,
                                                width=1,
                                                height=1,
                                                corner_radius=5,
                                                fg_color = "transparent",
                                                image=click__pause_btn,
                                                hover= False,
                                                text="",
                                                command=self._pause_btn)
        #self.pause_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        #stop button
        click__stop_btn = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "stop.png")),
                                            light_image=Image.open(os.path.join(image_path, "stop_dark.png")),
                                            size=(30, 30))
        self.stop_button = customtkinter.CTkButton(master=self.frame_buttons,
                                                width=1,
                                                height=1,
                                                corner_radius=5,
                                                fg_color = "transparent",
                                                image=click__stop_btn,
                                                hover= False,
                                                text="",
                                                command=self._stop_btn)
        self.stop_button.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        #search button
        click__search_btn = customtkinter.CTkImage(dark_image=Image.open(os.path.join(image_path, "search.png")),
                                            light_image=Image.open(os.path.join(image_path, "search_dark.png")),
                                            size=(30, 30))
        self.search_button = customtkinter.CTkButton(master=self.frame_buttons,
                                                width=1,
                                                height=1,
                                                corner_radius=5,
                                                fg_color = "transparent",
                                                image=click__search_btn,
                                                hover= False,
                                                text="",
                                                command=self._search_btn)
        self.search_button.grid(row=1, column=7, padx=10, pady=10, sticky="nsew")

        #download button
        click__download_btn = customtkinter.CTkImage(
                                            dark_image=Image.open(os.path.join(image_path, "save.png")),
                                            light_image=Image.open(os.path.join(image_path, "save_dark.png")),
                                            size=(30, 30))
        self.download_button = customtkinter.CTkButton(master=self.frame_buttons,
                                                width=1,
                                                height=1,
                                                corner_radius=5,
                                                fg_color = "transparent",
                                                image=click__download_btn,
                                                state="disabled",
                                                hover= False,
                                                text="",
                                                command=lambda: Thread(target=self._download_btn).start())
        self.download_button.grid(row=1, column=8, padx=10, pady=10, sticky="nsew")

        #volumen slider
        self.volume_var = IntVar(value=100)
        self.slider_volumen = customtkinter.CTkSlider(master=self.frame_buttons,
                                            from_=0, to=100,
                                            variable=self.volume_var,
                                            command=self._volume)
        self.slider_volumen.grid(row=1, column=2, padx=10, pady=10, sticky="ew")
        self.slider_volumen.set(100)

        #search on youtube entry
        self.entry_search = customtkinter.CTkEntry(master=self.frame_buttons,
                                                font=("arial", 14),
                                                corner_radius=10,
                                                width=650,
                                                height=30,
                                                border_width=1,
                                                placeholder_text="Search on Youtube",)
        self.entry_search.grid(row=1, column=3, columnspan=3, padx=10, pady=10)
        self.entry_search.bind('<Return>', self._search_btn)

        # load image
        self._load_from_database()
    
    #################################################################
    ############# Load and save background image if any #############
    #################################################################
    
    def _load_from_database(self) -> None:
        """Tries to load a image from the database if exists"""
        if bg_path := self.image_db.get_image():
            self._show_bg_image(bg_path)
    
    def _select_background_image(self) -> None:
        """Opens a window that allows the user select an image"""
        # Open file
        selected_image = askopenfilename(filetypes = IMAGE_EXTENSIONS, title = "Choose your Background image")
        # select and uptdate the background image
        self.image_db.save_image(selected_image)
        self._show_bg_image(selected_image)
    
    def _show_bg_image(self, selected_image: str) -> None:
        """Shows the selected image in the app background"""
        self.image = selected_image
        self.bg_image = PIL.Image.open(self.image)
        width = 1160
        height = 430
        self.bg_image = self.bg_image.resize((width, height)) # width 1160 height 430
        self.bg_image = customtkinter.CTkImage(self.bg_image, size=(1160, 430))
        self.display = customtkinter.CTkLabel(self.frame_main_frame, text="", image=self.bg_image)
        #self.display.place(x=0, y=0)
        self.display.grid(column=0, row=0, columnspan=12, rowspan=12, sticky="nsew")
    
    def _video_file(self) -> None:
        """Opens a window asking the user to select a file and then reproduces it in the app"""
        filetypes = (
            ("Media Files", " ".join([*SUPPORTED_VIDEO, *SUPPORTED_AUDIO])),
            ("All Files", "*.*")
        )
        selected_video = askopenfilename(filetypes=filetypes, title = "Choose your file")
        if "mp4" in selected_video or "webm" in selected_video or "mpg" in selected_video or "mkv" in selected_video or "flv" in selected_video:
            self._vlc_video(selected_video)
        elif "mp3" in selected_video or "ogg" in selected_video or "wav" in selected_video:
            self._vlc_audio(selected_video)

    ##################################################################
    ################# methods related to the buttons #################
    ##################################################################

    # Play button
    def _play_btn(self) -> None:
        """Plays the current media"""
        self._is_playing()
        self.media_manager.play()

    # Pause button
    def _pause_btn(self) -> None:
        """Pauses the current media"""
        self._is_playing()
        self.media_manager.pause()
    
    #Stop button
    def _stop_btn(self) -> None:
        """Stops the current media and shows the background again"""
        self.media_manager.stop()
        self.download_button.configure(state="disabled")
        self.slider_video_duration.set(0)
        self._load_from_database()

    # Search button
    def _search_btn(self, *key_event) -> None:
        """Takes the input and makes a search on youtube"""
        if self.entry_search.get() != "":
            try:
                self._stop_btn()
                self.display.grid_forget()
            except:
                pass
            self.url = str(self.entry_search.get())

            if "https://www.youtube.com" in self.url:
                Thread(target=self._youtube_selector(self.url, "video")).start()
            else:    
                thread = Thread(target=self._list_of_searched_videos())
                thread.start()
                thread.join
        else:
            pass
    
    # Update the volume with the scale
    def _volume(self, *args) -> None:
        """Uodates the volume scale with the current value"""
        volume = self.volume_var.get()
        if volume > 100:
            volume = 100
        self.media_manager.volume_scale(volume)

    # Methods related to the scale of the video duration
    
    def _on_tick(self) -> int:
        """Gets and corrects the scale related to the duration of the current audio or video"""
        if self.media_manager.player:
            player = self.media_manager.player
            lenght = player.get_length() * 1e-3  # to seconds
            if lenght > 0:
                self.slider_video_duration.configure(to=lenght)

                t = player.get_time() * 1e-3  # to seconds
                if t > 0 and time() > (self.time_slider_update + 2):
                    self.slider_video_duration.set(t)
                    self.time_slider_last = int(self.time_var.get())

                    if self.time_var.get() + 0.1 >= lenght:
                        self._stop_btn()
                        return 0
        self.after(100, self._on_tick)


    def _on_time(self, *unused) -> None:
        """No idea, this is a hack that I found on the internet lol"""
        if self.media_manager.player:
            player = self.media_manager.player
            t = self.time_var.get()
            if self.time_slider_last != int(t):
                player.set_time(int(t * 1e3))
                self.time_slider_update = time()
    
    '''def update_video_slider(self, t):
        """Stops the media player once the media ends the video scale, unused for now, maybe in the future..."""
        if self.slider_video_duration.get() == t:
            self._stop_btn()'''

    ######################################################################
    ################ method related to the Download function #############
    ######################################################################

    #  Download button
    def _download_btn(self) -> None:
        """Downloads the current video or audio"""
        self.yt_manager.download(self.id_or_url, self.current_media)

    ######################################################################
    # methods related to the vlc instance and playing the video or audio #
    ######################################################################
    
    def _list_of_searched_videos(self) -> None:
        """Creates a new frame and shows the tittle, video and audio of a list of videos searched on Youtube.
        Note, need to show the video thumbnail in the future."""
        try:
            self.display.grid_forget()
            self.frame_display.grid_forget()
        except:
            pass
        videos_to_search = self.url
        youtube_search = self.yt_manager.search(videos_to_search)
        video_id, video_title, video_live = zip(*youtube_search)
        video_id = list(video_id)
        video_title = list(video_title)
        del video_live

        title_and_id = list(zip(video_title, video_id))

        self.frame_display = customtkinter.CTkFrame(self.frame_main_frame, width=1170, height=500)
        self.frame_display.grid(column=0, row=0, columnspan=12, rowspan=12)
        self.frame_display.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.frame_display.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9), weight=1)

        count = 0
        for elements in title_and_id:
            label_video_name = customtkinter.CTkLabel(master=self.frame_display,
                                                            text=elements[0],
                                                            wraplength=600,
                                                            #text_color="silver",
                                                            font=("arial", 14))
            label_video_name.grid(row=count, column=0, pady=10, padx=5)


            play_video_btn = customtkinter.CTkButton(master=self.frame_display,
                                                        text="Video",
                                                        #height=35,
                                                        #width=45,
                                                        font=("arial", 14),
                                                        command=lambda elements = elements[1]: Thread(target=self._youtube_selector(elements, "video")).start())
            play_video_btn.grid(row=count, column=1, pady=10, padx=5)

            play_video_btn = customtkinter.CTkButton(master=self.frame_display,
                                                        text="Audio",
                                                        #height=35,
                                                        #width=45,
                                                        font=("arial", 14),
                                                        command=lambda elements = elements[1]: Thread(target=self._youtube_selector(elements, "audio")).start())
            play_video_btn.grid(row=count, column=2, pady=10, padx=5)
            
            count += 1
    
    def _youtube_selector(self, id_or_url, video_or_audio: str) -> None:
        """Selects if the media is a video or an audio"""
        self.id_or_url = id_or_url
        self.download_button.configure(state="normal")
        self.current_media = None # used for the _download_btn function

        if video_or_audio == "video":
            video = self.yt_manager.get_stream_url(id_or_url, "best")
            self.current_media = "best"
            self._vlc_video(video)
        elif video_or_audio == "audio":
            self.current_media = "bestaudio"
            audio = self.yt_manager.get_stream_url(id_or_url, "bestaudio")
            self._vlc_audio(audio)
            
    def _vlc_video(self, video) -> None:
        """Shows the video in the current main frame"""
        # vlc instance
        self.frame_display = ttk.Frame(self.frame_main_frame, width=1170, height=480)
        self.frame_display.grid(column=0, row=0, columnspan=12, rowspan=12)

        self._on_tick()
        self.media_manager.video(self.frame_display, video)
        self._volume()
        self._play_btn()
        self._is_playing()

    # Show an instance of an audio
    def _vlc_audio(self, audio) -> None:
        """Plays the audio"""
        try:
            self.frame_display.grid_forget()
            self.display.grid(column=0, row=0, columnspan=12, rowspan=12, sticky="nsew")
        finally:    
            # Playing the audio
            self._on_tick()
            self.media_manager.audio(audio)
            self._volume()
            self._play_btn()
            self._is_playing()
    
    def _is_playing(self) -> None:
        """Check if a video or audio is currently playing"""
        if self.media_manager.media_player_is_playing() == True:
            self.play_button.grid_forget()
            self.pause_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        else:
            self.pause_button.grid_forget()
            self.play_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

if __name__ == "__main__":
    app = PyPlayer()
    app.eval('tk::PlaceWindow . center')
    app.mainloop()