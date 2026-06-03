# Chapter 1 Opening: Introduction to Window Functions

## Introduction
This chapter introduces window functions in PostgreSQL and explains why they are useful for analysis workflows.

## Motivation
Analysts often need calculations across related rows while still keeping each original row visible.

## Course outline
The opening frames the course focus on summary statistics and window functions, with practical SQL patterns throughout.

## Summer Olympics dataset
The chapter uses a Summer Olympics dataset to make examples concrete and easy to compare across rows.

## Window functions
Window functions calculate values across a related set of rows tied to the current row.

## Row numbers
A common first example is assigning row positions in a result set.

## ROW_NUMBER
`ROW_NUMBER()` is introduced as the core ranking function that assigns sequential numbers.

## Anatomy of a window function
The opening breaks down function syntax and the role of `OVER()` as the window clause.

## Practice transition
The chapter closes by transitioning into hands-on practice with first window-function queries.