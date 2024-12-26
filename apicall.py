import requests
import mysql.connector


DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Replace with your MySQL username
    'password': 'passwd',  # Replace with your MySQL password
    'database': 'github_repos'  # Replace with your database name
}


GITHUB_TOKEN = "pattoken"  # Replace with your GitHub token
HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}


def fetch_github_data(language="Python", per_page=10):
    url = f"https://api.github.com/search/repositories?q=language:{language}&sort=stars&order=desc&per_page={per_page}"
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        print("Data fetched successfully from GitHub API.")
        return response.json()["items"]
    else:
        print(f"Failed to fetch data from GitHub API. Status Code: {response.status_code}")
        return None


def load_data_to_mysql(data):
    try:
        
        connection = mysql.connector.connect(**DB_CONFIG)

        if connection.is_connected():
            print("Connected to MySQL database.")
            cursor = connection.cursor()

            
            insert_query = """
                INSERT INTO github_repos (id, name, owner, stars, language, url)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                name = VALUES(name), owner = VALUES(owner), stars = VALUES(stars), 
                language = VALUES(language), url = VALUES(url);
            """

            
            for record in data:
                cursor.execute(insert_query, (
                    record['id'],
                    record['name'],
                    record['owner']['login'],
                    record['stargazers_count'],
                    record['language'],
                    record['html_url']
                ))

            
            connection.commit()
            print("Data inserted/updated successfully.")

    except mysql.connector.Error as e:
        print(f"Error: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection closed.")


def etl_process():
    print("Starting ETL process...")
    language = "Python"  # Change this to your desired language
    data = fetch_github_data(language)

    if data:
        load_data_to_mysql(data)
        print("data inserted!!")
    else:
        print("No data to load.")

if __name__ == "__main__":
    etl_process()
