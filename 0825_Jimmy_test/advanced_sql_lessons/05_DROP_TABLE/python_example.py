import psycopg2

def drop_tables():
    """Drops the employees and departments tables from the database."""
    conn = psycopg2.connect("dbname=company_db user=your_user password=your_password")
    cur = conn.cursor()

    # Drop the tables
    cur.execute("DROP TABLE IF EXISTS employees, departments CASCADE")

    # Commit the changes
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

if __name__ == '__main__':
    drop_tables()
