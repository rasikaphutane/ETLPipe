import streamlit as st
import pymysql
import pandas as pd


DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Your MySQL username
    'password': 'passwd',  # Your MySQL password
    'database': 'db'  # Your MySQL database name
}


def fetch_data_from_mysql():
    connection = None
    try:
        
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


def display_dashboard():
    st.title("GitHub Repositories Dashboard")
    st.write("This dashboard displays GitHub repository data fetched and stored in MySQL.")
    
   
    data = fetch_data_from_mysql()
    
    if data is not None and not data.empty:
        st.write("Displaying data from MySQL:")
        st.dataframe(data)  
    else:
        st.write("No data found in MySQL.")

def main():
    display_dashboard()

if __name__ == "__main__":
    main()
