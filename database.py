import psycopg2

def get_connection():
    conn = psycopg2.connect(host="localhost",database="movie_db",user="postgres",password="72145")
    return conn

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""CREATE TABLE IF NOT EXISTS favorite_movies(id INT PRIMARY KEY,title TEXT,
        overview TEXT,runtime INT, release_date VARCHAR(100),rating FLOAT, genre VARCHAR(100),poster TEXT,
        backdrop TEXT, is_favorite BOOLEAN DEFAULT FALSE)""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS watchlist_movies(id INT PRIMARY KEY,title TEXT,
                overview TEXT,runtime INT, release_date VARCHAR(100),rating FLOAT, genre VARCHAR(100),poster TEXT,
                backdrop TEXT)""")
        conn.commit()
    except psycopg2.Error as error:
        print("Database error:",error)
        if conn:
            conn.rollback() #to undo all changes that haven't been comitted yet
    finally:
        if conn:
            cursor.close()
            conn.close()