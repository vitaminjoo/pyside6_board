import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QMessageBox

from app.database import db
from app.models import Post
from app.viewmodels import PostViewModel
from app.views import PostDetailPage, PostEditorPage, PostListPage

def init_app():
    """
    애플리케이션 초기화 함수입니다.
    데이터베이스 테이블을 생성합니다.
    """
    conn = db.get_connection()
    Post.create_table(conn)
    conn.close()


class MainWindow(QMainWindow):
    """
    애플리케이션의 메인 윈도우 클래스입니다.
    페이지 전환(QStackedWidget)과 전역 에러/알림 처리를 담당합니다.
    """
    def __init__(self):
        """
        MainWindow 초기화 메서드입니다.
        윈도우 설정, ViewModel 생성, UI 및 네비게이션을 초기화합니다.
        """
        super().__init__()
        self.setWindowTitle("DDE Free Board")
        self.resize(800, 600)

        self.view_model = PostViewModel()
        self.view_model.error_message_signal.connect(self.show_global_error)
        self.view_model.message_signal.connect(self.show_global_alarm)
        self.init_ui()
        self.init_navigation()

        self.view_model.fetch_posts()

    def init_ui(self):
        """
        UI 컴포넌트들을 초기화하고 스택 위젯에 페이지들을 추가합니다.
        """
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.list_page = PostListPage(self.view_model)
        self.detail_page = PostDetailPage(self.view_model)
        self.editor_page = PostEditorPage(self.view_model)

        self.stack.addWidget(self.list_page)
        self.stack.addWidget(self.detail_page)
        self.stack.addWidget(self.editor_page)

    def init_navigation(self):
        """
        각 페이지 간의 화면 전환 시그널을 연결합니다.
        """
        self.list_page.request_post_signal.connect(self.go_to_edit)
        self.list_page.request_read_signal.connect(self.go_to_detail)

        self.detail_page.request_go_list.connect(self.go_to_list)
        self.detail_page.request_edit_signal.connect(self.go_to_edit)

        self.editor_page.request_go_list.connect(self.go_to_list)
        self.editor_page.request_back_to_post.connect(self.go_to_detail)

    # 화면 전환 함수
    def go_to_list(self):
        """
        게시글 목록 페이지로 이동합니다.
        """
        self.stack.setCurrentIndex(0)

    def go_to_detail(self, post):
        """
        게시글 상세 페이지로 이동합니다.

        Args:
            post (Post): 상세 내용을 표시할 게시글 객체
        """
        self.detail_page.set_data(post)
        self.stack.setCurrentIndex(1)

    def go_to_edit(self, post=None):
        """
        게시글 작성/수정 페이지로 이동합니다.

        Args:
            post (Post, optional): 수정할 게시글 객체. None이면 새 글 작성.
        """
        self.editor_page.set_data(post)
        self.stack.setCurrentIndex(2)

    def show_global_error(self, message: str = None):
        """
        전역 에러 메시지를 표시합니다.

        Args:
            message (str): 표시할 에러 메시지
        """
        QMessageBox.critical(self, "Error", message)

    def show_global_alarm(self, message: str = None):
        """
        전역 알림 메시지를 표시합니다.

        Args:
            message (str): 표시할 알림 메시지
        """
        QMessageBox.about(self, "Alarm", message)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    init_app()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
