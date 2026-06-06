SET search_path TO joining_data_lab;

-- Challenge 1
-- Return every country with its 2015 population and 2015 GDP per capita.
-- Preserve countries even when one of the 2015 facts is missing.

-- Challenge 2
-- Find countries that have population data for both 2010 and 2015.

-- Challenge 3
-- Find countries that have no city rows.

-- Challenge 4
-- Return all distinct country codes appearing anywhere in populations or economies.

-- Challenge 5
-- Return country-year pairs that exist in populations but not economies.

-- Challenge 6
-- Show each country and the count of official languages.

-- Challenge 7
-- Create every country × target-year combination for 2010 and 2015,
-- then LEFT JOIN the actual population where available.

-- Challenge 8
-- Compare 2010 and 2015 populations using both:
--   a) a self join
--   b) conditional aggregation

-- Challenge 9
-- Explain why the NOT IN query in 06_subqueries.sql may return no rows.

-- Challenge 10
-- Build one final report with:
-- country name, region, 2015 population, 2015 GDP per capita,
-- official language count, and a flag showing whether the country has any city.
