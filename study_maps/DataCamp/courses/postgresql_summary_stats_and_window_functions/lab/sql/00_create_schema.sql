\set ON_ERROR_STOP on

DROP SCHEMA IF EXISTS dc_window_lab CASCADE;
CREATE SCHEMA dc_window_lab;

COMMENT ON SCHEMA dc_window_lab IS
'DataCamp PostgreSQL Summary Stats and Window Functions practice lab';

SET search_path TO dc_window_lab, public;
