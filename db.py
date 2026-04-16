import mysql.connector
import json

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="actowiz",
        database="ipl"
    )

def create_tabel():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS ipl_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        match_name VARCHAR(255),
        match_date VARCHAR(255),
        winner VARCHAR(255),
        score JSON,
        match_url VARCHAR(255),
        innings JSON
    )
    """)

    conn.commit()
    conn.close()


def insert_single_match(d):
    conn = get_connection()
    cur = conn.cursor()

    query = """
    INSERT INTO ipl_data (match_name, match_date, winner, score, match_url, innings)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    cur.execute(query, (
        d.get('match'),
        d.get('date'),
        d.get('winner'),
        json.dumps(d.get('score')),
        d.get('match_url'),
        json.dumps(d.get('innings'))
    ))

    conn.commit()
    conn.close()

def match_url_exists(url):
    conn = get_connection()
    cur = conn.cursor()

    query = "SELECT match_url FROM ipl_data WHERE match_url = %s"
    cur.execute(query, (url,))

    result = cur.fetchone()
    conn.close()
    return result is not None

