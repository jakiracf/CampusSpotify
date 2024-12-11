import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import pygame

# --USER DEPENDENT--
SPOTIPY_CLIENT_ID = '******************'
SPOTIPY_CLIENT_SECRET = '*******************'
SPOTIPY_REDIRECT_URI = 'https://campusspotify.onrender.com'
SCOPE = 'user-modify-playback-state user-read-playback-state user-read-currently-playing playlist-read-private'


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI,
                                               scope=SCOPE))

#////////////////////////////////ZALIJEPI LINK NA PLAYLIST//////////////////////////////////////
playlist_id = 'https://open.spotify.com/playlist/63n4nPiyh3yxfgW8rHlKhZ?si=1484cc6d2dbd404a'


#//////////////////////////////FILE SE MORA ZVAT "reklama.mp3"//////////////////////////////////
local_mp3_path = r'reklama.mp3'



def get_playlist_tracks(playlist_id):
    tracks = []
    results = sp.playlist_tracks(playlist_id)
    tracks.extend(results['items'])
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

def shuffle_playlist(tracks):
    import random
    random.shuffle(tracks)
    return tracks

def play_local_mp3(mp3_path):
    pygame.mixer.init()
    pygame.mixer.music.load(mp3_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(1)

def play_spotify_tracks(track_ids):
    sp.start_playback(uris=track_ids)

def wait_for_next_track():
    # Polling until the currently playing track changes
    current_track_id = None
    while True:
        current_playback = sp.current_playback()
        if current_playback and current_playback['is_playing']:
            track_id = current_playback['item']['id']
            if track_id != current_track_id:
                return track_id
        time.sleep(1)

def pause_and_resume_with_local_mp3(current_track_uri, current_position_ms):
    
    sp.pause_playback()

    # Ensure playback is fully paused before continuing
    time.sleep(1)  # Slight delay to ensure Spotify is paused

    # Play local .mp3 file
    play_local_mp3(local_mp3_path)

    # Resume Spotify playback from the saved position
    sp.start_playback(uris=[current_track_uri], position_ms=current_position_ms)

def main():
    tracks = get_playlist_tracks(playlist_id)
    shuffled_tracks = shuffle_playlist(tracks)
    played_tracks = set()
    
    for i in range(0, len(shuffled_tracks), 10):
        
        track_ids = [track['track']['uri'] for track in shuffled_tracks[i:i+10]]
        
        
        play_spotify_tracks(track_ids)
        
        
        while len(played_tracks) < (i + 10):
            current_playback = sp.current_playback()
            if current_playback and current_playback['is_playing']:
                current_track_uri = current_playback['item']['uri']
                current_position_ms = current_playback['progress_ms']
                
                track_id = wait_for_next_track()
                played_tracks.add(track_id)
                print(f"Track {len(played_tracks)}: {track_id} played.")
                
                
                if len(played_tracks) == i + 10:
                    pause_and_resume_with_local_mp3(current_track_uri, current_position_ms)

if __name__ == "__main__":
    main()
