SET search_path TO joining_data_lab;

CREATE TABLE countries (
    code        text PRIMARY KEY,
    name        text NOT NULL,
    region      text NOT NULL,
    population  bigint
);

CREATE TABLE cities (
    city_id       integer PRIMARY KEY,
    name          text NOT NULL,
    country_code  text REFERENCES countries(code),
    population    bigint
);

CREATE TABLE populations (
    country_code  text NOT NULL,
    year          integer NOT NULL,
    size          bigint NOT NULL,
    PRIMARY KEY (country_code, year)
);

CREATE TABLE economies (
    country_code       text,
    year               integer NOT NULL,
    gdp_percapita      numeric(12,2),
    unemployment_rate  numeric(5,2)
);

CREATE TABLE languages (
    country_code  text,
    language      text NOT NULL,
    official      boolean NOT NULL DEFAULT false
);
