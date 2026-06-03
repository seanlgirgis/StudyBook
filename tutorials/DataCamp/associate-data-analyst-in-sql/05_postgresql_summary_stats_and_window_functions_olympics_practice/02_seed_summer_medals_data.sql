-- 02_seed_summer_medals_data.sql
-- Reconstructed local practice data for summer_medals.
-- Inserts 120 rows (40 years x 3 medals) for one event,
-- plus additional rows for Discus Throw and other events.

INSERT INTO public.summer_medals (
    medal_id,
    year,
    city,
    sport,
    discipline,
    athlete,
    country,
    gender,
    event,
    medal
)
SELECT
    (y.year * 10) + m.medal_rank AS medal_id,
    y.year,
    y.city,
    'Weightlifting' AS sport,
    'Weightlifting' AS discipline,
    CASE m.medal
        WHEN 'Gold' THEN y.gold_athlete
        WHEN 'Silver' THEN y.silver_athlete
        ELSE y.bronze_athlete
    END AS athlete,
    CASE m.medal
        WHEN 'Gold' THEN y.gold_country
        WHEN 'Silver' THEN y.silver_country
        ELSE y.bronze_country
    END AS country,
    'Men' AS gender,
    '69KG' AS event,
    m.medal
FROM (
    VALUES
    (1980,'Moscow','Bulgaria','Ivan Petrov','Soviet Union','Sergei Ivanov','Poland','Jan Kowalski'),
    (1981,'Sofia','Bulgaria','Ivan Petrov','Soviet Union','Sergei Ivanov','Poland','Jan Kowalski'),
    (1982,'Budapest','Turkey','Kemal Yilmaz','Bulgaria','Ivan Petrov','Romania','Mihai Popescu'),
    (1983,'Prague','Turkey','Kemal Yilmaz','Soviet Union','Viktor Sokolov','Bulgaria','Georgi Stoyanov'),
    (1984,'Los Angeles','Turkey','Kemal Yilmaz','Bulgaria','Ivan Petrov','Romania','Mihai Popescu'),
    (1985,'Seoul','Bulgaria','Georgi Stoyanov','Soviet Union','Viktor Sokolov','Turkey','Ali Demir'),
    (1986,'Madrid','China','Li Wei','Bulgaria','Georgi Stoyanov','Soviet Union','Viktor Sokolov'),
    (1987,'Rome','China','Li Wei','Turkey','Ali Demir','Bulgaria','Georgi Stoyanov'),
    (1988,'Seoul','China','Li Wei','Soviet Union','Viktor Sokolov','Turkey','Ali Demir'),
    (1989,'Athens','Bulgaria','Nikolai Ivanov','China','Li Wei','Romania','Mihai Popescu'),
    (1990,'Beijing','Bulgaria','Nikolai Ivanov','Turkey','Ali Demir','China','Li Wei'),
    (1991,'Berlin','Turkey','Ali Demir','Bulgaria','Nikolai Ivanov','China','Li Wei'),
    (1992,'Barcelona','Turkey','Ali Demir','China','Li Wei','Bulgaria','Nikolai Ivanov'),
    (1993,'Lisbon','Greece','Dimitrios Pappas','Turkey','Ali Demir','Bulgaria','Nikolai Ivanov'),
    (1994,'Paris','Greece','Dimitrios Pappas','China','Li Wei','Turkey','Ali Demir'),
    (1995,'Sydney','China','Wang Jun','Greece','Dimitrios Pappas','Turkey','Ali Demir'),
    (1996,'Atlanta','China','Wang Jun','Turkey','Ali Demir','Greece','Dimitrios Pappas'),
    (1997,'Toronto','Greece','Dimitrios Pappas','China','Wang Jun','Bulgaria','Petar Kolev'),
    (1998,'Bangkok','Iran','Reza Hosseini','Greece','Dimitrios Pappas','China','Wang Jun'),
    (1999,'Istanbul','Iran','Reza Hosseini','Turkey','Ali Demir','Greece','Dimitrios Pappas'),
    (2000,'Sydney','Iran','Reza Hosseini','China','Wang Jun','Turkey','Ali Demir'),
    (2001,'Milan','China','Zhao Ming','Iran','Reza Hosseini','Bulgaria','Petar Kolev'),
    (2002,'Oslo','China','Zhao Ming','Turkey','Ali Demir','Iran','Reza Hosseini'),
    (2003,'Athens','Greece','Nikos Pappas','China','Zhao Ming','Iran','Reza Hosseini'),
    (2004,'Athens','Greece','Nikos Pappas','Iran','Reza Hosseini','China','Zhao Ming'),
    (2005,'Helsinki','Iran','Majid Karimi','Greece','Nikos Pappas','Turkey','Ali Demir'),
    (2006,'Doha','Iran','Majid Karimi','China','Zhao Ming','Greece','Nikos Pappas'),
    (2007,'Lima','China','Zhao Ming','Iran','Majid Karimi','Greece','Nikos Pappas'),
    (2008,'Beijing','China','Zhao Ming','Greece','Nikos Pappas','Iran','Majid Karimi'),
    (2009,'Moscow','Kazakhstan','Arman Sadykov','China','Zhao Ming','Iran','Majid Karimi'),
    (2010,'Delhi','Kazakhstan','Arman Sadykov','Iran','Majid Karimi','China','Zhao Ming'),
    (2011,'Tokyo','Iran','Majid Karimi','Kazakhstan','Arman Sadykov','Turkey','Murat Aydin'),
    (2012,'London','Iran','Majid Karimi','China','Zhao Ming','Kazakhstan','Arman Sadykov'),
    (2013,'Warsaw','Turkey','Murat Aydin','Iran','Majid Karimi','China','Zhao Ming'),
    (2014,'Incheon','Turkey','Murat Aydin','Kazakhstan','Arman Sadykov','Iran','Majid Karimi'),
    (2015,'Rio','China','Liu Chen','Turkey','Murat Aydin','Iran','Majid Karimi'),
    (2016,'Rio','China','Liu Chen','Iran','Majid Karimi','Turkey','Murat Aydin'),
    (2017,'Taipei','Iran','Majid Karimi','China','Liu Chen','Kazakhstan','Arman Sadykov'),
    (2018,'Jakarta','Iran','Majid Karimi','Turkey','Murat Aydin','China','Liu Chen'),
    (2019,'Lima','Turkey','Murat Aydin','Iran','Majid Karimi','China','Liu Chen')
) AS y(year, city, gold_country, gold_athlete, silver_country, silver_athlete, bronze_country, bronze_athlete)
CROSS JOIN (
    VALUES
    (1,'Gold'),
    (2,'Silver'),
    (3,'Bronze')
) AS m(medal_rank, medal);

