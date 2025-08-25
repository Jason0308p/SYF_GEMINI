import sqlite3

# Connect to the database
conn = sqlite3.connect('test_database.db')

# Create a cursor
cursor = conn.cursor()

# Execute a query
cursor.execute("SELECT * FROM Customers")

# Fetch the results
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the connection
conn.close()
