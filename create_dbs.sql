CREATE TABLE IF NOT EXISTS movies(
  movieId INT PRIMARY KEY,
  title VARCHAR(512) NOT NULL,
  genres VARCHAR(1024)
);

CREATE TABLE IF NOT EXISTS links(
  movieId INT PRIMARY KEY,
  imdbId VARCHAR(512) NOT NULL,
  tmdbId VARCHAR(1024)
);

CREATE TABLE IF NOT EXISTS ratings(
  userId VARCHAR(512),
  movieId INT,
  rating VARCHAR(512) NOT NULL,
  timestamp VARCHAR(1024)
);

CREATE TABLE IF NOT EXISTS tags(
  userId VARCHAR(512),
  movieId INT,
  tag VARCHAR(512) NOT NULL,
  timestamp VARCHAR(1024)
);
