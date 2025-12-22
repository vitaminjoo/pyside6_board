import sqlite3
import os

from app.models.post_model import Post


class DatabaseManager:
    """
    데이터베이스 연결 및 초기화를 담당하는 클래스
    """

    def __init__(self, db_file="board.db"):
        # 현재 실행중인 파일의 위치를 기준으로 DB 경로 설정
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # 프로젝트 최상위 폴더에 DB 파일을 두기 위한 경로 계산
        project_root = os.path.dirname(base_dir)
        self.db_path = os.path.join(project_root, db_file)

    def get_connection(self):
        """
        DB 연결 객체를 생성하여 반환합니다.
        사용 후에는 반드시 con.close()를 호출해야 합니다
        => 왜?
        """
        conn = sqlite3.connect(self.db_path)
        # Row 팩토리 설정: 데이터를 튜플(1, '제목) 대신 딕셔너리 처럼 접근 가능하게 함(row['title'])
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        conn = self.get_connection()

        Post.create_table(conn)

        conn.close()
        print(f"DB 초기화 완료: {self.db_path}")

# 전역 인스턴스 생성

db = DatabaseManager()
