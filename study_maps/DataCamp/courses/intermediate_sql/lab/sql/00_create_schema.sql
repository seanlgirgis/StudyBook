-- Intermediate SQL course lab
-- Creates a dedicated PostgreSQL schema for this course.

DROP SCHEMA IF EXISTS intermediate_sql CASCADE;

CREATE SCHEMA intermediate_sql;

SET search_path TO intermediate_sql, public;
