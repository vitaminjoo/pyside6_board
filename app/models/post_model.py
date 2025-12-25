from dataclasses import dataclass


@dataclass
class Post:
    """
    게시글 데이터를 담는 데이터 클래스입니다.
    """
    title: str
    content: str
    author: str = "anonymous"
    id: int = None
    created_at: str = None
    updated_at: str = None

    @staticmethod
    def create_table(conn):
        """
        데이터베이스에 posts 테이블을 생성합니다.
        이미 존재하는 경우 생성하지 않습니다.

        Args:
            conn: 데이터베이스 연결 객체
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
