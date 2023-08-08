import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Input your data from Spotify Developer Dashboard https://developer.spotify.com/dashboard
client_id = 'put here your client ID'
client_secret = 'put here your client secret'
redirect_uri = 'http://localhost:8080'  # your redirect (if case of your local machine just keep exist url

# Clear timings from list in file: delete chars before "-", included
with open('track_list.txt', 'r') as file:
    lines = file.readlines()

new_lines = [line.split('- ', 1)[1] if '- ' in line else line for line in lines]

with open('track_list.txt', 'w') as file:
    file.writelines(new_lines)

# Spotify Autorization
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope='playlist-modify-public playlist-modify-private'))

# Read list of tracks from file
with open('track_list.txt', 'r') as file:
    track_list = file.read().splitlines()

# Creating playlist
playlist_name = input("Enter playlist name: ")
user_id = sp.current_user()['id']
playlist = sp.user_playlist_create(user_id, playlist_name)

# Search and add tracks with logging output
totalCount, added, notAdded = 0, 0, 0
for track in track_list:
    artist, track_name = track.split(" - ")
    results = sp.search(q=f"artist:{artist} track:{track_name}", type='track')
    if results['tracks']['items']:
        track_uri = results['tracks']['items'][0]['uri']
        sp.playlist_add_items(playlist['id'], [track_uri])
        added += 1
        totalCount += 1
        print(f'OK: found and add <{track}> ')
    else:
        notAdded += 1
        totalCount += 1
        print(f"WARN: not found <{track}>")

print(f"Playlist '{playlist_name}' was created and filled successfully.")
print(f"Total tracks: {totalCount}")
print(f"Added tracks: {added}")
print(f"Not added tracks: {notAdded}")
