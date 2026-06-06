\set ON_ERROR_STOP on
SET search_path TO dc_window_lab, public;

-- Exercise 1
-- Enable tablefunc if your PostgreSQL role has permission.
-- TODO: CREATE EXTENSION.

-- Exercise 2
-- Create a basic Gold-medal pivot for CHN, RUS, and USA for 2008 and 2012.
-- TODO: CROSSTAB query.

-- Exercise 3
-- Aggregate Gold medals by country and year, rank countries inside each year,
-- then pivot the ranks for 2008 and 2012.
-- TODO.

-- Exercise 4
-- For 2008 CHN and RUS medal rows, generate country-level subtotals by medal
-- using ROLLUP.
-- TODO.

-- Exercise 5
-- Generate all country/medal subtotal combinations with CUBE.
-- TODO.

-- Exercise 6
-- Use COALESCE to label subtotal NULL values.
-- TODO.

-- Exercise 7
-- Rank CHN, RUS, and USA by 2012 Gold medals and return one ordered,
-- comma-separated country list with STRING_AGG().
-- TODO.
