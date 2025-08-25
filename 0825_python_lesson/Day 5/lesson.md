# Day 5: Introduction to Data Warehousing

Today, we will learn about data warehouses and how they differ from traditional databases.

## What is a Data Warehouse?

A data warehouse is a large, centralized repository of data that is used for reporting and data analysis. It is designed to handle large volumes of historical data and to support complex queries.

## Database vs. Data Warehouse

| Feature | Database (OLTP) | Data Warehouse (OLAP) |
| :--- | :--- | :--- |
| **Purpose** | To store and manage transactional data | To store and analyze historical data |
| **Data** | Real-time, current data | Historical data |
| **Queries** | Simple, fast queries | Complex, analytical queries |
| **Users** | End-users, applications | Business analysts, data scientists |
| **Examples** | PostgreSQL, MySQL, SQL Server | Amazon Redshift, Google BigQuery, Snowflake |

## Star Schema

The star schema is a common data modeling technique used in data warehouses. It consists of a central **fact table** that is connected to multiple **dimension tables**.

*   **Fact Table:** Contains the quantitative data (measures) for analysis. For example, sales amount, number of units sold.
*   **Dimension Tables:** Contain descriptive attributes that are used to filter and group the data. For example, time, product, location.

This structure is called a star schema because the diagram resembles a star, with the fact table at the center and the dimension tables radiating out from it.
