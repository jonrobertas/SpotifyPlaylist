import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

scope = 'playlist-modify-public'
username = '11126440604'

token = SpotifyOAuth(scope=scope, username=username)
spotifyObject = spotipy.Spotify(auth_manager= token)

#create the playlist
playlist_name = input('Enter a playlist name: ')
playlist_desc = input('Enter a playlist desc: ')

spotifyObject.user_playlist_create(user=username,
                                   name=playlist_name,
                                   public=True,
                                   description=playlist_desc)

user_input = input('Enter a song: ')
list_of_songs = []

while user_input != 'quit':
    result = spotifyObject.search(q=user_input)
    # print(json.dumps(result, sort_keys=4, indent=4))
    list_of_songs.append(result['tracks']['items'][0]['uri'])
    user_input = input('Enter a song: ')

#find the new playlist
prePlaylist = spotifyObject.user_playlists(user=username)
playlist = prePlaylist['items'][0]['id']

#add songs
spotifyObject.user_playlist_add_tracks(user=username,
                                       playlist_id=playlist,
                                       tracks=list_of_songs)