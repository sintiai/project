import sqlite3
import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
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
    full_path = os.path.join(base_path, 'music.db')
    conn = sqlite3.connect(full_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS Artists (
                 artist_id INTEGER PRIMARY KEY,
                 artist_name TEXT,
                 UNIQUE(artist_id, artist_name))''')   
    c.execute('''CREATE TABLE IF NOT EXISTS tracks (
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
    full_path = os.path.join(base_path, 'music.db')
    conn = sqlite3.connect(full_path)
    c = conn.cursor()
    
    for artist in artist_list:
        tracks = get_top_tracks(artist)
        for track in tracks:
            try:
                c.execute("INSERT INTO TopTracks (artist_name, track_name) VALUES (?, ?)", track)
            except sqlite3.IntegrityError:
                pass
    
    conn.commit()
    conn.close()


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
