from turtle import down
from jmespath import search
from pytube import YouTube
import os
import csv

"""
GET https://convert2mp3s.com/api/button/{FTYPE}?url={VIDEO_URL}
Parameters
FTYPE
mp3, mp4, webm
VIDEO_URL"""

def download(url_: str):
    if(url_ == ""):
        return
    # url input from user
    yt = YouTube(url_)
    
    # extract only audio
    video = yt.streams.filter(only_audio=True).first()
    
    # check for destination to save file
    print("Enter the destination (leave blank for current directory)")
    destination = "./DownloadedSongs/"
    
    # download the file
    out_file = video.download(output_path=destination)
    
    # save the file
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    
    # result of success
    print(yt.title + " has been successfully downloaded.")

def search_for_song(song_string: str):
    print(f"Searching for: {song_string}")
    base_search_string = f"site: www.youtube.com intitle:{song_string}"
    pass

def read_from_csv(file_name: str):
    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)
def main():
    
    choice = int(input("1. Enter URL\n2. Find single song\n3. Read from file\n"))

    if (choice == 1):
        # Enter filetype somewhere else, maybe use simple term
        url = input("Enter a url: ")
        download(url)
    elif (choice == 2):
        song = input("Enter song: ")
        url = search_for_song(song)
        download(url)
    elif (choice == 3):
        file_name = input("BRENDEN enter CSV instructions at some point")
        list_of_songs = read_from_csv("spotlistr-exported-playlist.csv")
        # for song in list_of_songs:
        #     url = search_for_song(song)
        #     download(song)
if __name__ == "__main__":
    main()