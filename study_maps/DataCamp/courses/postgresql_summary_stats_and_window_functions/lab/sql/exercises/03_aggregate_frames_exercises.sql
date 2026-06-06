\set ON_ERROR_STOP on
SET search_path TO dc_window_lab, public;

-- Exercise 1
-- Count medals per athlete, then calculate a running total ordered by
-- medal count descending and athlete ascending.
-- TODO.

-- Exercise 2
-- Count Gold medals per country and year.
-- Show the maximum annual Gold-medal count for each country beside every row.
-- TODO.

-- Exercise 3
-- Using the same data, show the minimum annual Gold-medal count per country.
-- TODO.

-- Exercise 4
-- Count medals by Scandinavian country and year for DEN, FIN, NOR, SWE.
-- Calculate a moving maximum using:
-- ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING.
-- TODO.

-- Exercise 5
-- Count medals by China and year.
-- Calculate a moving maximum using:
-- ROWS BETWEEN 2 PRECEDING AND CURRENT ROW.
-- TODO.

-- Exercise 6
-- Count Russian medals by year and calculate a three-row moving average.
-- TODO.

-- Exercise 7
-- Count medals per country and year.
-- Calculate a three-row moving total independently per country.
-- TODO.

-- Exercise 8
-- Write a SQL comment explaining the difference between ROWS and RANGE.
