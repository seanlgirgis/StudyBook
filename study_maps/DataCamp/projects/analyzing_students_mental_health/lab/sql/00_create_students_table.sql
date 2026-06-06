-- DataCamp Project: Analyzing Students' Mental Health
-- File: lab/sql/00_create_students_table.sql
--
-- Purpose:
--   Create a local PostgreSQL copy of the DataCamp students dataset.
--
-- Source:
--   source_material/students.csv
--
-- Notes:
--   1. Columns are defined in the same order as the CSV.
--   2. The CSV header contains a leading space before "phone".
--      The local PostgreSQL column is normalized to phone.
--   3. Columns remain nullable so the local table preserves the source data.

DROP TABLE IF EXISTS students;

CREATE TABLE students (
    inter_dom        text,
    region           text,
    gender           text,
    academic         text,
    age              integer,
    age_cate         integer,
    stay             integer,
    stay_cate        text,
    japanese         integer,
    japanese_cate    text,
    english          integer,
    english_cate     text,
    intimate         text,
    religion         text,
    suicide          text,
    dep              text,
    deptype          text,
    todep            integer,
    depsev           text,
    tosc             integer,
    apd              integer,
    ahome            integer,
    aph              integer,
    afear            integer,
    acs              integer,
    aguilt           integer,
    amiscell         integer,
    toas             integer,
    partner          integer,
    friends          integer,
    parents          integer,
    relative         integer,
    profess          integer,
    phone            integer,
    doctor           integer,
    reli             integer,
    alone            integer,
    others           integer,
    internet         integer,
    partner_bi       text,
    friends_bi       text,
    parents_bi       text,
    relative_bi      text,
    professional_bi  text,
    phone_bi         text,
    doctor_bi        text,
    religion_bi      text,
    alone_bi         text,
    others_bi        text,
    internet_bi      text
);

COMMENT ON TABLE students IS
'Local PostgreSQL copy of the DataCamp Analyzing Students Mental Health project dataset.';

COMMENT ON COLUMN students.inter_dom IS
'Student type: international or domestic.';

COMMENT ON COLUMN students.stay IS
'Current length of stay in years.';

COMMENT ON COLUMN students.todep IS
'Total depression score from the PHQ-9 test.';

COMMENT ON COLUMN students.tosc IS
'Total social connectedness score from the SCS test.';

COMMENT ON COLUMN students.toas IS
'Total acculturative stress score from the ASISS test.';

-- Confirm the table structure after running this file:
-- \d students
