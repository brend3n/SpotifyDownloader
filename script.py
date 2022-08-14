from turtle import down
from pytube import YouTube
import os
import csv
import requests
from bs4 import BeautifulSoup
from Web_Scrape_Tool.web_scrape_tool import get_soup_adv
from alive_progress import alive_bar # Progress bar

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from time import sleep


"""
GET https://convert2mp3s.com/api/button/{FTYPE}?url={VIDEO_URL}
Parameters
FTYPE
mp3, mp4, webm
VIDEO_URL
"""
# Enums for CSV file
ARTIST_NAME = 'Arist(s) Name'
TRACK_NAME  = 'Track Name'
ALBUM_NAME  = 'Album Name'
LENGTH      = 'Length'
SPOTIFY_ID  = 'SpotifyID'
IRSC        = 'ISRC'

# I copied most of this code from somewhere else
def download(url_: str, file_name_: str):
    if(url_ == ""):
        return
    # url input from user
    yt = YouTube(url_)
    
    # extract only audio
    video = yt.streams.filter(only_audio=True).first()

    destination = file_name_ if file_name_ != "" else "./DownloadedSongs/"
    
    # download the file
    out_file = video.download(output_path=destination)
    
    # save the file
    base, ext = os.path.splitext(out_file)
    new_file = base + '.mp3'
    os.rename(out_file, new_file)
    
    # result of success
    print(yt.title + " has been successfully downloaded.")

# TODO: Find the most viewed song
def get_most_viewed_song(links):

    if (len(links) > 0):
        return links[0]
    else:
        return

def search_for_song(song_string: str):
    youtube_url = ""
    youtube_links = []

    # print(f"Searching for: {song_string}")

    # Creating search string
    base_search_string = f"https://www.google.com/search?q=site: www.youtube.com intitle:{song_string}"

    # Making request
    soup = get_soup_adv(base_search_string)

    links = soup.find_all('a', href=True)

    # Getting all youtube links
    for youtube_link in links:
        href = youtube_link['href'] # get links
        if "https://www.youtube.com/watch?" not in href: # Not a youtube link
            continue
        else:
            youtube_links.append(href)

    # Remove duplicates
    youtube_links = list(set(youtube_links))

    youtube_url = get_most_viewed_song(youtube_links)

    return youtube_url

# Gaurantees a not None URL
def retrieve_song(song):
    url = ""
    res = False

    while(res == False):
        url = search_for_song(song)
        if url is None:
            continue
        else:
            res = True

    return url
def read_from_csv(file_name: str):
    list_of_strings = []
    with open(file_name, 'r') as file:
        reader = csv.DictReader(file) # allows each row to be dictionary
        for row in reader:
            row_dict = dict(row) # get dictionary of row 
            string = f"{row_dict[ARTIST_NAME]} {row_dict[TRACK_NAME]} {row_dict[ALBUM_NAME]}" # make search string
            # print(string) # Debugging
            list_of_strings.append(string)
    return list_of_strings

def main():
    
    choice = int(input("1. Enter URL\n2. Find single song\n3. Read from file\n"))
    file_name = input("Enter folder name to store songs(mp3) or just press Enter for default folder (DownloadedSongs): ")

    if (choice == 1):
        # Enter filetype somewhere else, maybe use simple term
        url = input("Enter a url: ")
        download(song, file_name)
    elif (choice == 2):
        song = input("Enter song: ")
        url = retrieve_song(song)
        download(url,file_name)
    elif (choice == 3):
        file_name = input("BRENDEN enter CSV instructions at some point")
        list_of_songs = read_from_csv("spotlistr-exported-playlist.csv")
        print("Total songs: " + str(len(list_of_songs)))
        with alive_bar(len(list_of_songs), dual_line=True, title='Downloading') as bar:
            for song in list_of_songs:
                url = retrieve_song(song)
                download(url,file_name)
                # sleep(1) # rate limit
                bar()
if __name__ == "__main__":
    main()