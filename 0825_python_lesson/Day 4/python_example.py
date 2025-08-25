import psycopg2

def etl_pipeline():
    """A simple ETL pipeline to extract, transform, and load data."""
    # Connect to the database
    conn = psycopg2.connect("dbname=week_long_project user=your_user password=your_password")
    cur = conn.cursor()

    # Extract data from the raw_data table
    cur.execute("SELECT id, first_name, last_name, email FROM raw_data")
    data = cur.fetchall()

    # Transform and load data into the clean_data table
    for row in data:
        cur.execute("INSERT INTO clean_data (id, first_name, last_name, email) VALUES (%s, %s, %s, %s)", row)

    # Commit the changes
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

if __name__ == '__main__':
    etl_pipeline()
