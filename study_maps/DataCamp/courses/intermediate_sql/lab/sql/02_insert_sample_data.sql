-- Intermediate SQL course lab
-- Loads compact sample data for selection, filtering, aggregates,
-- sorting, grouping, NULL handling, and HAVING practice.

SET search_path TO intermediate_sql, public;

INSERT INTO films
    (title, release_year, country, language, certification, duration, genre,
     budget, gross, imdb_score, facebook_likes)
VALUES
    ('Northern Lights', 2018, 'Canada', 'English', 'PG', 112, 'Drama',
     12000000, 28500000, 7.2, 18000),

    ('Desert Run', 2020, 'United States', 'English', 'PG-13', 128, 'Action',
     45000000, 134000000, 6.8, 42000),

    ('Silent River', 2019, 'France', 'French', 'R', 101, 'Drama',
     8000000, 17300000, 7.6, 9500),

    ('City of Glass', 2021, 'United Kingdom', 'English', 'PG-13', 116, 'Mystery',
     22000000, 61000000, 7.1, 27500),

    ('The Last Station', 2017, 'Germany', 'German', 'PG', 109, 'Drama',
     9500000, 14200000, 6.9, 7200),

    ('Ocean Signal', 2022, 'Australia', 'English', 'PG-13', 124, 'Science Fiction',
     38000000, 97000000, 7.4, 36000),

    ('Red Horizon', 2023, 'United States', 'English', 'R', 137, 'Action',
     70000000, 182000000, 7.8, 56000),

    ('Paper Wings', 2016, 'Japan', 'Japanese', 'PG', 98, 'Animation',
     15000000, 54000000, 8.0, 41000),

    ('Blue Orchard', 2018, 'Spain', 'Spanish', NULL, 104, 'Drama',
     6000000, 11800000, 7.0, 8300),

    ('Midnight Market', 2020, 'South Korea', 'Korean', 'R', 119, 'Thriller',
     11000000, 48600000, 7.9, 33500),

    ('Winter Code', 2021, 'Canada', 'English', 'PG-13', 121, 'Thriller',
     26000000, 73500000, 7.3, 28900),

    ('Golden Hour', 2015, 'United States', 'English', 'PG', 95, 'Comedy',
     9000000, 31200000, 6.5, 14400),

    ('Hidden Frequency', 2022, 'Germany', 'German', 'PG-13', 130, 'Science Fiction',
     32000000, 88400000, 7.5, 30100),

    ('Falling Snow', 2019, 'Canada', 'French', 'PG', 107, 'Romance',
     7000000, 19600000, 6.7, 10200),

    ('No Budget Film', 2024, 'United Kingdom', 'English', NULL, 88, 'Documentary',
     NULL, 2400000, 7.1, NULL),

    ('Unknown Score', 2014, 'Brazil', 'Portuguese', 'PG-13', 110, 'Drama',
     5000000, NULL, NULL, 3900);

INSERT INTO people
    (person_name, birth_year, country)
VALUES
    ('Maya Chen', 1985, 'Canada'),
    ('Daniel Brooks', 1978, 'United States'),
    ('Sofia Laurent', 1982, 'France'),
    ('Elias Weber', 1975, 'Germany'),
    ('Hana Mori', 1990, 'Japan'),
    ('Lucas Reed', 1988, 'United Kingdom'),
    ('Ana Torres', 1986, 'Spain'),
    ('Min-jun Park', 1981, 'South Korea');

INSERT INTO roles
    (film_id, person_id, role_type, character_name)
VALUES
    (1, 1, 'Actor', 'Claire'),
    (1, 6, 'Director', NULL),
    (2, 2, 'Actor', 'Cole'),
    (2, 6, 'Director', NULL),
    (3, 3, 'Actor', 'Elise'),
    (3, 3, 'Director', NULL),
    (4, 6, 'Actor', 'Miles'),
    (5, 4, 'Director', NULL),
    (6, 1, 'Actor', 'Dr. Lin'),
    (7, 2, 'Actor', 'Ryder'),
    (8, 5, 'Director', NULL),
    (9, 7, 'Actor', 'Lucia'),
    (10, 8, 'Director', NULL),
    (11, 1, 'Actor', 'Nora'),
    (13, 4, 'Director', NULL);

INSERT INTO reviews
    (film_id, reviewer_name, rating, review_text, review_date)
VALUES
    (1, 'A. Patel', 7.5, 'Strong performances and atmosphere.', '2018-07-12'),
    (1, 'J. Green', 7.0, 'Slow but rewarding.', '2018-07-16'),
    (2, 'R. King', 6.5, 'Energetic action with a familiar plot.', '2020-03-21'),
    (3, 'M. Silva', 8.0, 'Beautifully photographed.', '2019-11-03'),
    (4, 'D. Cole', 7.0, 'A clever mystery.', '2021-05-28'),
    (6, 'T. Adams', 7.5, 'Ambitious science fiction.', '2022-09-14'),
    (7, 'L. Moore', 8.0, 'Excellent pacing.', '2023-06-08'),
    (8, 'K. Ito', 8.5, 'Inventive and moving.', '2016-12-02'),
    (10, 'S. Kim', 8.0, 'Tense from start to finish.', '2020-10-18'),
    (11, 'P. Roy', 7.0, 'A solid thriller.', '2021-02-11'),
    (15, 'N. Hall', 7.0, 'Small production with a clear point of view.', '2024-01-20');

-- Quick validation
SELECT COUNT(*) AS film_rows FROM films;
SELECT COUNT(*) AS people_rows FROM people;
SELECT COUNT(*) AS role_rows FROM roles;
SELECT COUNT(*) AS review_rows FROM reviews;
