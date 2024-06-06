import psycopg2
import pandas as pd
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT
from ddl_queries import ddl_queries
from insert_queries import insert_queries
import os

def get_connection():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="postgres",
        host= "192.168.255.1",
        port=5435
    )
    return conn

def create_tables():
    try:
        # Connect to the database
        conn = get_connection()

        # Create a cursor object
        cursor = conn.cursor()

        # Execute each query to create tables
        for query_name, query in ddl_queries.items():
            cursor.execute(query)
            print(f"Table '{query_name}' created successfully.")

        # Commit the transaction
        conn.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error creating tables:", error)

    finally:
        # Close the cursor and connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            print("Connection closed.")

def fetch_data_from_csv(file_path):
    try:
        # Read data from CSV file
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        print("Error reading CSV file:", e)
        return None

def insert_data_into_table(conn, table_name, data):
    try:
        # Create a cursor object
        cursor = conn.cursor()

        # Iterate over rows in the DataFrame and insert data into the table
        for index, row in data.iterrows():
            # Prepare the INSERT query
            query = insert_queries[table_name].format(**row.to_dict())
            
            # print(query)
            # Execute the INSERT query
            cursor.execute(query)

        # Commit the transaction
        conn.commit()
        print("sucessfully inserted data")

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error inserting data into table '{table_name}':", error)
        # print("---------")

    finally:
        # Close the cursor
        if cursor:
            cursor.close()



def load_data_from_csv_and_insert():
    try:
        # Connect to the database
        conn = get_connection()

        # Load data from CSV files and insert into tables
        for table_name, query in insert_queries.items():
            file_path = f"processed_db/{table_name}.csv"  # Adjust the file path as per your directory structure
            data = fetch_data_from_csv(file_path)
            if data is not None:
                insert_data_into_table(conn, table_name, data)
                print(f"Tried inserting into table '{table_name}'.")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error:", error)

    finally:
        # Close the connection
        if conn:
            conn.close()
            print("Connection closed.")



#Call the function to create the tables
create_tables() 

# Call the function to load data from CSV files and insert into tables
load_data_from_csv_and_insert()

def fetch_data(query, params=None):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(query, params)
        data = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
    conn.close()
    return pd.DataFrame(data, columns=columns)

