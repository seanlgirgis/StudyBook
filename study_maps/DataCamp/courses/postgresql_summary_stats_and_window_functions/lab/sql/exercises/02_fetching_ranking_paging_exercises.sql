\set ON_ERROR_STOP on
SET search_path TO dc_window_lab, public;

-- Exercise 1
-- Women’s Discus Throw Gold medalists from 2000 onward:
-- use LEAD(Athlete, 3) ordered by year.
-- TODO.

-- Exercise 2
-- Return all distinct male Gold medalists and the first athlete alphabetically
-- using FIRST_VALUE().
-- TODO.

-- Exercise 3
-- Return each Olympic host and the true last host city using LAST_VALUE().
-- Your frame must include UNBOUNDED FOLLOWING.
-- TODO.

-- Exercise 4
-- Count medals per athlete and rank athletes by medal count with RANK().
-- TODO.

-- Exercise 5
-- For Japan and Korea since 2000, keep athletes with more than one medal.
-- DENSE_RANK athletes inside each country by medals descending.
-- TODO.

-- Exercise 6
-- Split distinct events into 111 pages using NTILE().
-- TODO.

-- Exercise 7
-- Split multi-medal athletes into thirds by medal count.
-- TODO.

-- Exercise 8
-- In a second CTE, calculate the thirds.
-- In the outer query, calculate average medals per third.
-- TODO.
