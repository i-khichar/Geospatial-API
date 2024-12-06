import psycopg2

# Database configuration
DB_CONFIG = {
    "dbname": "karnataka_db",
    "user": "postgres",
    "password": "yourpassword",
    "host": "localhost",  # Or the IP of your PostgreSQL container
    "port": 5432          # Default PostgreSQL port
}

def run_sql_file(file_path):
    """Execute a SQL script from a file."""
    try:
        # Read the SQL file
        with open(file_path, "r") as file:
            sql_script = file.read()

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Execute the SQL script
        cursor.execute(sql_script)
        conn.commit()
        print(f"SQL script {file_path} executed successfully!")

    except Exception as e:
        print(f"Error executing SQL script {file_path}: {e}")
    finally:
        # Clean up
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Path to your SQL script file
    sql_file_path = "database/init.sql"
    run_sql_file(sql_file_path)
