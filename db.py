import time
import spotipy
import pylast
import mysql.connector
from spotipy.oauth2 import SpotifyOAuth
from pylast import LastFMNetwork, md5

# (Include all the previous functions here: authenticate_spotify_user, authenticate_lastfm,
# fetch_spotify_tracks, fetch_lastfm_tracks, and all insert_*_to_db functions)

def main():
    # Spotify credentials and redirect URI
    spotify_client_id = 'YourSpotifyClientID'  # Replace with your actual Spotify Client ID
    spotify_client_secret = 'YourSpotifyClientSecret'  # Replace with your actual Spotify Client Secret
    spotify_redirect_uri = 'http://localhost:8888/callback'  # Replace with your actual redirect URI

    sp = authenticate_spotify_user(spotify_client_id, spotify_client_secret, spotify_redirect_uri)

    # Last.fm credentials
    lastfm_api_key = 'YourApiKey'  # Replace with your actual Last.fm API Key
    lastfm_api_secret = 'YourApiSecret'
    lastfm_username = 'YourUsername'
    lastfm_password = 'YourPassword'  # Plain text password

    network = authenticate_lastfm(lastfm_api_key, lastfm_api_secret, lastfm_username, lastfm_password)

    # Fetch data
    print("Fetching Spotify tracks...")
    spotify_tracks = fetch_spotify_tracks(sp)

    print(f"Fetched {len(spotify_tracks)} Spotify tracks")

    print("Fetching Last.fm tracks...")
    lastfm_tracks = fetch_lastfm_tracks(network, lastfm_username)

    print(f"Fetched {len(lastfm_tracks)} Last.fm tracks")

    # Example: Extract unique artists from spotify_tracks (basic)
    artists = []
    seen_artist_ids = set()
    for track in spotify_tracks:
        if track['artist_id'] and track['artist_id'] not in seen_artist_ids:
            artists.append({
                'artist_id': track['artist_id'],
                'name': 'Unknown Artist Name',  # You can extend to fetch artist info if needed
                'genre': None,
                'popularity_score': None
            })
            seen_artist_ids.add(track['artist_id'])
    # Database configuration
    db_config = {
        'user': 'root',
        'password': 'password',
        'host': 'localhost',
        'database': 'database_name'
    }

    print("Inserting artists into DB...")
    insert_artists_to_db(artists, db_config)

    print("Inserting songs into DB...")
    insert_songs_to_db(spotify_tracks, db_config)

    print("Inserting listening history into DB...")
    insert_listening_history_to_db(listening_history, db_config)

    print("Inserting song instruments into DB...")
    insert_song_instruments_to_db(song_instruments, db_config)

    print("Inserting instrument popularity into DB...")
    insert_instrument_popularity_to_db(instrument_popularity, db_config)

    print("Inserting user genre preferences into DB...")
    insert_user_genre_preferences_to_db(user_genre_preferences, db_config)

    print("Inserting user surveys into DB...")
    insert_user_surveys_to_db(user_surveys, db_config)

    print("Inserting users into DB...")
    insert_users_to_db(users, db_config)

    print("Done!")

if __name__ == '__main__':
    main()
