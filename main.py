import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from app.database import db
from app.models.post_model import Post
from app.viewmodels.post_viewmodel import PostViewModel

from app.views.post_list import PostListPage
from app.views.post_detail import PostDetailPage
from app.views.post_editor import PostEditorPage

def init_app():
    conn = db.get_connection()
    Post.create_table(conn)
    conn.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DDE Free Board")
        self.resize(800, 600)

        self.view_model = PostViewModel()
        self.init_ui()
        self.init_navigation()

        self.view_model.fetch_posts()

    def init_ui(self):
        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.list_page = PostListPage(self.view_model)
        self.detail_page = PostDetailPage(self.view_model)
        self.editor_page = PostEditorPage(self.view_model)

        self.stack.addWidget(self.list_page)
        self.stack.addWidget(self.detail_page)
        self.stack.addWidget(self.editor_page)

    def init_navigation(self):
        self.list_page.request_post_signal.connect(self.go_to_edit)
        self.list_page.request_read_signal.connect(self.go_to_detail)
        self.detail_page.request_go_list.connect(self.go_to_list)
        self.detail_page.request_edit_signal.connect(self.go_to_edit)
        self.editor_page.request_go_list.connect(self.go_to_list)
        self.editor_page.request_back_to_post.connect(self.go_to_detail)

    # 화면 전환 함수
    def go_to_list(self):
        self.stack.setCurrentIndex(0)
    def go_to_detail(self, post):
        self.detail_page.set_data(post)
        self.stack.setCurrentIndex(1)
    def go_to_edit(self, post=None):
        self.editor_page.set_data(post)
        self.stack.setCurrentIndex(2)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    init_app()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())