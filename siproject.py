import requests
from bs4 import BeautifulSoup
import sqlite3
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import json
import pprint

# Spotify API credentials
client_id = '8c279de418d9430296bbb01fbabd6dd6'
client_secret = '2d383ce0756348e5b96748c6d64aa270'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)  # uses personal key to give data

# Connect to SQLite database
conn = sqlite3.connect('music_movies.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS artists
             (id INTEGER PRIMARY KEY, name TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS albums
             (id INTEGER PRIMARY KEY, artist_id INTEGER, name TEXT)''')

# Add more tables as needed (e.g., tracks, movies)

def check_if_artist_exists(name):
    result = sp.search(q='artist:' + name, type='artist')
    return result["artists"]["total"] > 0

def movie_data(movie):
    no_space = movie.replace(" ", "+")
    api_url = f"http://www.omdbapi.com/?t={no_space}&apikey=524429c9"
    response = requests.get(api_url)
    data = json.loads(response.text)
    if data.get('Response', '') == 'True':
        return data
    else:
        return None

def store_artist_data(artist_name):
    c.execute("INSERT INTO artists (name) VALUES (?)", (artist_name,))
    conn.commit()

def store_album_data(artist_id, album_name):
    c.execute("INSERT INTO albums (artist_id, name) VALUES (?, ?)", (artist_id, album_name))
    conn.commit()

def store_movie_data(movie_info):
    # Store movie data in the database
    pass  # Add code to insert movie data into the database

# Input from user
name = input("Enter an artist: ")
movie_title = input("Enter a movie title: ")

# Check if artist exists and store data
if check_if_artist_exists(name):
    store_artist_data(name)
else:
    print("Artist does not exist")

# Retrieve movie data and store if found
movie_info = movie_data(movie_title)
if movie_info:
    store_movie_data(movie_info)
    print("Movie found!")
    pprint.pprint(movie_info)
else:
    print("Movie not found.")

# Close the database connection
conn.close()