# SQL Cheat Sheet

## Basic Commands

*   `SELECT` - extracts data from a database
*   `UPDATE` - updates data in a database
*   `DELETE` - deletes data from a database
*   `INSERT INTO` - inserts new data into a database
*   `CREATE DATABASE` - creates a new database
*   `ALTER DATABASE` - modifies a database
*   `CREATE TABLE` - creates a new table
*   `ALTER TABLE` - modifies a table
*   `DROP TABLE` - deletes a table
*   `CREATE INDEX` - creates an index (search key)
*   `DROP INDEX` - deletes an index

## SELECT Statement

```sql
SELECT column1, column2, ...
FROM table_name;
```

## WHERE Clause

```sql
SELECT column1, column2, ...
FROM table_name
WHERE condition;
```

## ORDER BY Clause

```sql
SELECT column1, column2, ...
FROM table_name
ORDER BY column1, column2, ... ASC|DESC;
```

## INSERT INTO Statement

```sql
INSERT INTO table_name (column1, column2, column3, ...)
VALUES (value1, value2, value3, ...);
```

## UPDATE Statement

```sql
UPDATE table_name
SET column1 = value1, column2 = value2, ...
WHERE condition;
```

## DELETE Statement

```sql
DELETE FROM table_name WHERE condition;
```

## JOINs

*   `(INNER) JOIN`: Returns records that have matching values in both tables
*   `LEFT (OUTER) JOIN`: Returns all records from the left table, and the matched records from the right table
*   `RIGHT (OUTER) JOIN`: Returns all records from the right table, and the matched records from the left table
*   `FULL (OUTER) JOIN`: Returns all records when there is a match in either left or right table
