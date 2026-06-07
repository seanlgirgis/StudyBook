SET search_path TO dc_functions, public;

INSERT INTO customer VALUES
(1, ' sean ', 'girgis', 'Sean.Girgis@example.com', DATE '2026-01-10'),
(2, 'ANNA', 'GIRGIS', 'anna.girgis@example.com', DATE '2026-02-15'),
(3, 'Maya', 'Nabil', 'maya.nabil@example.org', DATE '2026-03-01'),
(4, 'Omar', 'Saleh', 'invalid-email', DATE '2026-03-20');

INSERT INTO film VALUES
(101, 'GAMBOL MOON', 'A Astounding story about a moonlit journey.', 3, 2.99, ARRAY['Trailers','Commentaries']),
(102, 'ELF RIVER', 'An elf follows a river into a hidden forest.', 5, 3.99, ARRAY['Deleted Scenes','Trailers']),
(103, 'DATABASE DREAMS', 'A practical documentary about data systems.', 2, 1.99, ARRAY['Commentaries']),
(104, 'POSTGRES PATH', 'A developer learns powerful PostgreSQL functions.', 4, 4.99, ARRAY['Trailers']),
(105, 'SILENT ARRAY', 'A quiet collection of unusual values.', 7, 2.49, ARRAY[]::text[]);

INSERT INTO rental VALUES
(1001, 1, 101, TIMESTAMP '2026-01-05 10:00', TIMESTAMP '2026-01-07 12:30'),
(1002, 1, 102, TIMESTAMP '2026-01-29 09:15', TIMESTAMP '2026-02-03 10:00'),
(1003, 2, 103, TIMESTAMP '2026-02-10 14:00', TIMESTAMP '2026-02-11 08:00'),
(1004, 3, 104, TIMESTAMP '2026-03-04 18:00', TIMESTAMP '2026-03-10 18:30'),
(1005, 4, 105, TIMESTAMP '2026-03-20 11:00', NULL),
(1006, 2, 102, TIMESTAMP '2026-04-02 16:45', TIMESTAMP '2026-04-05 12:00');
