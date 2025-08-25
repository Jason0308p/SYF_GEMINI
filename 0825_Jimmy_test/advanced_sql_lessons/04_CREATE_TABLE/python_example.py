import psycopg2

def create_tables():
    """Creates the departments and employees tables in the database."""
    conn = psycopg2.connect("dbname=company_db user=your_user password=your_password")
    cur = conn.cursor()

    # Create the departments table
    cur.execute("""
        CREATE TABLE departments (
            id INT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE
        );
    """)

    # Create the employees table
    cur.execute("""
        CREATE TABLE employees (
            id INT PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name VARCHAR(50) NOT NULL,
            email VARCHAR(100) UNIQUE,
            hire_date DATE DEFAULT CURRENT_DATE,
            department_id INT,
            FOREIGN KEY (department_id) REFERENCES departments(id)
        );
    """)

    # Commit the changes
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

if __name__ == '__main__':
    create_tables()
