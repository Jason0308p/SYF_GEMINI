-- This script provides the SQL commands to set up your PostgreSQL database.
-- You will need to have PostgreSQL installed and running.
-- You can run these commands using a PostgreSQL client like psql or a GUI tool like DBeaver.

-- 1. Create a new database
CREATE DATABASE week_long_project;

-- 2. Connect to the new database
\c week_long_project

-- 3. Create a table for our raw data
CREATE TABLE raw_data (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(50),
    gender VARCHAR(50),
    ip_address VARCHAR(20)
);

-- 4. Create a table for our clean data
CREATE TABLE clean_data (
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(50)
);
