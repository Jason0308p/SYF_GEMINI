import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def drop_database(db_name):
    """Drops a PostgreSQL database."""
    # Connect to the default database
    conn = psycopg2.connect("dbname=postgres user=your_user password=your_password")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    # Drop the database
    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")

    # Close the cursor and connection
    cur.close()
    conn.close()

if __name__ == '__main__':
    drop_database('company_db')
