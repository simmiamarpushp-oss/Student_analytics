import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Load environment variables from .env file in the same directory
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=dotenv_path)

def get_db_connection():
    """Establishes a connection to the MySQL database and initializes it if necessary."""
    db_host = os.getenv('DB_HOST', 'localhost')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_name = os.getenv('DB_NAME', 'student_analytics')

    try:
        # Connect to MySQL server to create the database if it doesn't exist
        conn_server = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password
        )
        cursor_server = conn_server.cursor()
        cursor_server.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor_server.close()
        conn_server.close()

        # Now connect to the student_analytics database
        conn = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        
        if conn.is_connected():
            cursor = conn.cursor()
            
            # Construct path to the SQL file
            sql_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'database', 'students.sql')

            with open(sql_file_path, 'r') as f:
                # The mysql-connector can't handle multi-line comments in CREATE TABLE statements well with multi=True
                # Reading the single statement is safer.
                sql_script = f.read()

            # The CREATE TABLE statement in students.sql is idempotent due to "IF NOT EXISTS",
            # so it's safe to run every time.
            cursor.execute(sql_script)
            
            cursor.close()
            return conn
            
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None
    except FileNotFoundError:
        print(f"Error: 'database/students.sql' not found.")
        return None
