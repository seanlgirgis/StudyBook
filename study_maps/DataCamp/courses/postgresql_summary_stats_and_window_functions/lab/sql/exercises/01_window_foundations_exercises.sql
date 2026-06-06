\set ON_ERROR_STOP on
SET search_path TO dc_window_lab, public;

-- Exercise 1
-- Compare one grouped medal count per country with a window count that
-- preserves medal-level rows.
-- TODO: write both queries.

-- Exercise 2
-- Number all Gold medal rows chronologically using ROW_NUMBER().
-- Show year, event, athlete, country, and row number.
-- TODO: write query.

-- Exercise 3
-- Number Gold medal rows independently inside each country.
-- TODO: add PARTITION BY.

-- Exercise 4
-- For women’s Discus Throw Gold medalists from 2000 onward,
-- number champions by year.
-- TODO: write query.

-- Exercise 5
-- Explain in a SQL comment:
-- What is the difference between ORDER BY inside OVER() and the final ORDER BY?
