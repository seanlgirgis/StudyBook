SET search_path TO data_manipulation_lab;

CREATE TABLE country (
    id integer PRIMARY KEY,
    name text NOT NULL
);

CREATE TABLE league (
    id integer PRIMARY KEY,
    country_id integer NOT NULL REFERENCES country(id),
    name text NOT NULL
);

CREATE TABLE team (
    team_api_id integer PRIMARY KEY,
    team_long_name text NOT NULL,
    team_short_name text NOT NULL
);

CREATE TABLE match (
    id integer PRIMARY KEY,
    country_id integer NOT NULL REFERENCES country(id),
    league_id integer NOT NULL REFERENCES league(id),
    season text NOT NULL,
    stage integer NOT NULL,
    date date NOT NULL,
    hometeam_id integer NOT NULL REFERENCES team(team_api_id),
    awayteam_id integer NOT NULL REFERENCES team(team_api_id),
    home_goal integer NOT NULL,
    away_goal integer NOT NULL
);
