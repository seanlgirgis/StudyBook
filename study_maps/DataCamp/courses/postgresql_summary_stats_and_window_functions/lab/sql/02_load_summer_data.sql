SET search_path TO dc_window_functions, public;

TRUNCATE TABLE summer_medals RESTART IDENTITY;

\copy summer_medals (year, city, sport, discipline, athlete, country, gender, event, medal)
FROM 'D:/Workarea/StudyBook/study_maps/DataCamp/courses/postgresql_summary_stats_and_window_functions/lab/data/summer.csv'
WITH (FORMAT csv, HEADER true, ENCODING 'UTF8');

SELECT COUNT(*) AS loaded_rows FROM summer_medals;
