import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
from datetime import datetime

scope = 'playlist-read-private'
username = '11126440604'

P_TEMPTEMP_ID = '4IxcD4CCUZIdQfnP90Ydn8'
P_JUODRASTIS_ID = '7oI6ZI9MKa3J6OadquB6iu'
P_VALANDELE_ID = '59XmFOcKm77AeQXNvnzluT'
P_VISOSVALAND_ID = '7MwrKkYS3tSyrqiAbbUQuO'

menesiai = ['Sausio', 'Vasario', 'Kovo', 'Balandžio', 'Gegužės', 'Birželio',
            'Liepos', 'Rugpjūčio', 'Rugsėjo', 'Spalio', 'Lapkričio', 'Gruodžio']

def read_playlists():
    '''Print all user's playlists and its IDs'''
    results = spotifyObject.current_user_playlists()
    for i, item in enumerate(results['items']):
        print('{} {} {}'.format(i, item['name'], item['id']))
        # print(json.dumps(i,indent=4))

def read_track_json(track_json):
    '''From Spotify Track API json return artist name, track name and track ID'''
    track_name = track_json['name']
    t_id = track_json['id']

    artist_list = []
    for artists in track_json['artists']:
        artist = artists['name']
        artist_list.append(artist)

    return [artist_list, track_name, t_id]

def track_string(track_json):
    '''Return a string from a read_track_json list'''
    track = read_track_json(track_json)
    return ', '.join(track[0]) + '-' + track[1] + ' (' + track[2] + ')'


def read_tracks(p_id, print_names=False):
    '''Return playlist's track IDs and print track names'''
    results = spotifyObject.playlist(p_id, fields='tracks')

    t_ids = []
    for item in results['tracks']['items']:
        track_info = read_track_json(item['track'])
        t_ids.append(track_info[2])
        if print_names==True: print(track_string(item['track']))
        
    return t_ids

def replace_tracks(p_id, t_ids):
    '''Replace tracks to a playlist'''
    spotifyObject.playlist_replace_items(p_id, t_ids)

def add_tracks(p_id, t_ids):
    '''Add tracks to a playlist'''
    spotifyObject.playlist_add_items(p_id, t_ids)

def remove_tracks(p_id):
    '''Remove all tracks from a playlist'''
    t_ids = read_tracks(p_id)
    spotifyObject.playlist_remove_all_occurrences_of_items(p_id, t_ids)

def rename_playlist(p_id, new_name):
    '''Rename a playlist'''
    spotifyObject.playlist_change_details(p_id, name=new_name)

def matching_songs(p_id1, p_id2):
    '''Check if there are any matching songs between two playlists'''
    t_ids1 = read_tracks(p_id1, print_names=False)
    t_ids2 = read_tracks(p_id2, print_names=False)
    matches = list(set(t_ids1).intersection(t_ids2))
    if not matches: print('There are no matches between these playlists')
    else:
        print('Matching songs between these playlists:')
        for match in matches:
            result = spotifyObject.track(match)
            print(track_string(result))

token = SpotifyOAuth(scope=scope, username=username)
spotifyObject = spotipy.Spotify(auth_manager= token)

# read_playlists() # nuskaitomi visi playlistai
# matching_songs(P_JUODRASTIS_ID, P_VISOSVALAND_ID) # parodo besikartojancias dainas tarp playlistu

# t_ids = read_tracks(P_JUODRASTIS_ID, False) # nuskaitomos dainos is juodrascio
# replace_tracks(P_VALANDELE_ID, t_ids) # pakeiciamos dainos menesio valandeleje
# add_tracks(P_VISOSVALAND_ID, t_ids) # pridedamos dainos i visu valandeliu playlista
# rename_playlist(P_VALANDELE_ID, menesiai[(datetime.now().month)-1]+' valandėlė') #pervadinamas playlistas
remove_tracks(P_JUODRASTIS_ID) # istrinamos visos dainos is playlisto
