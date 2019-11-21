# importing the module
from pytube import YouTube
import os


# where to save
SAVE_PATH = "downloads"  # to_do

# link of the video to be downloaded
link = "https://www.youtube.com/watch?v=v9ZzcKZJCa0"


def main():
    if not os.path.exists(SAVE_PATH):
        os.mkdir(SAVE_PATH)
    try:
        # object creation using YouTube which was imported in the beginning
        yt = YouTube(link)
    except:
        print("Connection Error")  # to handle exception

    # filters out all the files with "mp4" extension
    stream = yt.streams.first()

    stream.download('.\downloads')


if __name__ == "__main__":
    main()
