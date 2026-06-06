\set ON_ERROR_STOP on
SET search_path TO dc_window_lab, public;

CREATE TABLE summer_medals (
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
    CONSTRAINT ck_summer_medals_medal
        CHECK (medal IN ('Gold', 'Silver', 'Bronze'))
);

CREATE INDEX ix_summer_medals_year
    ON summer_medals (year);

CREATE INDEX ix_summer_medals_country_year
    ON summer_medals (country, year);

CREATE INDEX ix_summer_medals_event_gender_year
    ON summer_medals (event, gender, year);

CREATE INDEX ix_summer_medals_athlete
    ON summer_medals (athlete);
