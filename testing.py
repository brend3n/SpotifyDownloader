from turtle import down
from jmespath import search
from pytube import YouTube
import os
import csv
"""
first payload:

data: {
        "url":"https://www.youtube.com/watch?v=Q39g89E0CFM",
        "action":"checkYoutubeUrl2"
    }

response:
{
    "status":"ok",
    "id":"Q39g89E0CFM",
    "title":"PROVENZA (Letra\/Lyrics)",
    "filename":"KAROL_G_-_PROVENZA_(Letra\/Lyrics)",
    "duration":863,
    "thumbnail":"https:\/\/i.ytimg.com\/vi_webp\/Q39g89E0CFM\/maxresdefault.webp",
    "youtube_cover":"https:\/\/www.converto.io\/covers\/842\/Q39g89E0CFM_original.jpg",
    "inet_cover":"none",
    "wrong":0,
    "mp4_arr":
    [
        {
            "format":"1080p",
            "class":"hd",
            "format_id":"137",
            "size":"10.8 mb",
            "o_size":11296709
        },
        {
            "format":"720p",
            "class":"hd",
            "format_id":"136",
            "size":"4.3 mb",
            "o_size":4545869
        },
        {
            "format":"480p",
            "class":"hq",
            "format_id":"135",
            "size":"2.7 mb",
            "o_size":2882132
        },
        {
            "format":"360p",
            "class":"sq",
            "format_id":"134",
            "size":"2 mb",
            "o_size":2140745
        },     
        {
            "format":"240p",
            "class":"lq",
            "format_id":"133",
            "size":"1.4 mb",
            "o_size":1466837
        },
        {
            "format":"144p",
            "class":"lq",
            "format_id":"597",
            "size":"0.8 mb",
            "o_size":835122
        }
    ],
    "sel_format":"136",
    "full_title":"KAROL G - PROVENZA (Letra\/Lyrics)","artist":"KAROL G",
    "url_id":"P1iVDOwQAOv0nSm7a7U23rpU0DRGlAs3"}
"""

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