SET search_path TO dc_functions, public;

-- Literal pattern matching.
SELECT title, description
FROM film
WHERE title ILIKE '%elf%' OR description ILIKE '%elf%';

-- Full-text search.
SELECT title, description
FROM film
WHERE to_tsvector('english', title || ' ' || description)
      @@ to_tsquery('english', 'elf');

-- Inspect installed extensions.
SELECT extname, extversion
FROM pg_extension
ORDER BY extname;

-- OPTIONAL: run only with sufficient privileges.
-- CREATE EXTENSION IF NOT EXISTS pg_trgm;
-- CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;

-- After pg_trgm and fuzzystrmatch are available:
-- SELECT title,
--        similarity(title, 'GAMBOL') AS similarity_score,
--        levenshtein(lower(title), lower('GAMBOL')) AS edit_distance
-- FROM film
-- ORDER BY similarity_score DESC, edit_distance ASC;
