\set ON_ERROR_STOP on
SET search_path TO dc_window_lab, public;

TRUNCATE TABLE summer_medals RESTART IDENTITY;

\copy summer_medals (year, city, sport, discipline, athlete, country, gender, event, medal)
FROM './data/summer.csv'
WITH (
    FORMAT csv,
    HEADER true,
    ENCODING 'UTF8'
);

SELECT COUNT(*) AS loaded_rows
FROM summer_medals;
