pip3 install spotipy
import spotipy
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
        top_tracks = sp.artist_top_tracks(artist_id, country='US')  # Change country code if necessary
        return [track['name'] for track in top_tracks['tracks']]
    else:
        print(f"No artist found for {artist_name}")
        return []

# Retrieve top tracks for each artist
for artist in artist_list:
    print(f"Top tracks for {artist}:")
    tracks = get_top_tracks(artist)
    if tracks:
        for track in tracks:
            print(track)
    else:
        print("No tracks available.")
    print()
