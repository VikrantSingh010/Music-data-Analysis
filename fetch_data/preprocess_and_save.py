import pandas as pd
import os
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:password@localhost/music")

RAW_DIR = "data/raw"
PROC_DIR = "data/processed"
os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROC_DIR, exist_ok=True)

tables = [
    "users", "user_surveys", "user_genre_preferences", "songs",
    "artists", "song_instruments", "instrument_popularity", "listening_history"
]
def clean_users(df):
    df = df.dropna(subset=["user_id", "username"])
    df['age'] = df['age'].fillna(df['age'].median())
    df['gender'] = df['gender'].fillna("unknown")
    df['country'] = df['country'].fillna("unknown")
    return df

def clean_user_surveys(df):
    df = df.dropna(subset=["survey_id", "user_id"])
    df['favorite_genre'] = df['favorite_genre'].fillna("unknown")
    df['preferred_instrument'] = df['preferred_instrument'].fillna("unknown")
    df['listening_frequency'] = df['listening_frequency'].fillna("unknown")
    return df

def clean_user_genre_preferences(df):
    df['age'] = df['age'].fillna(df['age'].median())
    df['gender'] = df['gender'].fillna("unknown")
    df['genre'] = df['genre'].fillna("unknown")
    df['avg_listen_duration'] = df['avg_listen_duration'].fillna(0)
    df['completion_rate'] = df['completion_rate'].fillna(0)
    return df

def clean_songs(df):
    df['title'] = df['title'].fillna("unknown")
    df['genre'] = df['genre'].fillna("unknown")
    df['tempo'] = df['tempo'].fillna(df['tempo'].median())
    df['energy'] = df['energy'].fillna(df['energy'].median())
    df['danceability'] = df['danceability'].fillna(df['danceability'].median())
    df['instrumentalness'] = df['instrumentalness'].fillna(df['instrumentalness'].median())
    return df

def clean_artists(df):
    df['name'] = df['name'].fillna("unknown")
    df['genre'] = df['genre'].fillna("unknown")
    df['popularity_score'] = df['popularity_score'].fillna(0)
    return df

def clean_song_instruments(df):
    df['confidence_score'] = df['confidence_score'].fillna(0)
    return df

def clean_instrument_popularity(df):
    df['avg_confidence'] = df['avg_confidence'].fillna(0)
    return df

def clean_listening_history(df):
    df['listen_duration_ms'] = df['listen_duration_ms'].fillna(0)
    df['completed'] = df['completed'].fillna(0)
    return df

clean_funcs = {
    "users": clean_users,
    "user_surveys": clean_user_surveys,
    "user_genre_preferences": clean_user_genre_preferences,
    "songs": clean_songs,
    "artists": clean_artists,
    "song_instruments": clean_song_instruments,
    "instrument_popularity": clean_instrument_popularity,
    "listening_history": clean_listening_history
}

def save_raw_tables():
    for table in tables:
        df = pd.read_sql(f"SELECT * FROM {table}", engine)
        df.to_csv(f"{RAW_DIR}/{table}.csv", index=False)
        print(f"[RAW SAVED] {table}")

def preprocess_all():
    for table in tables:
        df = pd.read_csv(f"{RAW_DIR}/{table}.csv")
        cleaned_df = clean_funcs[table](df)
        cleaned_df.to_csv(f"{PROC_DIR}/{table}_cleaned.csv", index=False)
        print(f"[CLEANED SAVED] {table}")

def main():
    save_raw_tables()
    preprocess_all()

if __name__ == "__main__":
    main()
