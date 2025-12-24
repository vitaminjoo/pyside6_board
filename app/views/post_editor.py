from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QPushButton, QLineEdit


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

        btn_to_list_layout = QHBoxLayout()
        self.btn_go_list = QPushButton("List")
        btn_to_list_layout.addWidget(self.btn_go_list)
        layout.addLayout(btn_to_list_layout)

        self.lable_title = QLabel("Subject")
        self.input_title = QLineEdit()
        self.input_title.setPlaceholderText("Please enter your subject")
        layout.addWidget(self.lable_title)
        layout.addWidget(self.input_title)

        self.lable_author = QLabel("Author")
        self.input_author = QLineEdit()
        self.input_author.setPlaceholderText("Please enter your author name")
        layout.addWidget(self.lable_author)
        layout.addWidget(self.input_author)

        self.input_content = QTextEdit()
        self.input_content.setPlaceholderText("Please enter your content")
        self.input_content.setTabChangesFocus(True)
        layout.addWidget(self.input_content)

        btn_layout = QHBoxLayout()
        self.btn_back = QPushButton("Back")
        self.btn_save = QPushButton("Post")

        btn_layout.addWidget(self.btn_back)
        btn_layout.addWidget(self.btn_save)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        self.btn_save.clicked.connect(self.save_post)
        self.btn_go_list.clicked.connect(self.request_go_list.emit)
        self.btn_back.clicked.connect(self.back_to_post)

    def set_data(self, post=None):
        if post:
            self.current_post_id = post.id
            self.input_title.setText(post.title)
            self.input_author.setText(post.author)
            self.input_content.setText(post.content)

            self.btn_back.setVisible(True)
            self.btn_save.setText("Save")
        else:
            self.current_post_id = None
            self.input_title.clear()
            self.input_author.clear()
            self.input_content.clear()

            self.btn_back.setVisible(False)
            self.btn_save.setText("Post")

    def save_post(self):
        id = self.current_post_id
        title = self.input_title.text().strip()
        content = self.input_content.toPlainText().strip()
        author = self.input_author.text().strip()

        if not title or not content:
            self.view_model.message_signal.emit("Please enter title and content")
            return

        isPass = False
        if id:
            isPass = self.view_model.update_post(id, title, content, author)
        else:
            isPass = self.view_model.add_post(title, content, author)

        if isPass:
            self.request_go_list.emit()

    def back_to_post(self):
        post = self.view_model.get_post(self.current_post_id)
        self.request_back_to_post.emit(post)
