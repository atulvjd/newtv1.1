# modules/spotify_control.py

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from core.speech import speak

CLIENT_ID = '7b1d57914c2b40bd8130c2be277cdd96'
CLIENT_SECRET = 'b3546f6f758f4e9ba9e42d41a164e756'
REDIRECT_URI = 'http://localhost:8888/callback'

SCOPE = 'user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-private user-read-email'
CACHE = ".cache"

# Authenticate
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE,
    cache_path=CACHE
))


# --------------------------- DEVICE HANDLING ---------------------------

def get_active_device_id():
    try:
        devices = sp.devices()
        for d in devices['devices']:
            if d['is_active']:
                return d['id']
        if devices['devices']:
            return devices['devices'][0]['id']
        speak("No active Spotify device found.")
    except Exception as e:
        print(f"[Device Error] {e}")
    return None


def list_devices():
    try:
        devices = sp.devices()
        if not devices['devices']:
            speak("No devices are currently connected to Spotify.")
            return
        speak("Here are your available devices:")
        for d in devices['devices']:
            status = "active" if d['is_active'] else "inactive"
            print(f"🎧 {d['name']} - {status}")
            speak(f"{d['name']}, {status}")
    except Exception as e:
        print(f"[List Devices Error] {e}")
        speak("I couldn’t fetch your Spotify devices.")


# --------------------------- CORE CONTROLS ---------------------------

def play():
    try:
        sp.start_playback(device_id=get_active_device_id())
        speak("Resuming Spotify.")
    except Exception as e:
        print(f"[Play Error] {e}")
        speak("I couldn't start playback.")


def pause():
    try:
        sp.pause_playback()
        speak("Paused Spotify.")
    except Exception as e:
        print(f"[Pause Error] {e}")
        speak("I couldn't pause the music.")


def next_track():
    try:
        sp.next_track()
        speak("Skipped to next track.")
    except Exception as e:
        print(f"[Next Track Error] {e}")
        speak("I couldn't skip the track.")


def previous_track():
    try:
        sp.previous_track()
        speak("Went back to the previous song.")
    except Exception as e:
        print(f"[Previous Track Error] {e}")
        speak("I couldn't go to the previous song.")


# --------------------------- SONG/PLAYLIST SEARCH ---------------------------

def play_song(song_name: str):
    try:
        results = sp.search(q=song_name, type='track', limit=1)
        items = results.get('tracks', {}).get('items', [])
        if items:
            track = items[0]
            uri = track['uri']
            name = track['name']
            artist = track['artists'][0]['name']
            sp.start_playback(device_id=get_active_device_id(), uris=[uri])
            speak(f"Playing {name} by {artist}")
            print(f"🎵 Now playing: {name} — {artist}")
        else:
            speak("I couldn't find that song.")
    except Exception as e:
        print(f"[Play Song Error] {e}")
        speak("Something went wrong while playing the song.")


def play_playlist(playlist_name: str):
    try:
        playlists = sp.current_user_playlists()['items']
        for playlist in playlists:
            if playlist_name.lower() in playlist['name'].lower():
                sp.start_playback(device_id=get_active_device_id(), context_uri=playlist['uri'])
                speak(f"Playing playlist {playlist['name']}")
                return
        speak("Couldn't find that playlist.")
    except Exception as e:
        print(f"[Play Playlist Error] {e}")
        speak("Something went wrong while playing the playlist.")


# --------------------------- METADATA + STATUS ---------------------------

def current_track():
    try:
        track = sp.current_playback()
        if track and track.get("item"):
            name = track['item']['name']
            artist = track['item']['artists'][0]['name']
            progress = track['progress_ms'] // 1000
            duration = track['item']['duration_ms'] // 1000
            minutes = duration // 60
            seconds = duration % 60
            speak(f"Currently playing {name} by {artist}, duration {minutes} minutes and {seconds} seconds.")
        else:
            speak("Nothing is currently playing.")
    except Exception as e:
        print(f"[Track Info Error] {e}")
        speak("I couldn't fetch the current song.")


# --------------------------- VOLUME ---------------------------

def set_volume(percent: int):
    try:
        sp.volume(percent, device_id=get_active_device_id())
        speak(f"Spotify volume set to {percent} percent.")
    except Exception as e:
        print(f"[Volume Error] {e}")
        speak("I couldn't change the volume.")

