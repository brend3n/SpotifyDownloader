from pytube import YouTube
import os
import csv
import requests
from bs4 import BeautifulSoup
from Web_Scrape_Tool.web_scrape_tool import get_soup_adv
from alive_progress import alive_bar # Progress bar
import threading # Multithreading for faster scanning

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

    print(f"Searching for: {song_string}")

    # Creating search string
    base_search_string = f"https://www.google.com/search?q=site:youtube.com+{song_string}"

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
        sleep(5)
        try:
            url = search_for_song(song)
        except Exception:
            continue
        
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
            string = f"{row_dict[ARTIST_NAME]}{row_dict[TRACK_NAME]}{row_dict[ALBUM_NAME]}" # make search string
            string = string.replace(";", "")
            string = string.replace(" ", "+")
            # print(string) # Debugging
            list_of_strings.append(string)
    return list_of_strings

# Used for making chunks
def chunkify(lst,n):
    return [lst[i::n] for i in range(n)]

# Use threads to speed up scanning
def launch_threads(prog_bar_obj, num_threads, all_links, file_name):
    
    # Divide chunks of webpages to each thread
    chunks = chunkify(all_links, num_threads)
    
    # Holds the Thread objects
    threads = []
    
    # Give each thread webpages
    for i in range(num_threads):
        t = threading.Thread(name=f"Thread {i}", target=do_process, args=(chunks[i],file_name,prog_bar_obj,) )
        t.setDaemon(True)
        threads.append(t)
    
    # Start threads
    print(f"Starting {num_threads} threads.")
    for i in range(num_threads):
        threads[i].start()
    
    # Join threads
    # ! If this is excluded, it breaks code
    for i in range(num_threads):
        threads[i].join()

def do_process(chunk_of_songs, file_name, bar):
    for song in chunk_of_songs:
        url = retrieve_song(song)
        download(url,file_name)
        sleep(5) # rate limit
        bar()

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
        num_threads = int(input("Enter number of threads to use: "))
        # file_name = input("BRENDEN enter CSV instructions at some point")
        list_of_songs = read_from_csv("spotlistr-exported-playlist.csv")
        print("Total songs: " + str(len(list_of_songs)))
        with alive_bar(len(list_of_songs), dual_line=True, title='Downloading') as bar:
            launch_threads(bar, num_threads, list_of_songs, file_name)
if __name__ == "__main__":
    # Need to figure out rate limiting
    main()