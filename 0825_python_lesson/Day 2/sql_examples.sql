-- SQL Examples for Day 2

-- Select all data from the raw_data table
SELECT * FROM raw_data;

-- Select only the first_name and email columns from the raw_data table
SELECT first_name, email FROM raw_data;

-- Select data from the raw_data table where the gender is 'Female'
SELECT * FROM raw_data WHERE gender = 'Female';

-- Insert a new row into the raw_data table
INSERT INTO raw_data (id, first_name, last_name, email, gender, ip_address)
VALUES (6, 'John', 'Doe', 'johndoe@example.com', 'Male', '127.0.0.1');

-- Update a row in the raw_data table
UPDATE raw_data
SET email = 'newemail@example.com'
WHERE id = 6;

-- Delete a row from the raw_data table
DELETE FROM raw_data
WHERE id = 6;
