-- psql loading path (alternative to Python loader)
\set ON_ERROR_STOP on

DROP TABLE IF EXISTS students;

CREATE TABLE students (
    "index" INTEGER,
    inter_dom TEXT,
    region TEXT,
    gender TEXT,
    academic TEXT,
    age INTEGER,
    age_cate TEXT,
    stay INTEGER,
    stay_cate TEXT,
    japanese INTEGER,
    japanese_cate TEXT,
    english INTEGER,
    english_cate TEXT,
    intimate TEXT,
    religion TEXT,
    suicide TEXT,
    dep TEXT,
    deptype TEXT,
    todep INTEGER,
    depsev TEXT,
    tosc INTEGER,
    apd TEXT,
    ahome TEXT,
    aph TEXT,
    afear TEXT,
    acs TEXT,
    aguilt TEXT,
    amiscell TEXT,
    toas INTEGER,
    partner TEXT,
    friends TEXT,
    parents TEXT,
    relative TEXT,
    profess TEXT,
    phone TEXT,
    doctor TEXT,
    reli TEXT,
    alone TEXT,
    others TEXT,
    internet TEXT,
    partner_bi TEXT,
    friends_bi TEXT,
    parents_bi TEXT,
    relative_bi TEXT,
    professional_bi TEXT,
    phone_bi TEXT,
    doctor_bi TEXT,
    religion_bi TEXT,
    alone_bi TEXT,
    others_bi TEXT,
    internet_bi TEXT
);

\copy students FROM './data/raw/students.csv' WITH (FORMAT csv, HEADER true);

SELECT COUNT(*) AS loaded_rows FROM students;
SELECT * FROM students ORDER BY "index" NULLS LAST LIMIT 10;
