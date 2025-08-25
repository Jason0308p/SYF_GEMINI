# Day 3: Connecting Python to PostgreSQL

Today, we will learn how to connect to a PostgreSQL database from Python using the `psycopg2` library.

## `psycopg2`

`psycopg2` is the most popular PostgreSQL database adapter for the Python programming language. It is a DB API 2.0 compliant driver.

### Installation

To install `psycopg2`, you can use pip:

```bash
pip install psycopg2-binary
```

### Connecting to PostgreSQL

To connect to a PostgreSQL database, you need to provide the connection details, such as the database name, user, password, host, and port.

```python
import psycopg2

conn = psycopg2.connect(
    dbname="your_db_name",
    user="your_username",
    password="your_password",
    host="your_host",
    port="your_port"
)
```

Once you have a connection, you can create a **cursor** to execute SQL commands.

```python
cur = conn.cursor()

# Execute a command
cur.execute("SELECT * FROM my_table;")

# Fetch the results
results = cur.fetchall()

# Close the cursor and connection
cur.close()
conn.close()
```

Today, we will write a Python script to connect to our `week_long_project` database, execute a query, and print the results.
