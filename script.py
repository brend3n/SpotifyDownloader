# Youtube->Mp3 downloader
from pytube import YouTube

# File handling
import os
import csv

# Webscraping
import requests
from bs4 import BeautifulSoup
from Web_Scrape_Tool.web_scrape_tool import get_soup_adv

# CLI
from alive_progress import alive_bar # Progress bar

# Threading and Utilities
import threading # Multithreading for faster scanning
import random
import urllib3
from time import sleep

# Disable warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

RATE_LIMIT_SLEEP_TIMEOUT = 20 # 20 second delay

class DownloaderThread(threading.Thread):
    backoff_time = 0
    minimum_backoff_time = 1 #second
    MAX_BACKOFF_TIME = 60 # seconds
    
    def __init__(self, chunk, file_name, bar, name, DEBUG) -> None:
        threading.Thread.__init__(self)
        self.chunk = chunk
        self.file_name = file_name
        self.bar = bar
        self.name
        self.DEBUG = DEBUG

    def run(self) -> None:
        self.do_process()

    def backoff(self):
        if(self.minimum_backoff_time > self.MAX_BACKOFF_TIME):
            return
        else:
            delay = self.minimum_backoff_time + random.randint(0,1000) / 1000.0

            print(f"Thread: {self.name} backoff: {delay}")

            sleep(delay)

            self.minimum_backoff_time *= 2

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

    def search_for_song(self, song_string: str):
        youtube_url = ""
        youtube_links = []

        # Creating search string
        base_search_string = f"https://www.google.com/search?q=site:youtube.com+{song_string}"

        # Making request
        soup = get_soup_adv(base_search_string)

        # check if soup had bad response status code
        if (soup is None):
            # wait a bit before trying again
            self.backoff()
            return None

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

        youtube_url = self.get_most_viewed_song(youtube_links)

        return youtube_url

    # Gaurantees a not None URL
    def retrieve_song(self, song: str):
        url = ""
        res = False

        while(res == False):
            try:
                url = self.search_for_song(song)
                if (url is None):
                    raise Exception
            except Exception:
                continue
            
            if url is None:
                continue
            else:
                res = True

        return url

    def do_process(self):
        for song in self.chunk:
            url = self.retrieve_song(song)
            self.download(url, self.file_name)
            sleep(5) # rate limit
            self.bar()

# Convert Songs to dictionary from CSV file
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

# Partitioning data for each thread
def chunkify(lst,n):
    return [lst[i::n] for i in range(n)]

# Start the threads
def launch_threads(prog_bar_obj, num_threads, all_links, file_name: str, DEBUG: int):
    
    # Divide chunks of webpages to each thread
    chunks = chunkify(all_links, num_threads)
    
    # Holds the Thread objects
    threads = []
    
    # Give each thread webpages
    for i in range(num_threads):
        t = DownloaderThread(chunks[i], file_name, prog_bar_obj, str(i), DEBUG)
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

def main():
    
    choice = int(input("1. Enter URL\n2. Find single song\n3. Read from file\n"))
    file_name = input("Enter folder name to store songs(mp3) or just press Enter for default folder (DownloadedSongs): ")
    DEBUG = int(input("Enter 1 for DEBUG, else no DEBUG\n"))
    
    if (choice == 1):
        # Enter filetype somewhere else, maybe use simple term
        url = input("Enter a url: ")
        t_thread = DownloaderThread()
        t_thread.download(song, file_name)
    elif (choice == 2):
        song = input("Enter song: ")
        t_thread = DownloaderThread()
        url = t_thread.retrieve_song(song)
        t_thread.download(url,file_name)
    elif (choice == 3):
        num_threads = int(input("Enter number of threads to use: "))
        # file_name = input("BRENDEN enter CSV instructions at some point")
        list_of_songs = read_from_csv("spotlistr-exported-playlist.csv")
        print("Total songs: " + str(len(list_of_songs)))
        with alive_bar(len(list_of_songs), dual_line=True, title='Downloading') as bar:
            launch_threads(bar, num_threads, list_of_songs, file_name, DEBUG)
if __name__ == "__main__":
    # Need to figure out rate limiting
    main()