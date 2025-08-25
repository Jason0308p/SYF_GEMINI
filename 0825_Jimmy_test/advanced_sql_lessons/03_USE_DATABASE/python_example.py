import psycopg2

def connect_to_database(db_name):
    """Connects to a specific PostgreSQL database."""
    # In psycopg2, you specify the database to use when you connect.
    conn = psycopg2.connect(f"dbname={db_name} user=your_user password=your_password")
    cur = conn.cursor()

    # You are now connected to the specified database.
    print(f"Successfully connected to database: {db_name}")

    # Close the cursor and connection
    cur.close()
    conn.close()

if __name__ == '__main__':
    connect_to_database('company_db')
