import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_database(db_name):
    """Creates a new PostgreSQL database."""
    # Connect to the default database
    conn = psycopg2.connect("dbname=postgres user=your_user password=your_password")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    # Create the new database
    cur.execute(f"CREATE DATABASE {db_name}")

    # Close the cursor and connection
    cur.close()
    conn.close()

if __name__ == '__main__':
    create_database('company_db')
