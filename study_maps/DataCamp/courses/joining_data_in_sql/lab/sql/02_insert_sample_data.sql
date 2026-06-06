SET search_path TO joining_data_lab;

INSERT INTO countries (code, name, region, population) VALUES
('USA', 'United States', 'North America', 331000000),
('CAN', 'Canada', 'North America', 38000000),
('MEX', 'Mexico', 'North America', 128000000),
('BRA', 'Brazil', 'South America', 213000000),
('FRA', 'France', 'Europe', 67000000),
('SGP', 'Singapore', 'Asia', 5700000),
('ESP', 'Spain', 'Europe', 47000000);

INSERT INTO cities (city_id, name, country_code, population) VALUES
(1, 'New York', 'USA', 8400000),
(2, 'Washington', 'USA', 700000),
(3, 'Toronto', 'CAN', 2900000),
(4, 'Mexico', 'MEX', 9200000),
(5, 'Brasilia', 'BRA', 3000000),
(6, 'Paris', 'FRA', 2100000),
(7, 'Singapore', 'SGP', 5700000),
(8, 'Canada', NULL, 12000);

INSERT INTO populations (country_code, year, size) VALUES
('USA', 2010, 309000000),
('USA', 2015, 321000000),
('CAN', 2010, 34000000),
('CAN', 2015, 36000000),
('MEX', 2010, 114000000),
('MEX', 2015, 121000000),
('BRA', 2010, 195000000),
('BRA', 2015, 204000000),
('FRA', 2010, 65000000),
('FRA', 2015, 66500000),
('SGP', 2010, 5100000),
('SGP', 2015, 5500000);

INSERT INTO economies (country_code, year, gdp_percapita, unemployment_rate) VALUES
('USA', 2010, 48467.00, 9.60),
('USA', 2015, 56803.00, 5.30),
('CAN', 2010, 47450.00, 8.10),
('CAN', 2015, 43596.00, 6.90),
('MEX', 2010, 9271.00, 5.30),
('BRA', 2015, 8814.00, 8.50),
('FRA', 2010, 40638.00, 9.30),
('FRA', 2015, 36653.00, 10.40),
('ARG', 2015, 13790.00, 7.20),
(NULL, 2015, 9999.00, 4.40);

INSERT INTO languages (country_code, language, official) VALUES
('USA', 'English', false),
('USA', 'Spanish', false),
('CAN', 'English', true),
('CAN', 'French', true),
('MEX', 'Spanish', true),
('BRA', 'Portuguese', true),
('FRA', 'French', true),
('SGP', 'English', true),
('SGP', 'Malay', true),
('SGP', 'Mandarin', true),
(NULL, 'Unknown', false);
