from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QPushButton, QLineEdit, QMessageBox

from app.models.post_model import Post


class PostEditorPage(QWidget):
    request_go_list = Signal()
    request_back_to_post = Signal(object)

    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.current_post = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.lable_title = QLabel("제목")
        self.input_title = QLineEdit()
        self.input_title.setPlaceholderText("제목을 입력하세요")
        layout.addWidget(self.lable_title)
        layout.addWidget(self.input_title)

        self.input_content = QTextEdit()
        self.input_content.setPlaceholderText("내용을 입력하세요")
        layout.addWidget(self.input_content)

        self.lable_author = QLabel("작성자")
        self.input_author = QLineEdit()
        self.lable_date = QLabel("작성일")
        layout.addWidget(self.lable_author)
        layout.addWidget(self.input_author)
        layout.addWidget(self.lable_date)


        btn_layout = QHBoxLayout()
        self.btn_go_list = QPushButton("List")
        self.btn_back = QPushButton("Back")
        self.btn_save = QPushButton("Post")

        btn_layout.addWidget(self.btn_go_list)
        btn_layout.addWidget(self.btn_back)
        btn_layout.addWidget(self.btn_save)

        btn_delete_layout = QHBoxLayout()
        self.btn_delete = QPushButton("Delete")
        btn_delete_layout.addWidget(self.btn_delete)

        layout.addLayout(btn_layout)
        layout.addLayout(btn_delete_layout)

        self.setLayout(layout)

        self.btn_save.clicked.connect(self.save_post)
        self.btn_go_list.clicked.connect(self.request_go_list.emit)
        self.btn_back.clicked.connect(self.back_to_post)
        # self.btn.delete.clicked.connect()


    def set_data(self, post=None):
        if post:
            self.current_post_id = post.id
            self.input_title.setText(post.title)
            self.input_author.setText(post.author)
            self.input_content.setText(post.content)
            self.lable_date.setText(post.updated_at or post.created_at)
            self.btn_save.setText("Edit")
        else:
            self.current_post_id = None
            self.input_title.clear()
            self.input_author.clear()
            self.input_content.clear()

            self.btn_back.setVisible(False)
            self.btn_delete.setVisible(False)
            self.btn_save.setText("Post")

    def save_post(self):
        id = self.current_post_id
        title = self.input_title.text().strip()
        author = self.input_author.text().strip()
        content = self.input_content.toPlainText().strip()

        if not title or not content:
            QMessageBox.warning(self, "알림", "제목과 내용을 입력해주세요.")
            return

        isPass = False
        if id:
            isPass = self.view_model.update_post(id, title, author, content)
        else:
            isPass = self.view_model.add_post(title, content, author)

        if isPass:
            QMessageBox.about(self, "작성 완료", "글이 정상적으로 게시됐습니다.")
            self.request_go_list.emit()

    def back_to_post(self):
        post = self.view_model.get_post(self.current_post_id)
        self.request_back_to_post.emit(post)


