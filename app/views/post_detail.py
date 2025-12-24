from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextBrowser, QMessageBox

from app.models import Post


class PostDetailPage(QWidget):
    request_go_list = Signal()
    request_edit_signal = Signal(object)
    request_delete_signal = Signal(object)

    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.current_post = None
        self.init_ui()

    def init_ui(self):
        # TODO: UX 고려해서 재배치 필요
        layout = QVBoxLayout()

        self.lable_title = QLabel("제목")
        self.lable_title.setWordWrap(True)
        layout.addWidget(self.lable_title)

        self.label_info = QLabel("작성자 | 작성일")
        layout.addWidget(self.label_info)

        self.text_content = QTextBrowser()
        layout.addWidget(self.text_content)

        btn_layout = QHBoxLayout()
        self.btn_go_list = QPushButton("List")
        self.btn_edit = QPushButton("Edit")
        self.btn_delete = QPushButton("Delete")

        btn_layout.addWidget(self.btn_go_list)
        btn_layout.addWidget(self.btn_edit)
        btn_layout.addWidget(self.btn_delete)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

        self.btn_go_list.clicked.connect(self.request_go_list.emit)
        self.btn_edit.clicked.connect(self.on_edit_clicked)
        self.btn_delete.clicked.connect(self.on_delete_clicked)

    def set_data(self, post: Post):
        self.current_post = post

        self.lable_title.setText(post.title)
        date_str = post.updated_at if post.updated_at else post.created_at
        info_text = f"author: {post.author} | date: {date_str}"
        self.label_info.setText(info_text)

        self.text_content.setText(post.content)

    def on_edit_clicked(self):
        if self.current_post:
            self.request_edit_signal.emit(self.current_post)

    def on_delete_clicked(self):
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
