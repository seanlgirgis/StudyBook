-- Intermediate SQL course lab
-- Creates the core tables used across Chapters 1-4.

SET search_path TO intermediate_sql, public;

CREATE TABLE films (
    film_id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title           VARCHAR(150) NOT NULL,
    release_year    INTEGER,
    country         VARCHAR(80),
    language        VARCHAR(50),
    certification   VARCHAR(20),
    duration        INTEGER,
    genre           VARCHAR(60),
    budget          NUMERIC(14,2),
    gross           NUMERIC(14,2),
    imdb_score      NUMERIC(3,1),
    facebook_likes  INTEGER
);

CREATE TABLE people (
    person_id       INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    person_name     VARCHAR(120) NOT NULL,
    birth_year      INTEGER,
    country         VARCHAR(80)
);

CREATE TABLE roles (
    role_id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    film_id         INTEGER NOT NULL REFERENCES films(film_id),
    person_id       INTEGER NOT NULL REFERENCES people(person_id),
    role_type       VARCHAR(30) NOT NULL,
    character_name  VARCHAR(120)
);

CREATE TABLE reviews (
    review_id       INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    film_id         INTEGER NOT NULL REFERENCES films(film_id),
    reviewer_name   VARCHAR(120),
    rating          NUMERIC(3,1),
    review_text     TEXT,
    review_date     DATE
);

CREATE INDEX idx_films_release_year ON films(release_year);
CREATE INDEX idx_films_country ON films(country);
CREATE INDEX idx_films_genre ON films(genre);
CREATE INDEX idx_roles_film_id ON roles(film_id);
CREATE INDEX idx_reviews_film_id ON reviews(film_id);
