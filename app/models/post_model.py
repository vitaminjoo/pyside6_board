class Post:
    """
    게시글 데이터 구조 정의 클래스 (DTO)
    """
    def __init__(self, title, content, id=None, author="anonymous", created_at=None, updated_at=None):
        self.id = id
        self.title = title
        self.content = content
        self.author = author
        self.created_at = created_at
        self.updated_at = updated_at

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
