import sqlite3

"""Manages background image storage using SQLite"""
class ImageDatabase():
    """Manages background image storage using SQLite"""
    def __init__(self, db_path: str = "config.db"):
        self.conn = sqlite3.connect(db_path)
        self._initialize_db()

    def _initialize_db(self) -> None:
        """Create table if not exists"""
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS background_image (
                    path TEXT PRIMARY KEY
                )
            """)

    def save_image(self, image_path: str) -> None:
        """Save new background image path"""
        with self.conn:
            self.conn.execute("DELETE FROM background_image")
            self.conn.execute("INSERT INTO background_image VALUES (?)", (image_path,))

    def get_image(self) -> str:
        """Retrieve stored background image path"""
        cursor = self.conn.execute("SELECT path FROM background_image LIMIT 1")
        result = cursor.fetchone()
        return result[0] if result else None

    def close(self) -> None:
        """Close database connection"""
        self.conn.close()