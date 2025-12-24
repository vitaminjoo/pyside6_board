from PySide6.QtCore import Signal, QModelIndex
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableView, QPushButton, QAbstractItemView, \
    QHeaderView, QMessageBox

from app.models import Post
from app.views import PostTableModel


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
        # TODO: UX 고려해서 버튼 배치하기
        layout = QVBoxLayout()
        self.table = QTableView()

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        pagination_layout = QHBoxLayout()
        pagination_layout.addStretch()

        self.btn_prev_jump = QPushButton("<<")
        self.btn_prev = QPushButton("<")
        self.btn_prev_jump.setFixedSize(30, 30)
        self.btn_prev.setFixedSize(30, 30)
        pagination_layout.addWidget(self.btn_prev_jump)
        pagination_layout.addWidget(self.btn_prev)

        self.page_buttons_layout = QHBoxLayout()
        self.page_buttons_layout.setSpacing(5)  # 버튼 사이 간격 5px
        pagination_layout.addLayout(self.page_buttons_layout)

        self.btn_next_jump = QPushButton(">>")
        self.btn_next = QPushButton(">")
        self.btn_next_jump.setFixedSize(30, 30)
        self.btn_next.setFixedSize(30, 30)
        pagination_layout.addWidget(self.btn_next)
        pagination_layout.addWidget(self.btn_next_jump)
        pagination_layout.addStretch()  # 오른쪽 여백 밀기 (가운데 정렬됨)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        self.btn_post = QPushButton("Post")
        self.btn_remove = QPushButton("Remove")
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_post)
        btn_layout.addWidget(self.btn_remove)

        layout.addLayout(pagination_layout)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def init_signals(self):
        self.view_model.post_list_updated.connect(self.update_table)
        self.view_model.paging_info_updated.connect(self.update_paging_ui)
        self.table.doubleClicked.connect(self.on_double_click)
        self.btn_prev_jump.clicked.connect(lambda: self.view_model.go_prev_page(10))
        self.btn_prev.clicked.connect(lambda: self.view_model.go_prev_page(1))
        self.btn_next_jump.clicked.connect(lambda: self.view_model.go_next_page(10))
        self.btn_next.clicked.connect(lambda: self.view_model.go_next_page(1))
        self.btn_post.clicked.connect(self.request_post_signal.emit)
        self.btn_remove.clicked.connect(self.delete_selected_posts)

    def update_table(self, posts: list[Post]):
        self.current_posts = posts
        self.model = PostTableModel(posts)
        self.table.setModel(self.model)

    def on_double_click(self, index: QModelIndex):
        row = index.row()
        if row < len(self.current_posts):
            selected_post = self.current_posts[row]
            self.request_read_signal.emit(selected_post)

    def delete_selected_posts(self):
        selected_indexes = self.table.selectionModel().selectedRows()

        if not selected_indexes:
            return

        msg = f"Are you sure you want to delete {len(selected_indexes)} posts?"
        reply = QMessageBox.question(self, "Delece Confirm", msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.No:
            return

        ids_to_delete = []
        for index in selected_indexes:
            row = index.row()
            if row < len(self.current_posts):
                ids_to_delete.append(self.current_posts[row].id)

        if ids_to_delete:
            self.view_model.delete_posts(ids_to_delete)

    def update_paging_ui(self, current, total):
        # 1. [청소] 기존 버튼 삭제
        while self.page_buttons_layout.count():
            child = self.page_buttons_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # --- [수정된 로직: 블록 단위 계산] ---
        # 한 화면에 보여질 페이지 버튼 개수 (1~10 이면 10개)
        items_per_block = 10

        # 현재 페이지가 속한 블록의 시작 번호 구하기 공식
        # 예: current가 5면 -> (4 // 10) * 10 + 1 = 1
        # 예: current가 15면 -> (14 // 10) * 10 + 1 = 11
        current_block = (current - 1) // items_per_block
        start_page = current_block * items_per_block + 1

        # 끝 번호는 시작 번호 + 9. 단, 전체 페이지(total)를 넘을 순 없음
        end_page = min(total, start_page + items_per_block - 1)
        # ----------------------------------

        # 2. [생성] 계산된 범위(start_page ~ end_page)만큼 버튼 만들기
        for page in range(start_page, end_page + 1):
            btn = QPushButton(str(page))
            btn.setFixedSize(30, 30)

            if page == current:
                btn.setStyleSheet("color: white; font-weight: bold;")
                btn.setEnabled(False)
            else:
                btn.setStyleSheet("color:gray")

            btn.clicked.connect(lambda checked, p=page: self.view_model.go_to_page(p))

            self.page_buttons_layout.addWidget(btn)

        # 3. 이전/다음 버튼 활성화 여부
        # (선택 사항) '이전' 버튼을 누르면 '이전 페이지(current-1)'로 갈지, '이전 블록(11->10)'으로 갈지 취향 차이입니다.
        # 여기서는 그냥 가장 기본적인 '1페이지라도 있으면 활성화'로 둡니다.
        self.btn_prev_jump.setEnabled(current > 1)
        self.btn_prev.setEnabled(current > 1)
        self.btn_next_jump.setEnabled(current < total)
        self.btn_next.setEnabled(current < total)
