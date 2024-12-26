import streamlit as st
import pymysql
import pandas as pd

# MySQL database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Your MySQL username
    'password': 'Rasika@1809',  # Your MySQL password
    'database': 'github_repos'  # Your MySQL database name
}

# Function to fetch data from MySQL using PyMySQL
def fetch_data_from_mysql():
    connection = None
    try:
        # Connect to MySQL database using PyMySQL
        connection = pymysql.connect(**DB_CONFIG)
        query = "SELECT * FROM github_repos"  # Table name to fetch
        data = pd.read_sql(query, connection)
        return data
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
        return None
    finally:
        if connection and connection.open:
            connection.close()

# Function to display the data in the Streamlit app
def display_dashboard():
    st.title("GitHub Repositories Dashboard")
    st.write("This dashboard displays GitHub repository data fetched and stored in MySQL.")
    
    # Fetch data from MySQL
    data = fetch_data_from_mysql()
    
    if data is not None and not data.empty:
        st.write("Displaying data from MySQL:")
        st.dataframe(data)  # Display the data as a table in the dashboard
    else:
        st.write("No data found in MySQL.")

# Main function
def main():
    display_dashboard()

if __name__ == "__main__":
    main()
