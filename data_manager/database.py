import sqlite3
from utils.logger import logger

DATABASE_NAME = "personal_shopper.db"

class DatabaseManager:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            self.conn = sqlite3.connect(DATABASE_NAME)
            self.conn.row_factory = sqlite3.Row
            logger.info(f"Connected to {DATABASE_NAME}")
        except sqlite3.Error as e:
            logger.error(f"Error connecting to database: {e}")
            raise

    def disconnect(self):
        if self.conn:
            self.conn.close()
            logger.info(f"Disconnected from database.")

    def _create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profiles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT UNIQUE,
                preferences TEXT, -- JSON string for preferences
                history TEXT    -- JSON string for search history
            )
        """)
        self.conn.commit()
        logger.info("Database tables checked/created.")
    
    def save_user_profile(self, user_id, preferences, history):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR REPLACE INTO user_profiles (user_id, preferences, history)
            VALUES (?, ?, ?)
        """, (user_id, preferences, history))
        self.conn.commit()
        logger.info(f"Saved profile for user: {user_id}")

    def get_user_profile(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM user_profiles WHERE user_id = ?", (user_id,))
        return cursor.fetchone()