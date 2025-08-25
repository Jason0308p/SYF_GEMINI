-- More advanced example for DROP TABLE
-- This command drops multiple tables if they exist.
-- The CASCADE option automatically drops objects that depend on the table (like foreign key constraints).

DROP TABLE IF EXISTS employees, departments CASCADE;
