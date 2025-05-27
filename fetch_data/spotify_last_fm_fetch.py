import time
import spotipy
import pylast
import mysql.connector
from spotipy.oauth2 import SpotifyOAuth
from pylast import LastFMNetwork, md5

# Spotify Authentication using OAuth (user authorization)
from spotipy.oauth2 import SpotifyOAuth

def authenticate_spotify_user(client_id, client_secret, redirect_uri):
    scope = "user-library-read"
    sp_oauth = SpotifyOAuth(client_id=client_id,
                            client_secret=client_secret,
                            redirect_uri=redirect_uri,
                            scope=scope,
                            cache_path=".cache")
    token_info = sp_oauth.get_access_token(as_dict=False)
    sp = spotipy.Spotify(auth=token_info)
    return sp

# Last.fm Authentication
def authenticate_lastfm(api_key, api_secret, username, password):
    password_hash = md5(password)  # pylast md5 hashing of password
    network = LastFMNetwork(api_key=api_key, api_secret=api_secret,
                           username=username, password_hash=password_hash)
    return network

# Fetch Spotify saved tracks with audio features
def fetch_spotify_tracks(sp, limit=10000):
    tracks = []
    offset = 0

    while len(tracks) < limit:
        results = sp.current_user_saved_tracks(limit=50, offset=offset)
        if not results['items']:
            break

        for item in results['items']:
            track = item['track']
            track_info = {
                'name': track['name'],
                'spotify_id': track['id'],
                'artist_id': track['artists'][0]['id'] if track['artists'] else None,
                'duration_ms': track['duration_ms'],
                'release_date': track['album']['release_date'],
                'danceability': None,
                'energy': None,
                'tempo': None,
                'valence': None,
            }
            tracks.append(track_info)

        if len(results['items']) < 50:
            break
        offset += 50

    # Fetch audio features in batches
    for i in range(0, len(tracks), 100):
        batch = tracks[i:i+100]
        ids = [t['spotify_id'] for t in batch if t['spotify_id']]
        audio_features = sp.audio_features(ids)
        for j, af in enumerate(audio_features):
            if af:
                batch[j]['danceability'] = af['danceability']
                batch[j]['energy'] = af['energy']
                batch[j]['tempo'] = af['tempo']
                batch[j]['valence'] = af['valence']

    return tracks[:limit]

def fetch_lastfm_tracks(network, username, limit=10000):
    tracks = []
    user = network.get_user(username)

    recent_tracks = user.get_recent_tracks(limit=None)  # get all available, streamed
    count = 0

    for track in recent_tracks:
        tracks.append({
            'name': track.get_name(),
            'artist': track.get_artist().get_name(),
            'album': track.get_album().get_name(),
            'played_at': track.get_date().strftime('%Y-%m-%d %H:%M:%S')
        })
        count += 1
        if count >= limit:
            break
        time.sleep(0.2)  # slow down to avoid rate limits

    return tracks

# Insert Spotify artists into MySQL
def insert_artists_to_db(artists, db_config):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    for artist in artists:
        cursor.execute("""
            INSERT INTO artists (artist_id, name, genre, popularity_score)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE name=VALUES(name), genre=VALUES(genre), popularity_score=VALUES(popularity_score)
        """, (artist['artist_id'], artist['name'], artist.get('genre'), artist.get('popularity_score')))
    conn.commit()
    cursor.close()
    conn.close()

# Insert Spotify songs into MySQL
def insert_songs_to_db(songs, db_config):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    for song in songs:
        cursor.execute("""
            INSERT INTO songs (song_id, title, artist_id, duration_ms, release_date, genre, tempo, energy, danceability, instrumentalness)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE title=VALUES(title), artist_id=VALUES(artist_id), duration_ms=VALUES(duration_ms),
                                    release_date=VALUES(release_date), genre=VALUES(genre), tempo=VALUES(tempo),
                                    energy=VALUES(energy), danceability=VALUES(danceability), instrumentalness=VALUES(instrumentalness)
        """, (
            song['song_id'], song['name'], song['artist_id'], song['duration_ms'], song['release_date'], song.get('genre'),
            song.get('tempo'), song.get('energy'), song.get('danceability'), song.get('instrumentalness', None)
        ))
    conn.commit()
    cursor.close()
    conn.close()