INSERT INTO public.summer_medals (
    medal_id,
    year,
    city,
    sport,
    discipline,
    athlete,
    country,
    gender,
    event,
    medal
)
VALUES
(30001, 2008, 'Beijing', 'Athletics', 'Athletics', 'Lars Holm', 'Sweden', 'Men', 'Discus Throw', 'Gold'),
(30002, 2008, 'Beijing', 'Athletics', 'Athletics', 'Markus Stein', 'Germany', 'Men', 'Discus Throw', 'Silver'),
(30003, 2008, 'Beijing', 'Athletics', 'Athletics', 'Ivan Drago', 'Russia', 'Men', 'Discus Throw', 'Bronze'),
(30004, 2009, 'Berlin', 'Athletics', 'Athletics', 'Lars Holm', 'Sweden', 'Men', 'Discus Throw', 'Gold'),
(30005, 2009, 'Berlin', 'Athletics', 'Athletics', 'Kenji Sato', 'Japan', 'Men', 'Discus Throw', 'Silver'),
(30006, 2009, 'Berlin', 'Athletics', 'Athletics', 'Tom Reed', 'USA', 'Men', 'Discus Throw', 'Bronze'),
(30007, 2010, 'Rome', 'Athletics', 'Athletics', 'Kenji Sato', 'Japan', 'Men', 'Discus Throw', 'Gold'),
(30008, 2010, 'Rome', 'Athletics', 'Athletics', 'Lars Holm', 'Sweden', 'Men', 'Discus Throw', 'Silver'),
(30009, 2010, 'Rome', 'Athletics', 'Athletics', 'Markus Stein', 'Germany', 'Men', 'Discus Throw', 'Bronze'),
(30010, 2011, 'Paris', 'Athletics', 'Athletics', 'Kenji Sato', 'Japan', 'Men', 'Discus Throw', 'Gold'),
(30011, 2011, 'Paris', 'Athletics', 'Athletics', 'Ivan Drago', 'Russia', 'Men', 'Discus Throw', 'Silver'),
(30012, 2011, 'Paris', 'Athletics', 'Athletics', 'Tom Reed', 'USA', 'Men', 'Discus Throw', 'Bronze'),
(30013, 2012, 'London', 'Athletics', 'Athletics', 'Ivan Drago', 'Russia', 'Men', 'Discus Throw', 'Gold'),
(30014, 2012, 'London', 'Athletics', 'Athletics', 'Kenji Sato', 'Japan', 'Men', 'Discus Throw', 'Silver'),
(30015, 2012, 'London', 'Athletics', 'Athletics', 'Lars Holm', 'Sweden', 'Men', 'Discus Throw', 'Bronze'),
(30016, 2013, 'Moscow', 'Athletics', 'Athletics', 'Ivan Drago', 'Russia', 'Men', 'Discus Throw', 'Gold'),
(30017, 2013, 'Moscow', 'Athletics', 'Athletics', 'Markus Stein', 'Germany', 'Men', 'Discus Throw', 'Silver'),
(30018, 2013, 'Moscow', 'Athletics', 'Athletics', 'Kenji Sato', 'Japan', 'Men', 'Discus Throw', 'Bronze'),
(30019, 2014, 'Zurich', 'Athletics', 'Athletics', 'Lars Holm', 'Sweden', 'Men', 'Discus Throw', 'Gold'),
(30020, 2014, 'Zurich', 'Athletics', 'Athletics', 'Ivan Drago', 'Russia', 'Men', 'Discus Throw', 'Silver'),
(30021, 2014, 'Zurich', 'Athletics', 'Athletics', 'Tom Reed', 'USA', 'Men', 'Discus Throw', 'Bronze'),
(30022, 2015, 'Doha', 'Athletics', 'Athletics', 'Tom Reed', 'USA', 'Men', 'Discus Throw', 'Gold'),
(30023, 2015, 'Doha', 'Athletics', 'Athletics', 'Lars Holm', 'Sweden', 'Men', 'Discus Throw', 'Silver'),
(30024, 2015, 'Doha', 'Athletics', 'Athletics', 'Kenji Sato', 'Japan', 'Men', 'Discus Throw', 'Bronze'),
(30025, 2016, 'Rio', 'Athletics', 'Athletics', 'Tom Reed', 'USA', 'Men', 'Discus Throw', 'Gold'),
(30026, 2016, 'Rio', 'Athletics', 'Athletics', 'Ivan Drago', 'Russia', 'Men', 'Discus Throw', 'Silver'),
(30027, 2016, 'Rio', 'Athletics', 'Athletics', 'Markus Stein', 'Germany', 'Men', 'Discus Throw', 'Bronze'),
(30028, 2017, 'London', 'Athletics', 'Athletics', 'Kenji Sato', 'Japan', 'Men', 'Discus Throw', 'Gold'),
(30029, 2017, 'London', 'Athletics', 'Athletics', 'Tom Reed', 'USA', 'Men', 'Discus Throw', 'Silver'),
(30030, 2017, 'London', 'Athletics', 'Athletics', 'Lars Holm', 'Sweden', 'Men', 'Discus Throw', 'Bronze');