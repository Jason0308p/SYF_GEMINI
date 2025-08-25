# Data Engineering Cheat Sheet

## Python (Pandas)

```python
import pandas as pd

# Create a DataFrame
df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})

# Read a CSV
df = pd.read_csv('data.csv')

# Write to a CSV
df.to_csv('output.csv', index=False)

# Select a column
df['col1']

# Filter rows
df[df['col1'] > 1]

# Group by a column
df.groupby('col1').sum()
```

## SQL

```sql
-- Select data
SELECT col1, col2 FROM my_table WHERE col1 > 1;

-- Create a table
CREATE TABLE my_table (col1 INT, col2 VARCHAR(255));

-- Insert data
INSERT INTO my_table (col1, col2) VALUES (1, 'a');

-- Update data
UPDATE my_table SET col2 = 'b' WHERE col1 = 1;

-- Delete data
DELETE FROM my_table WHERE col1 = 1;

-- Join tables
SELECT a.*, b.* FROM table_a a JOIN table_b b ON a.id = b.id;
```

## Command Line

```bash
# Navigate directories
cd my_folder

# List files
ls

# Run a Python script
python my_script.py

# Install a Python package
pip install pandas
```
