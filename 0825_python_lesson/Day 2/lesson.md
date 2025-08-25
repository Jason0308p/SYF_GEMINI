# Day 2: Introduction to Relational Databases & SQL

Today, we'll dive into the world of relational databases and learn the basics of SQL.

## Relational Databases

A relational database organizes data into tables, which are composed of rows and columns. Each table has a **primary key**, which is a unique identifier for each row.

Tables can be related to each other using **foreign keys**. A foreign key is a key used to link two tables together. It is a field (or collection of fields) in one table that refers to the PRIMARY KEY in another table.

## SQL Basics

SQL (Structured Query Language) is the language we use to interact with relational databases.

### Key SQL Commands

*   `SELECT`: Used to query the database and retrieve data that matches criteria that you specify.
*   `INSERT`: Used to add new rows of data to a table in the database.
*   `UPDATE`: Used to modify existing records in a database.
*   `DELETE`: Used to remove existing records from a table.
*   `CREATE TABLE`: Used to create a new table in your database.
*   `JOIN`: Used to combine rows from two or more tables, based on a related column between them.

We will be using the `raw_data` and `clean_data` tables we defined in the `setup_postgres.sql` script.
