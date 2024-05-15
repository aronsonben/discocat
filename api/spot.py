import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def spot(uri):
    # artist_uri = f'spotify:artist:{uri}'
    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    # Can get attributes like: genres, external_urls['spotify'] (link to Spotify), images, type (i.e. artist), popularity
    results = spotify.artist(uri)

    # Return as error if name is not received
    if results['name'] is None or results['id'] is None:
        return False
    
    spot_id = results['id']
    name = results['name']
    followers = results['followers']['total']
    data = {"spotify_id": spot_id, "name": name, "followers": followers}  
    return data

# Uncomment this to run as an independent script
# spot('3TVXtAsR1Inumwj472S9r4')