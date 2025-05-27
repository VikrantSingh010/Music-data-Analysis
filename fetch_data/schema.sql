CREATE TABLE artists (
  artist_id INT(11) NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  genre VARCHAR(50),
  popularity_score DECIMAL(3,2),
  PRIMARY KEY (artist_id)
);

CREATE TABLE instrument_popularity (
  instrument VARCHAR(50) NOT NULL,
  unique_listeners BIGINT(21) NOT NULL DEFAULT 0,
  total_plays BIGINT(21) NOT NULL DEFAULT 0,
  avg_confidence DOUBLE,
  PRIMARY KEY (instrument)
);

CREATE TABLE listening_history (
  history_id INT(11) NOT NULL AUTO_INCREMENT,
  user_id INT(11),
  song_id INT(11),
  listen_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  listen_duration_ms INT(11),
  completed TINYINT(1),
  PRIMARY KEY (history_id),
  KEY user_id_idx (user_id),
  KEY song_id_idx (song_id)
);

CREATE TABLE song_instruments (
  song_id INT(11) NOT NULL,
  instrument VARCHAR(50) NOT NULL,
  confidence_score FLOAT,
  PRIMARY KEY (song_id, instrument)
);

CREATE TABLE songs (
  song_id INT(11) NOT NULL AUTO_INCREMENT,
  title VARCHAR(200) NOT NULL,
  artist_id INT(11),
  duration_ms INT(11),
  release_date DATE,
  genre VARCHAR(50),
  tempo FLOAT,
  energy FLOAT,
  danceability FLOAT,
  instrumentalness FLOAT,
  PRIMARY KEY (song_id),
  KEY artist_id_idx (artist_id),
  KEY genre_idx (genre)
);

CREATE TABLE user_genre_preferences (
  user_id INT(11) NOT NULL DEFAULT 0,
  age INT(11),
  gender VARCHAR(20),
  genre VARCHAR(50),
  listen_count BIGINT(21) NOT NULL DEFAULT 0,
  avg_listen_duration DECIMAL(14,4),
  completion_rate DECIMAL(27,4)
);

CREATE TABLE user_surveys (
  survey_id INT(11) NOT NULL AUTO_INCREMENT,
  user_id INT(11),
  favorite_genre VARCHAR(50),
  preferred_instrument VARCHAR(50),
  listening_frequency VARCHAR(20),
  survey_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (survey_id),
  KEY user_id_idx (user_id)
);

CREATE TABLE users (
  user_id INT(11) NOT NULL AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL UNIQUE,
  age INT(11),
  gender VARCHAR(20),
  country VARCHAR(50),
  registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id)
);
