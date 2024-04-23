import sqlite3
import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
import matplotlib.pyplot as plt
import pandas as pd




client_id = "8c279de418d9430296bbb01fbabd6dd6"
client_secret = "2d383ce0756348e5b96748c6d64aa270"
client_credentials_manager = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager) #uses personal key to give data
artist_list = ["Taylor Swift", "Adele", "Drake", "Bad Bunny", "Doja Cat", "Bruno Mars", "Dolly Parton", "Sabrina Carpenter", "Lady Gaga", "Ariana Grande"]


def get_top_tracks(artist_name):
   result = sp.search(artist_name, type='artist')
   if len(result['artists']['items']) > 0:
       artist_id = result['artists']['items'][0]['id']
       top_tracks = sp.artist_top_tracks(artist_id, country='US')
       tracks_info = [(track['name'], track['popularity']) for track in top_tracks['tracks']]
       return tracks_info
   else:
       print(f"No artist found for {artist_name}")
       return []




def create_database():
   base_path = os.path.abspath(os.path.dirname(__file__))
   full_path = os.path.join(base_path, 'combined.db')
   conn = sqlite3.connect(full_path)
   c = conn.cursor()
   c.execute('''CREATE TABLE IF NOT EXISTS Artists (
                artist_id INTEGER PRIMARY KEY,
                artist_name TEXT,
                UNIQUE(artist_id, artist_name))''')  
   c.execute('''CREATE TABLE IF NOT EXISTS TopTracks (
                track_id INTEGER PRIMARY KEY,
                track_name TEXT,
                artist_id INTEGER,
                popularity INTEGER


   )''')
   conn.commit()
   conn.close()




def store_data(artist_list):
   client_id = "8c279de418d9430296bbb01fbabd6dd6"
   client_secret = "2d383ce0756348e5b96748c6d64aa270"
   client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
   sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
  
  
   base_path = os.path.abspath(os.path.dirname(__file__))
   full_path = os.path.join(base_path, 'combined.db')
   conn = sqlite3.connect(full_path)
   c = conn.cursor()
   track_count=0
   for artist in artist_list:
       #Insert or ignore each artist into the artist table
       c.execute("INSERT OR IGNORE INTO Artists (artist_name) VALUES (?)", (artist,))
       c.execute("SELECT COUNT(*) FROM TopTracks WHERE artist_id = (SELECT artist_id FROM Artists WHERE artist_name = ?)", (artist,))
       track_count = c.fetchone()[0]
       tracks = get_top_tracks(artist)
       for track in tracks:
           if track_count >= 25:  # Limit to 25 tracks per artist
               break
           song_name = track[0]
           popularity = track [1]
           # Find the ID associated with the artist (SELECT statement into artist table)
           artist_id = c.execute("SELECT artist_id FROM Artists WHERE artist_name = ? ", (artist,))
           artist_id = c.fetchone()[0]
           print("This is track ",track)
           print("by ", artist)
           try:
                c.execute("INSERT INTO TopTracks (artist_id, track_name, popularity ) VALUES (?, ?,? )", (artist_id,song_name,popularity))
                track_count += 1
           except sqlite3.IntegrityError:
               pass
  
   conn.commit()
   conn.close()
def calculate_average_popularity_by_artist():
   conn = sqlite3.connect('combined.db')
   c = conn.cursor()
   c.execute("SELECT Artists.artist_name, AVG(TopTracks.popularity) FROM TopTracks JOIN Artists ON TopTracks.artist_id = Artists.artist_id GROUP BY Artists.artist_name")
   average_popularity_by_artist = c.fetchall()
   conn.close()
   return average_popularity_by_artist


def write_to_file(data, filename):
   with open(filename, 'w') as file:
       for item in data:
           file.write(f"{item}\n")
    
#     client_id = "8c279de418d9430296bbb01fbabd6dd6"
# client_secret = "2d383ce0756348e5b96748c6d64aa270"
# client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
# sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
# base_path = os.path.abspath(os.path.dirname(__file__))
# full_path = os.path.join(base_path, 'combined.db')
# conn = sqlite3.connect(full_path)
    
# def create_artist_table():
#     c = conn.cursor()
#     track_count=0
#     for artist in artist_list:
#             #Insert or ignore each artist into the artist table
#             c.execute("INSERT OR IGNORE INTO Artists (artist_name) VALUES (?)", (artist,))
#             c.execute("SELECT COUNT(*) FROM TopTracks WHERE artist_id = (SELECT artist_id FROM Artists WHERE artist_name = ?)", (artist,))
#             track_count = c.fetchone()[0]
#             tracks = get_top_tracks(artist)
#             for track in tracks:
#                 if track_count >= 25:  # Limit to 25 tracks per artist
#                     break
#                 song_name = track[0]
#                 popularity = track [1]
#                 # Find the ID associated with the artist (SELECT statement into artist table)
#                 artist_id = c.execute("SELECT artist_id FROM Artists WHERE artist_name = ? ", (artist,)) 
#                 artist_id = c.fetchone()[0]
#                 try:
#                     c.execute("INSERT INTO TopTracks (artist_id, track_name, popularity ) VALUES (?, ?,? )", (artist_id,song_name,popularity))
#                     track_count += 1
#                 except sqlite3.IntegrityError:
#                     pass
        
#     conn.commit()
#     conn.close()
    
def graph_spotify():
   df = pd.read_csv('spotify_calculations.csv')
   df.plot.bar(x='Artist Name', y='Average Rating', color='pink')
   plt.show()


def main():
   create_database()
# Retrieve top tracks and their popularity for each artist
   for artist in artist_list:
       print(f"Top tracks for {artist}:")
       tracks = get_top_tracks(artist)
       if tracks:
           for track, popularity in tracks:
               print(f"{track} - Popularity: {popularity}")
       else:
           print("No tracks available.")
       print()


   store_data(artist_list)
  




if __name__ == "__main__":
   main()
#adding this to create a commit
