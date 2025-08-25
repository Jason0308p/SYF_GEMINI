# Final Exam

**1. What is the difference between a data engineer and a data scientist?**

**2. What is a Pandas DataFrame and how do you create one?**

**3. Write a SQL query to select all columns from a table called `users` where the `country` is 'Canada'.**

**4. What is the purpose of the `psycopg2` library in Python?**

**5. What are the three main steps in an ETL pipeline?**

**6. What is the difference between a database and a data warehouse?**

**7. What is a star schema and what are its components?**

**8. What is data orchestration and why is it important?**

**9. What is Apache Airflow and what is a DAG?**

**10. Write a Python script to read a CSV file called `data.csv`, remove any rows with missing values, and write the cleaned data to a new CSV file called `clean_data.csv`.**

---

## Answers

**1. What is the difference between a data engineer and a data scientist?**

A data engineer is responsible for building and maintaining the data infrastructure and pipelines, while a data scientist is responsible for analyzing data to extract insights and build machine learning models.

**2. What is a Pandas DataFrame and how do you create one?**

A Pandas DataFrame is a 2-dimensional labeled data structure with columns of potentially different types. You can create one from a dictionary or by reading a CSV file.

```python
import pandas as pd

# From a dictionary
df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

# From a CSV file
df = pd.read_csv('data.csv')
```

**3. Write a SQL query to select all columns from a table called `users` where the `country` is 'Canada'.**

```sql
SELECT * FROM users WHERE country = 'Canada';
```

**4. What is the purpose of the `psycopg2` library in Python?**

`psycopg2` is a PostgreSQL database adapter for Python, used to connect to and interact with PostgreSQL databases.

**5. What are the three main steps in an ETL pipeline?**

Extract, Transform, and Load.

**6. What is the difference between a database and a data warehouse?**

A database is designed for transactional data and real-time operations (OLTP), while a data warehouse is designed for analytical data and historical reporting (OLAP).

**7. What is a star schema and what are its components?**

A star schema is a data modeling technique used in data warehouses. It consists of a central fact table (containing measures) and multiple dimension tables (containing descriptive attributes).

**8. What is data orchestration and why is it important?**

Data orchestration is the automation of data pipelines. It is important for managing complex pipelines, scheduling, handling dependencies, and monitoring.

**9. What is Apache Airflow and what is a DAG?**

Apache Airflow is an open-source data orchestration tool. A DAG (Directed Acyclic Graph) is a way to define a data pipeline as a graph of tasks in Airflow.

**10. Write a Python script to read a CSV file called `data.csv`, remove any rows with missing values, and write the cleaned data to a new CSV file called `clean_data.csv`.**

```python
import pandas as pd

df = pd.read_csv('data.csv')
df = df.dropna()
df.to_csv('clean_data.csv', index=False)
```
