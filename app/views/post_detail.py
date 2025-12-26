from PySide6.QtCore import Signal, QSize
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextBrowser, QMessageBox

from app.models import Post
from app.utils import IconManager, DETAIL_STYLE


class PostDetailPage(QWidget):
    """
    게시글 상세 내용을 보여주는 페이지입니다.
    수정 및 삭제 기능을 제공합니다.
    """
    request_go_list = Signal()
    request_edit_signal = Signal(object)
    request_delete_signal = Signal(object)

    def __init__(self, view_model):
        """
        PostDetailPage 초기화 메서드입니다.

        Args:
            view_model: 게시글 데이터와 로직을 관리하는 ViewModel 인스턴스
        """
        super().__init__()
        self.view_model = view_model
        self.current_post = None
        self.init_ui()

        self.setStyleSheet(DETAIL_STYLE)

    def init_ui(self):
        """
        UI 컴포넌트들을 초기화하고 레이아웃을 구성합니다.
        제목, 작성자/날짜 정보, 본문 내용, 기능 버튼(목록, 수정, 삭제)을 배치합니다.
        """
        layout = QVBoxLayout()

        # 상단 기능 버튼 (목록, 수정, 삭제)
        nav_layout = QHBoxLayout()

        btn_to_list_layout = QHBoxLayout()
        self.btn_go_list = QPushButton("List")
        btn_to_list_layout.addWidget(self.btn_go_list)
        nav_layout.addLayout(btn_to_list_layout)
        nav_layout.addStretch()

        btn_func_layout = QHBoxLayout()
        self.btn_edit = QPushButton("Edit")
        self.btn_delete = QPushButton()
        self.btn_delete.setIcon(IconManager.get("delete"))
        self.btn_delete.setIconSize(QSize(20, 20))
        self.btn_delete.setObjectName("btn_delete")

        btn_func_layout.addWidget(self.btn_edit)
        btn_func_layout.addWidget(self.btn_delete)

        nav_layout.addLayout(btn_func_layout)
        layout.addLayout(nav_layout)

        # 제목 표시
        self.lable_title = QLabel("Subject")
        self.lable_title.setObjectName("lable_subject")
        self.lable_title.setWordWrap(True)

        layout.addWidget(self.lable_title)

        # 작성자 및 날짜 정보 표시
        info_layout = QVBoxLayout()

        author_layout = QHBoxLayout()
        self.label_author_info = QLabel("")
        self.label_date_info = QLabel("")
        author_layout.addStretch()
        author_layout.addWidget(self.label_author_info)
        author_layout.addWidget(self.label_date_info)

        info_layout.addLayout(author_layout)

        layout.addLayout(info_layout)

        # 본문 내용 표시 (읽기 전용)
        self.text_content = QTextBrowser()
        layout.addWidget(self.text_content)

        self.setLayout(layout)

        # 시그널 연결
        self.btn_go_list.clicked.connect(self.request_go_list.emit)
        self.btn_edit.clicked.connect(self.on_edit_clicked)
        self.btn_delete.clicked.connect(self.on_delete_clicked)

    def set_data(self, post: Post):
        """
        화면에 표시할 게시글 데이터를 설정합니다.

        Args:
            post (Post): 표시할 게시글 객체
        """
        self.current_post = post

        self.lable_title.setText(post.title)
        date_str = post.updated_at if post.updated_at else post.created_at

        self.label_author_info.setText(post.author)
        self.label_date_info.setText(date_str)

        self.text_content.setText(post.content)

    def on_edit_clicked(self):
        """
        수정 버튼 클릭 시 호출됩니다. 수정 요청 시그널을 발생시킵니다.
        """
        if self.current_post:
            self.request_edit_signal.emit(self.current_post)

    def on_delete_clicked(self):
        """
        삭제 버튼 클릭 시 호출됩니다. 확인 대화상자를 띄우고, 확인 시 삭제를 요청합니다.
        """
        if not self.current_post:
            return

        confirm_delete = QMessageBox.question(
            self,
            "Delete Confirm",
            f"Are you sure you want to delete this post?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm_delete == QMessageBox.Yes:
            self.view_model.delete_post(self.current_post.id)
            self.request_go_list.emit()
