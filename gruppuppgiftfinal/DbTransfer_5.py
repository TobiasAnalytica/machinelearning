import mysql.connector
from MLModelReturns_4 import validDict

def db_connection():
    """
    Skapar och returnerar en databasanslutning.
    """
    try:
        cnxn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sd8f7gsd786g87@$€{dfgedRG",
            database="news_db"
        )
        return cnxn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def insert_data(data, cnxn):
    """
    Infogar data från validDict i databasen.
    """
    cursor = cnxn.cursor()
    sql = """
    INSERT INTO news (title, summary, link, published, topic)
    VALUES (%s, %s, %s, %s, %s)
    """
    
    values = [(item['title'], item['summary'], item['link'], item['published'], item['topic']) for item in data]
    
    try:
        cursor.executemany(sql, values)
        cnxn.commit()
        print(f"{cursor.rowcount} records inserted successfully.")
    except mysql.connector.Error as err:
        print(f"Failed to insert records: {err}")
    finally:
        cursor.close()

def main():
    cnxn = db_connection()
    if cnxn:
        insert_data(validDict, cnxn)
        cnxn.close()
    else:
        print("Failed to connect to the database.")

if __name__ == "__main__":
    main()











"""
DbTransfer_5.py

This script will:
  - Import the final structured/validated data (e.g., `validDict`) from MLModelReturns_4.py
  - Connect to a MySQL database
  - Insert each record into a table (e.g., `news`) with columns: (title, summary, link, published, topic).

Students:
 - Fill out the pseudo code to connect to the DB, handle potential errors,
   and insert data in a loop or with executemany.


# from MLModelReturns_4 import validDict
import mysql.connector

def db_connection():
    
    Create and return a database connection.
    Pseudo code:
       - try to connect with mysql.connector.connect
       - return the connection object if successful
       - otherwise handle exceptions and return None
    
    # Example placeholder:
    # cnxn = mysql.connector.connect(
    #   host="localhost",
    #   user="root",
    #   password="password",
    #   database="my_database"
    # )
    # return cnxn
    pass

def insert_data(data, cnxn):
    
    Insert the provided data (list of dict) into the 'news' table.
    Each dict in 'data' is expected to have:
      - 'title'
      - 'summary'
      - 'link'
      - 'published'
      - 'topic'
    
    # Pseudo code:
    #   1) Create a cursor from cnxn
    #   2) Define an INSERT statement, e.g.:
    #      sql = "INSERT INTO news (title, summary, link, published, topic) VALUES (%s, %s, %s, %s, %s)"
    #   3) Transform data into a list of tuples
    #   4) Use cursor.executemany(sql, list_of_tuples)
    #   5) cnxn.commit()
    #   6) Close the cursor
    pass

def main():
    # 1. Connect to the DB
    cnxn = db_connection()
    
    if cnxn:
        # 2. Insert data
        # data = validDict  # from MLModelReturns_4
        # insert_data(data, cnxn)
        
        # 3. Close the connection
        cnxn.close()
    else:
        print("No database connection established.")

if __name__ == "__main__":
    main()
"""