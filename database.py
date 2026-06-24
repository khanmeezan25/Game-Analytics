import sqlite3
import os

# ===== Database name =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "Tennis.db")

def get_connection():
    conn = sqlite3.connect("Tennis.db")
    conn.execute("PRAGMA foreign_keys = ON")  # Enable foreign key to maintain relationship between tables
    return conn

# ===== Creating all tables =====

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # ----- 1. Categories Table -----
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id   VARCHAR(50) PRIMARY KEY,
            category_name VARCHAR(100) NOT NULL
        )
    """)

    # ----- 2. Competitions Table -----

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competitions (
            competition_id   VARCHAR(50)  PRIMARY KEY,
            competition_name VARCHAR(100) NOT NULL,
            parent_id        VARCHAR(50),
            type             VARCHAR(20) NOT NULL,
            gender           VARCHAR(10)  NOT NULL,
            category_id      VARCHAR(50), 
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    """)

    # ----- 3. Complexes Table -----

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS complexes (
            complex_id   VARCHAR(50)  PRIMARY KEY,
            complex_name VARCHAR(100)  NOT NULL
        )
    """)

    # ----- 4. Venues Table -----

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS venues (
            venue_id     VARCHAR(50) PRIMARY KEY,
            venue_name   VARCHAR(100) NOT NULL,
            city_name    VARCHAR(100) NOT NULL,
            country_name VARCHAR(100) NOT NULL,
            country_code CHAR(3) NOT NULL,
            timezone     VARCHAR(100) NOT NULL,
            complex_id   VARCHAR(50),
            FOREIGN KEY (complex_id) REFERENCES complexes(complex_id)
        )
    """)

    # -----  5. Competitors Ranking Table -----


    cursor.execute("""
         CREATE TABLE IF NOT EXISTS competitor_rankings (
            rank_id              INTEGER PRIMARY KEY AUTOINCREMENT,
            rank                 INTEGER NOT NULL,
            movement             INTEGER NOT NULL,
            points               INTEGER NOT NULL,
            competitions_played  INTEGER NOT NULL,
            competitor_id        VARCHAR(50),
            FOREIGN KEY (competitor_id) REFERENCES competitors(competitor_id)
        )
    """)

    # ----- 6. Competitors Table -----

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS competitors (
            competitor_id VARCHAR(50) PRIMARY KEY,
            name          VARCHAR(100) NOT NULL,
            country       VARCHAR(100) NOT NULL,
            country_code  CHAR(3) NOT NULL,
            abbreviation  VARCHAR(10) NOT NULL
        )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_tables() 
            
          
        