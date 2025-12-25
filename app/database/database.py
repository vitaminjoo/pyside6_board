import os
import sqlite3
from contextlib import contextmanager

DB_FILE = "board.db"


class DatabaseManager:
    """
    데이터베이스 연결 및 초기화를 담당하는 클래스입니다.
    SQLite 데이터베이스 파일과의 연결을 관리합니다.
    """

    def __init__(self, db_file: str = "board.db"):
        """
        DatabaseManager 초기화 메서드입니다.
        DB 파일의 경로를 설정합니다.

        Args:
            db_file (str): 데이터베이스 파일 이름 (기본값: "board.db")
        """
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(base_dir)
        self.db_path = os.path.join(project_root, db_file)

    def get_connection(self) -> sqlite3.Connection:
        """
        SQLite 데이터베이스 연결 객체를 반환합니다.
        Row 팩토리를 설정하여 결과를 딕셔너리처럼 접근할 수 있게 합니다.

        Returns:
            sqlite3.Connection: 데이터베이스 연결 객체
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    @contextmanager
    def get_cursor(self):
        """
        데이터베이스 커서를 제공하는 컨텍스트 매니저입니다.
        작업 완료 시 자동으로 커밋하고, 예외 발생 시 롤백하며, 종료 시 연결을 닫습니다.

        Yields:
            sqlite3.Cursor: 데이터베이스 커서 객체
        """
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
