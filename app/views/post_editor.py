from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QPushButton, QLineEdit

from app.utils import EDITOR_STYLE


class PostEditorPage(QWidget):
    """
    게시글을 작성하거나 수정하는 에디터 페이지입니다.
    """
    request_go_list = Signal()
    request_back_to_post = Signal(object)

    def __init__(self, view_model):
        """
        PostEditorPage 초기화 메서드입니다.

        Args:
            view_model: 게시글 데이터와 로직을 관리하는 ViewModel 인스턴스
        """
        super().__init__()
        self.view_model = view_model
        self.current_post_id = None
        self.init_ui()

        self.setStyleSheet(EDITOR_STYLE)

    def init_ui(self):
        """
        UI 컴포넌트들을 초기화하고 레이아웃을 구성합니다.
        제목, 작성자, 내용 입력 필드와 저장/취소 버튼을 배치합니다.
        """
        layout = QVBoxLayout()

        # 상단 기능 버튼 (목록, 저장/취소)
        nav_layout = QHBoxLayout()

        btn_to_list_layout = QHBoxLayout()
        self.btn_go_list = QPushButton("List")
        self.btn_cancel = QPushButton("Cancel")

        btn_to_list_layout.addWidget(self.btn_go_list)
        btn_to_list_layout.addWidget(self.btn_cancel)
        btn_to_list_layout.addStretch()
        nav_layout.addLayout(btn_to_list_layout)

        btn_layout = QHBoxLayout()
        self.btn_save = QPushButton("Post")
        self.btn_save.setObjectName("btn_post")
        btn_layout.addWidget(self.btn_save)
        nav_layout.addLayout(btn_layout)

        layout.addLayout(nav_layout)

        # 제목 입력
        self.lable_title = QLabel("Subject")
        self.input_title = QLineEdit()
        self.input_title.setPlaceholderText("Please enter your subject")
        layout.addWidget(self.lable_title)
        layout.addWidget(self.input_title)

        # 작성자 입력
        self.lable_author = QLabel("Author")
        self.input_author = QLineEdit()
        self.input_author.setPlaceholderText("Please enter your author name")
        layout.addWidget(self.lable_author)
        layout.addWidget(self.input_author)

        # 내용 입력
        self.input_content = QTextEdit()
        self.input_content.setPlaceholderText("Please enter your content")
        self.input_content.setTabChangesFocus(True)
        layout.addWidget(self.input_content)

        self.setLayout(layout)

        # 시그널 연결
        self.btn_save.clicked.connect(self.save_post)
        self.btn_go_list.clicked.connect(self.request_go_list.emit)
        self.btn_cancel.clicked.connect(self.back_to_post)

    def set_data(self, post=None):
        """
        에디터의 입력 필드를 초기화하거나 기존 게시글 데이터로 채웁니다.

        Args:
            post (Post, optional): 수정할 게시글 객체. None이면 새 글 작성 모드.
        """
        if post:
            self.current_post_id = post.id
            self.input_title.setText(post.title)
            self.input_author.setText(post.author)
            self.input_content.setText(post.content)

            self.input_author.setDisabled(True)
            self.btn_cancel.setVisible(True)
            self.btn_save.setText("Save")
        else:
            self.current_post_id = None
            self.input_title.clear()
            self.input_author.clear()
            self.input_content.clear()

            self.input_author.setDisabled(False)
            self.btn_cancel.setVisible(False)
            self.btn_save.setText("Post")

    def save_post(self):
        """
        작성된 내용을 저장합니다.
        새 글이면 추가(add), 기존 글이면 수정(update)을 수행합니다.
        """
        id = self.current_post_id
        title = self.input_title.text().strip()
        content = self.input_content.toPlainText().strip()
        author = self.input_author.text().strip()

        if not title or not content:
            self.view_model.message_signal.emit("Please enter title and content")
            return

        is_pass = False
        if id:
            is_pass = self.view_model.update_post(id, title, content, author)
        else:
            is_pass = self.view_model.add_post(title, content, author)

        if is_pass:
            self.request_go_list.emit()

    def back_to_post(self):
        """
        수정 취소 시 상세 페이지로 돌아갑니다.
        """
        post = self.view_model.get_post(self.current_post_id)
        self.request_back_to_post.emit(post)
