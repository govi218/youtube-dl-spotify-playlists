from __future__ import unicode_literals
import urllib.request
import re

import youtube_dl
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def init_spotipy(client_id, client_secret):
    '''
    Initialize spotipy with Spotify developer credentials.
    Can be found here: https://developer.spotify.com/dashboard/
    client_id - Your client ID
    client_id - Your client secret
    '''
    auth_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)
    return sp

def get_playlist_names(sp, user_id):
    '''
    Get names of all playlists followed by a user.
    sp - Spotipy obj
    user_id - Spotify ID of the user
    '''
    playlists = sp.user_playlists(user_id)
    ret = []
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            ret.append(playlist['name'])
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    return ret

def get_playlist_ids(sp, user_id):
    '''
    Get ids of all playlists followed by a user.
    sp - Spotipy obj
    user_id - Spotify ID of the user
    '''
    playlists = sp.user_playlists(user_id)
    ret = []
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            ret.append(playlist['id'])
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    return ret

def get_songs_in_playlist(sp, p_id):
    '''
    Get songs in a playlist.
    sp - Spotipy obj
    p_id - ID of the playlist
    '''
    get_track_name = lambda p,idx: p['tracks']['items'][idx]['track']['name']+ ' ' + p['tracks']['items'][idx]['track']['artists'][0]['name']
    p = sp.playlist(p_id)
    tracks = [get_track_name(p, i) for i in range(len(p['tracks']['items']))]
    return tracks

def get_yt_audio(url):
    '''
    Gets audio for a youtube video as an MP3 file. Saved in 
    current folder.
    url - URL of youtube video.
    '''
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            # 'outtmpl': '%(title)s-%(id)s.%(ext)s',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def find_yt_video(search_str):
    '''
    Find a youtube video with a search string. Returns 
    the first search result.
    search_str - keywords separated by space
    '''
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_str.replace(' ', '+'))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return "https://www.youtube.com/watch?v=" + video_ids[0]