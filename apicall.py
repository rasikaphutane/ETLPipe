import requests
import mysql.connector

# MySQL database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'Rasika@1809',  # Replace with your MySQL password
    'database': 'etldb'
}

# Function to fetch data from JSONPlaceholder API
def fetch_data_from_api():
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url)

    if response.status_code == 200:
        print("Data fetched successfully from API.")
        return response.json()
    else:
        print(f"Failed to fetch data from API. Status Code: {response.status_code}")
        return None

# Function to load data into MySQL
def load_data_to_mysql(data):
    try:
        # Connect to the MySQL database
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            print("Connected to MySQL database.")
            cursor = connection.cursor()

            # Insert query
            insert_query = """
                INSERT INTO posts (id, title, body, user_id)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                title = VALUES(title), body = VALUES(body), user_id = VALUES(user_id);
            """

            # Insert each record into the database
            for record in data:
                cursor.execute(insert_query, (
                    record['id'],
                    record['title'],
                    record['body'],
                    record['userId']
                ))

            # Commit the transaction
            connection.commit()
            print("Data inserted/updated successfully.")

    except mysql.connector.Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")

# Main ETL process
def etl_process():
    print("Starting ETL process...")
    data = fetch_data_from_api()

    if data:
        load_data_to_mysql(data)
    else:
        print("No data to load.")

# Run the ETL process
if __name__ == "__main__":
    etl_process()