# Insert listening history into MySQL
def insert_listening_history_to_db(history, db_config):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    for entry in history:
        cursor.execute("""
            INSERT INTO listening_history (user_id, song_id, listen_timestamp, listen_duration_ms, completed)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            entry['user_id'], entry['song_id'], entry.get('listen_timestamp'), entry.get('listen_duration_ms'), entry.get('completed')
        ))
    conn.commit()
    cursor.close()
    conn.close()

# Insert song instruments into MySQL
def insert_song_instruments_to_db(song_instruments, db_config):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    for si in song_instruments:
        cursor.execute("""
            INSERT INTO song_instruments (song_id, instrument, confidence_score)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE confidence_score=VALUES(confidence_score)
        """, (si['song_id'], si['instrument'], si.get('confidence_score')))
    conn.commit()
    cursor.close()
    conn.close()

# Insert instrument popularity into MySQL
def insert_instrument_popularity_to_db(instruments, db_config):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    for inst in instruments:
        cursor.execute("""
            INSERT INTO instrument_popularity (instrument, unique_listeners, total_plays, avg_confidence)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE unique_listeners=VALUES(unique_listeners), total_plays=VALUES(total_plays), avg_confidence=VALUES(avg_confidence)
        """, (inst['instrument'], inst['unique_listeners'], inst['total_plays'], inst.get('avg_confidence')))
    conn.commit()
    cursor.close()
    conn.close()

# Insert user genre preferences into MySQL
def insert_user_genre_preferences_to_db(preferences, db_config):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    for pref in preferences:
        cursor.execute("""
            INSERT INTO user_genre_preferences (user_id, age, gender, genre, listen_count, avg_listen_duration, completion_rate)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE age=VALUES(age), gender=VALUES(gender), genre=VALUES(genre),
                                    listen_count=VALUES(listen_count), avg_listen_duration=VALUES(avg_listen_duration),
                                    completion_rate=VALUES(completion_rate)
        """, (pref['user_id'], pref.get('age'), pref.get('gender'), pref.get('genre'), pref['listen_count'], pref.get('avg_listen_duration'), pref.get('completion_rate')))
    conn.commit()
    cursor.close()
    conn.close()

# Insert user surveys into MySQL
def insert_user_surveys_to_db(surveys, db_config):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    for survey in surveys:
        cursor.execute("""
            INSERT INTO user_surveys (user_id, favorite_genre, preferred_instrument, listening_frequency, survey_date)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE favorite_genre=VALUES(favorite_genre), preferred_instrument=VALUES(preferred_instrument),
                                    listening_frequency=VALUES(listening_frequency), survey_date=VALUES(survey_date)
        """, (
            survey['user_id'], survey.get('favorite_genre'), survey.get('preferred_instrument'), survey.get('listening_frequency'), survey.get('survey_date')
        ))
    conn.commit()
    cursor.close()
    conn.close()

# Insert users into MySQL
def insert_users_to_db(users, db_config):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    for user in users:
        cursor.execute("""
            INSERT INTO users (user_id, username, age, gender, country, registration_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE username=VALUES(username), age=VALUES(age), gender=VALUES(gender),
                                    country=VALUES(country), registration_date=VALUES(registration_date)
        """, (
            user['user_id'], user['username'], user.get('age'), user.get('gender'), user.get('country'), user.get('registration_date')
        ))
    conn.commit()
    cursor.close()
    conn.close()

# You can call these insert functions from your main() as needed with the respective data lists.
