import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
client_id = "8c279de418d9430296bbb01fbabd6dd6"
client_secret = "2d383ce0756348e5b96748c6d64aa270"
client_credentials_manager = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager) #uses personal key to give data
