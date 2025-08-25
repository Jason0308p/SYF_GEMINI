import psycopg2
import pandas as pd

# Connect to your postgres DB
conn = psycopg2.connect("dbname=week_long_project user=your_user password=your_password")

# Open a cursor to perform database operations
cur = conn.cursor()

# Read the data from the CSV file
df = pd.read_csv('raw_data.csv')

# Insert the data into the raw_data table
for index, row in df.iterrows():
    cur.execute("INSERT INTO raw_data (id, first_name, last_name, email, gender, ip_address) VALUES (%s, %s, %s, %s, %s, %s)", (row['id'], row['first_name'], row['last_name'], row['email'], row['gender'], row['ip_address']))

# Commit the changes
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()
