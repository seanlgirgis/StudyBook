-- 01_create_summer_medals_table.sql
-- Reconstructed local table for Summer Medals practice.

DROP TABLE IF EXISTS summer_medals;

CREATE TABLE summer_medals (
    medal_id INTEGER PRIMARY KEY,
    year INTEGER CHECK (year BETWEEN 1896 AND 2030),
    city TEXT,
    sport TEXT,
    discipline TEXT,
    athlete TEXT,
    country TEXT,
    gender TEXT CHECK (gender IN ('Men', 'Women')),
    event TEXT,
    medal TEXT CHECK (medal IN ('Gold', 'Silver', 'Bronze'))
);