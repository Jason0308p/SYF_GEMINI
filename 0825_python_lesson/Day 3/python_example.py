import psycopg2

def get_data_from_db():
    """Connects to the database and returns all data from the raw_data table."""
    conn = psycopg2.connect("dbname=week_long_project user=your_user password=your_password")
    cur = conn.cursor()
    cur.execute("SELECT * FROM raw_data")
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

if __name__ == '__main__':
    data = get_data_from_db()
    for row in data:
        print(row)
