from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableView, QPushButton, QAbstractItemView, QHeaderView
from PySide6.QtCore import Signal

from app.views.post_table_model import PostTableModel

class PostListPage(QWidget):
    request_post_signal = Signal()
    request_read_signal = Signal(object)

    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        # 읽기 전용이니까 tuple도 괜찮지 않을까?
        self.current_posts = []
        self.init_ui()
        self.init_signals()

    def init_ui(self):
        #TODO: UX 고려해서 버튼 배치하기
        layout = QVBoxLayout()
        self.table = QTableView()

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        self.btn_post = QPushButton("Post")
        self.btn_remove = QPushButton("Remove")
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_post)
        btn_layout.addWidget(self.btn_remove)

        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def init_signals(self):
        self.view_model.post_list_updated.connect(self.update_table)
        self.table.doubleClicked.connect(self.on_double_click)
        self.btn_post.clicked.connect(self.request_post_signal.emit)

    def update_table(self, posts):
        self.current_posts = posts
        self.model = PostTableModel(posts)
        self.table.setModel(self.model)

    def on_double_click(self, index):
        row = index.row()

        if row < len(self.current_posts):
            selected_post = self.current_posts[row]

            self.request_read_signal.emit(selected_post)