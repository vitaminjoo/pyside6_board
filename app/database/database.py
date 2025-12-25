import os
import sqlite3
import sys
from contextlib import contextmanager

DB_FILE = "board.db"


class DatabaseManager:
    def __init__(self, db_file: str = DB_FILE):
        """
        DB 파일의 경로를 설정합니다.
        """
        if getattr(sys, 'frozen', False):
            # 배포 환경 -> .exe 파일이 있는 폴더 기준 : (PyInstaller로 빌드 시 sys.executable은 exe 파일 경로임)
            base_dir = os.path.dirname(sys.executable)
        else:
            # 개발 환경 -> 현재 파일(database.py)의 위치를 기준으로 프로젝트 루트 찾기
            current_file_path = os.path.abspath(__file__)
            db_dir = os.path.dirname(current_file_path)
            app_dir = os.path.dirname(db_dir)
            base_dir = os.path.dirname(app_dir)

        self.db_path = os.path.join(base_dir, db_file)

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
