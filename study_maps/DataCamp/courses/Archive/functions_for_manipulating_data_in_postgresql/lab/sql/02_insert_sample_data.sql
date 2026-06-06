-- Course 06 PostgreSQL Functions Lab
-- Purpose:
-- Insert small sample data for practicing PostgreSQL data functions.

SET search_path TO course06_functions_lab;

INSERT INTO lab_customers (
    customer_id,
    first_name,
    last_name,
    email,
    create_date,
    favorite_tags
)
VALUES
    (1, 'Sean', 'Girgis', 'sean.girgis@example.com', DATE '2024-01-15',
        ARRAY['sql', 'analytics', 'postgres']),
    (2, 'Anna', 'Rivera', 'anna.rivera@example.com', DATE '2024-02-20',
        ARRAY['python', 'dashboard']),
    (3, 'Brian', 'Piccolo', 'brian.piccolo@example.com', DATE '2024-03-05',
        ARRAY['strategy', 'sql']),
    (4, 'Maya', 'Chen', 'maya.chen@example.com', DATE '2024-04-12',
        ARRAY['reporting', 'postgres']),
    (5, 'Omar', 'Hassan', 'omar.hassan@example.com', DATE '2024-05-01',
        ARRAY['data', 'quality']);

INSERT INTO lab_films (
    film_id,
    title,
    description,
    rating,
    rental_duration,
    special_features
)
VALUES
    (101, 'ELF ADVENTURE',
        'A Astounding story about a helpful elf and a winter journey.',
        'PG', 3, ARRAY['Trailers', 'Deleted Scenes']),
    (102, 'DATA DETECTIVE',
        'A data analyst solves messy customer records with SQL.',
        'PG', 5, ARRAY['Commentaries', 'Behind the Scenes']),
    (103, 'POSTGRES HERO',
        'A database engineer learns timestamp and interval logic.',
        'PG-13', 4, ARRAY['Trailers', 'Commentaries']),
    (104, 'CLEAN TEXT CLUB',
        'A team fixes padded strings, bad case, and strange codes.',
        'G', 2, ARRAY['Deleted Scenes']),
    (105, 'THE FUZZY ELF',
        'An elf, elven helper, and elves appear in a search story.',
        'PG', 6, ARRAY['Trailers', 'Behind the Scenes']),
    (106, 'ARRAY GAMES',
        'A fun look at lists, tags, and special features.',
        'G', 7, ARRAY['Commentaries']);

INSERT INTO lab_rentals (
    rental_id,
    customer_id,
    film_id,
    rental_date,
    return_date
)
VALUES
    (1001, 1, 101, TIMESTAMP '2026-01-02 10:15:00',
        TIMESTAMP '2026-01-05 09:30:00'),
    (1002, 2, 102, TIMESTAMP '2026-01-03 14:00:00',
        TIMESTAMP '2026-01-08 16:45:00'),
    (1003, 3, 103, TIMESTAMP '2026-01-10 08:20:00',
        TIMESTAMP '2026-01-12 11:10:00'),
    (1004, 4, 104, TIMESTAMP '2026-02-01 18:00:00',
        TIMESTAMP '2026-02-03 18:30:00'),
    (1005, 5, 105, TIMESTAMP '2026-02-05 09:00:00',
        NULL),
    (1006, 1, 106, TIMESTAMP '2026-02-10 12:00:00',
        TIMESTAMP '2026-02-18 12:00:00'),
    (1007, 2, 101, TIMESTAMP '2026-03-01 13:25:00',
        TIMESTAMP '2026-03-04 15:40:00'),
    (1008, 3, 105, TIMESTAMP '2026-03-15 20:10:00',
        TIMESTAMP '2026-03-17 21:00:00');

INSERT INTO lab_payments (
    payment_id,
    customer_id,
    rental_id,
    amount,
    payment_date
)
VALUES
    (5001, 1, 1001, 4.99, TIMESTAMP '2026-01-02 10:20:00'),
    (5002, 2, 1002, 6.99, TIMESTAMP '2026-01-03 14:05:00'),
    (5003, 3, 1003, 5.99, TIMESTAMP '2026-01-10 08:25:00'),
    (5004, 4, 1004, 3.99, TIMESTAMP '2026-02-01 18:05:00'),
    (5005, 5, 1005, 7.99, TIMESTAMP '2026-02-05 09:05:00'),
    (5006, 1, 1006, 8.99, TIMESTAMP '2026-02-10 12:10:00'),
    (5007, 2, 1007, 4.99, TIMESTAMP '2026-03-01 13:30:00'),
    (5008, 3, 1008, 7.99, TIMESTAMP '2026-03-15 20:15:00');

INSERT INTO lab_dirty_text (
    dirty_id,
    raw_text,
    raw_code,
    comparison_text
)
VALUES
    (1, '  padded text  ', '7', 'GAMBOL'),
    (2, 'mixed CASE value', '42', 'GUMBO'),
    (3, 'A Astounding example', '305', 'ELF'),
    (4, '  left padded only', '9', 'ELVES'),
    (5, 'right padded only  ', '1234', 'POSTGRES');
