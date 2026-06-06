-- Course 06 PostgreSQL Functions Lab
-- Purpose:
-- Reset and create the schema used by the local runnable lab.

DROP SCHEMA IF EXISTS course06_functions_lab CASCADE;

CREATE SCHEMA course06_functions_lab;

SET search_path TO course06_functions_lab;
