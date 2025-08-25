-- More advanced example for CREATE TABLE
-- This command creates a new table with various constraints.
-- PRIMARY KEY: Uniquely identifies each record in a table.
-- FOREIGN KEY: Links a column in one table to the primary key of another table.
-- NOT NULL: Ensures that a column cannot have a NULL value.
-- UNIQUE: Ensures that all values in a column are different.
-- DEFAULT: Sets a default value for a column when no value is specified.

CREATE TABLE departments (
    id INT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE employees (
    id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    hire_date DATE DEFAULT CURRENT_DATE,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);
