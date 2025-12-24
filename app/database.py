import sqlite3
import os
from contextlib import contextmanager

DB_FILE = "board.db"


class DatabaseManager:
    """
    데이터베이스 연결 및 초기화를 담당하는 클래스
    """
    def __init__(self, db_file: str = "board.db"):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(base_dir)
        self.db_path = os.path.join(project_root, db_file)

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        # Row 팩토리 설정: 데이터를 튜플(1, '제목) 대신 딕셔너리 처럼 접근 가능하게 함(row['title'])
        conn.row_factory = sqlite3.Row
        return conn

    @contextmanager
    def get_cursor(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

db = DatabaseManager()
