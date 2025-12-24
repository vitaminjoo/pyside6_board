from dataclasses import dataclass


@dataclass
class Post:
    title: str
    content: str
    author: str = "anonymous"
    id: int = None
    created_at: str = None
    updated_at: str = None

    @staticmethod
    def create_table(conn):
        """
        posts 테이블 생성
        """
        cursor = conn.cursor()
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS posts
                       (
                           id         INTEGER PRIMARY KEY AUTOINCREMENT,
                           title      TEXT NOT NULL,
                           content    TEXT NOT NULL,
                           author     TEXT NOT NULL,
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                           updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                       )
                       ''')
        conn.commit()
