import urllib.parse
import mysql.connector
from mysql.connector import errorcode
import pandas as pd


def execute_sql_query(sql, db_url):
    # Parse the URL to get connection parameters
    parsed_url = urllib.parse.urlparse(db_url)
    username = parsed_url.username
    password = parsed_url.password
    host = parsed_url.hostname
    port = parsed_url.port or 3306
    database = parsed_url.path[1:]  # Removing the leading '/'

    # Connection parameters
    connection_params = {
        "user": username,
        "password": password,
        "host": host,
        "port": port,
        "database": database,
    }

    query = sql

    try:
        # Establish a connection to MySQL
        conn = mysql.connector.connect(**connection_params)

        # Create a cursor object
        cur = conn.cursor()

        # Execute the query
        try:
            cur.execute(query)
        except mysql.connector.Error as err:
            print("MySQL Error:", err)
            return "Query execution error"

        # Fetch all results
        query_results = cur.fetchall()

        # Get column names from the cursor description
        column_names = [col[0] for col in cur.description]

        # Create a Pandas DataFrame
        data_frame = pd.DataFrame(query_results, columns=column_names)

        return data_frame

    except mysql.connector.Error as err:
        print("MySQL Database Error:", err)

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # Close the cursor and connection
        try:
            cur.close()
        except:
            pass
        try:
            conn.close()
        except:
            pass
