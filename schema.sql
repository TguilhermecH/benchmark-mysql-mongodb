CREATE DATABASE IF NOT EXISTS imdb;
USE imdb;

CREATE TABLE title_basics (
    tconst VARCHAR(20) PRIMARY KEY,
    titleType VARCHAR(20),
    primaryTitle VARCHAR(255),
    originalTitle VARCHAR(255),
    isAdult TINYINT(1),
    startYear INT,
    endYear INT,
    runtimeMinutes INT,
    genres VARCHAR(255)
);
