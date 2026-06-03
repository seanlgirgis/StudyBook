# Chapter 1 Opening Transcript: Data Types and INFORMATION_SCHEMA

## 1. Welcome!

Welcome to PostgreSQL Functions for Manipulating Data. Instructor Brian Piccolo introduces the course as a continuation of SQL fundamentals, focused on using built-in PostgreSQL functions and operators to extend database capabilities.

## 2. The Sakila Database

The course uses the Sakila Database, a sample database modeling a fictional DVD rental store. It is highly normalized and useful for sample queries, PostgreSQL data types, and custom functions.

## 3. Topics

The course covers:

* common PostgreSQL data types and their properties
* built-in functions and operators for date/time manipulation
* text parsing and text manipulation functions
* introduction to full-text search with PostgreSQL extensions

## 4. Common Data Types

Common PostgreSQL data types include:

* text data types: CHAR, VARCHAR, TEXT
* numeric data types: INT, DECIMAL
* date/time data types: DATE, TIME, TIMESTAMP, INTERVAL
* arrays

The instructor emphasizes that understanding data types is important when working with relational databases.

## 5. Text Data Types

CHAR and VARCHAR store fixed or varying numbers of characters.
TEXT stores character/string data and can be very long.

Examples from the film table:

* title uses a text-like type
* description uses TEXT

The course will later show how to extract substrings and manipulate text values.

## 6. Numeric Data Types

INT and DECIMAL store whole numbers and precise numeric values.

Examples:

* payment_id can be an integer
* amount can be a decimal

## 7. Determining Data Types from Existing Tables

When working with an existing database, you may need to inspect column data types before using functions.

A simple SELECT can make columns appear like text, but the actual data types may differ.

## 8. INFORMATION_SCHEMA

PostgreSQL stores metadata about database objects in INFORMATION_SCHEMA.

You can query INFORMATION_SCHEMA to find:

* column names
* data types
* table metadata

Example pattern:

SELECT
column_name,
data_type
FROM information_schema.columns
WHERE table_name = 'film';

In the film table, title and description are text-related types, while special_features is actually an ARRAY.

## 9. Practice Setup

The next practice asks the learner to inspect the customer table in the DVD Rentals database.
