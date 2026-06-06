SET search_path TO data_manipulation_lab;

INSERT INTO country (id, name) VALUES
(1, 'England'),
(2, 'Spain'),
(3, 'Germany');

INSERT INTO league (id, country_id, name) VALUES
(10, 1, 'England Premier League'),
(20, 2, 'Spain LIGA BBVA'),
(30, 3, 'Germany 1. Bundesliga');

INSERT INTO team (team_api_id, team_long_name, team_short_name) VALUES
(10260, 'Manchester United', 'MUN'),
(8455, 'Chelsea', 'CHE'),
(8650, 'Liverpool', 'LIV'),
(8634, 'FC Barcelona', 'BAR'),
(8633, 'Real Madrid CF', 'RMA'),
(9823, 'FC Bayern Munich', 'BAY'),
(10189, 'FC Schalke 04', 'S04');

INSERT INTO match VALUES
(1, 1, 10, '2014/2015', 1, '2014-08-16', 10260, 8455, 2, 1),
(2, 1, 10, '2014/2015', 2, '2014-08-24', 8650, 10260, 3, 0),
(3, 1, 10, '2014/2015', 3, '2014-08-30', 10260, 8650, 1, 1),
(4, 1, 10, '2014/2015', 4, '2014-09-14', 8455, 10260, 2, 4),
(5, 1, 10, '2014/2015', 5, '2014-09-21', 10260, 8455, 0, 3),
(6, 2, 20, '2014/2015', 1, '2014-08-23', 8634, 8633, 3, 1),
(7, 2, 20, '2014/2015', 2, '2014-10-25', 8633, 8634, 1, 1),
(8, 2, 20, '2013/2014', 1, '2013-09-10', 8634, 8633, 5, 4),
(9, 3, 30, '2014/2015', 1, '2014-08-22', 9823, 10189, 4, 0),
(10, 3, 30, '2014/2015', 2, '2014-09-01', 10189, 9823, 2, 6),
(11, 3, 30, '2013/2014', 1, '2013-08-10', 9823, 10189, 8, 1),
(12, 1, 10, '2013/2014', 1, '2013-08-17', 10260, 8650, 4, 4);
