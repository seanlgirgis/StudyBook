SET search_path TO dc_window_functions, public;

CREATE TABLE IF NOT EXISTS summer_medals (
    medal_id    bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    year        integer NOT NULL,
    city        text NOT NULL,
    sport       text NOT NULL,
    discipline  text NOT NULL,
    athlete     text NOT NULL,
    country     text,
    gender      text NOT NULL,
    event       text NOT NULL,
    medal       text NOT NULL,
    CONSTRAINT summer_medals_medal_check
        CHECK (medal IN ('Gold', 'Silver', 'Bronze'))
);

CREATE INDEX IF NOT EXISTS ix_summer_medals_year
    ON summer_medals (year);
CREATE INDEX IF NOT EXISTS ix_summer_medals_country_year
    ON summer_medals (country, year);
CREATE INDEX IF NOT EXISTS ix_summer_medals_athlete
    ON summer_medals (athlete);
