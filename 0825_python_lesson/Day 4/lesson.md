# Day 4: Building a Simple ETL Pipeline

Today, we will build a simple ETL (Extract, Transform, Load) pipeline using Python and PostgreSQL.

## What is an ETL Pipeline?

An ETL pipeline is a set of processes that extracts data from a source, transforms it into a different format, and loads it into a destination.

*   **Extract:** Get data from a source (e.g., a CSV file, an API, a database).
*   **Transform:** Clean, process, and manipulate the data into the desired format.
*   **Load:** Load the transformed data into a destination (e.g., a data warehouse, a database).

## Our Simple ETL Pipeline

In our pipeline, we will:

1.  **Extract:** Read data from the `raw_data` table in our PostgreSQL database.
2.  **Transform:** Clean the data by removing unnecessary columns.
3.  **Load:** Load the cleaned data into the `clean_data` table in our PostgreSQL database.
