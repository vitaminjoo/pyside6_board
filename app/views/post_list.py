from PySide6.QtCore import Signal, QModelIndex
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QTableView, QPushButton, QAbstractItemView, \
    QHeaderView, QMessageBox, QLineEdit

from app.models import Post
from app.views import PostTableModel


class PostListPage(QWidget):
    """
    게시글 목록을 보여주는 페이지입니다.
    검색, 페이징, 게시글 추가/삭제 기능을 제공합니다.
    """
    request_post_signal = Signal()
    request_read_signal = Signal(object)
    request_search_signal = Signal(str)

    def __init__(self, view_model):
        """
        PostListPage 초기화 메서드입니다.

        Args:
            view_model: 게시글 데이터와 로직을 관리하는 ViewModel 인스턴스
        """
        super().__init__()
        self.view_model = view_model
        self.current_posts = []
        self.init_ui()
        self.init_signals()

    def init_ui(self):
        """
        UI 컴포넌트들을 초기화하고 레이아웃을 구성합니다.
        검색창, 테이블 뷰, 페이징 버튼, 기능 버튼(추가/삭제)을 배치합니다.
        """
        layout = QVBoxLayout()

        # 검색 영역
        search_layout = QHBoxLayout()
        self.input_search = QLineEdit()
        self.input_search.returnPressed.connect(lambda: self.search_by_keyword(self.input_search.text()))
        self.btn_search = QPushButton("Search")
        search_layout.addStretch()
        search_layout.addWidget(self.input_search)
        search_layout.addWidget(self.btn_search)

        layout.addLayout(search_layout)

        # 게시글 목록 테이블
        self.table = QTableView()

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.ExtendedSelection)

        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        # 페이징 영역
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

        # 하단 기능 버튼 (작성, 삭제)
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
        """
        ViewModel의 시그널과 UI 이벤트를 연결합니다.
        """

        # ViewModel event 연결
        self.view_model.post_list_updated.connect(self.update_table)
        self.view_model.paging_info_updated.connect(self.update_paging_ui)

        # Table Double click event 연결
        self.table.doubleClicked.connect(self.on_double_click)

        # Pagination event 연결
        self.btn_prev_jump.clicked.connect(lambda checked: self.view_model.go_prev_page(10))
        self.btn_prev.clicked.connect(lambda checked: self.view_model.go_prev_page(1))
        self.btn_next_jump.clicked.connect(lambda checked: self.view_model.go_next_page(10))
        self.btn_next.clicked.connect(lambda checked: self.view_model.go_next_page(1))

        # 작성, 삭제, 검색 기능 event 연결
        self.btn_post.clicked.connect(self.request_post_signal.emit)
        self.btn_remove.clicked.connect(self.delete_selected_posts)
        self.btn_search.clicked.connect(lambda checked: self.search_by_keyword(self.input_search.text()))

    def update_table(self, posts: list[Post]):
        """
        ViewModel로부터 전달받은 게시글 목록으로 테이블을 갱신합니다.

        Args:
            posts (list[Post]): 게시글 객체 리스트
        """
        self.current_posts = posts
        self.model = PostTableModel(posts)
        self.table.setModel(self.model)

    def on_double_click(self, index: QModelIndex):
        """
        테이블의 행을 더블 클릭했을 때 상세 페이지로 이동 요청을 보냅니다.

        Args:
            index (QModelIndex): 클릭된 셀의 인덱스
        """
        row = index.row()
        if row < len(self.current_posts):
            selected_post = self.current_posts[row]
            self.request_read_signal.emit(selected_post)

    def delete_selected_posts(self):
        """
        선택된 게시글들을 삭제합니다. 삭제 전 확인 대화상자를 띄웁니다.
        """
        selected_indexes = self.table.selectionModel().selectedRows()

        if not selected_indexes:
            return

        msg = f"Are you sure you want to delete {len(selected_indexes)} posts?"
        reply = QMessageBox.question(self, "Delete Confirm", msg, QMessageBox.Yes, QMessageBox.No)

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
        """
        현재 페이지와 전체 페이지 수에 따라 페이징 버튼 UI를 갱신합니다.

        Args:
            current (int): 현재 페이지 번호
            total (int): 전체 페이지 수
        """

        while self.page_buttons_layout.count():
            child = self.page_buttons_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # 한 화면에 보여질 페이지 버튼 개수 (1~10 이면 10개)
        items_per_block = 10

        # 현재 페이지가 속한 블록의 시작 번호 구하기 공식
        current_block = (current - 1) // items_per_block
        start_page = current_block * items_per_block + 1

        # 끝 번호는 시작 번호 + 9. 단, 전체 페이지(total)를 넘을 순 없음
        end_page = min(total, start_page + items_per_block - 1)

        # 계산된 범위(start_page ~ end_page)만큼 버튼 만들기
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

        # 이전/다음 버튼 활성화 여부
        self.btn_prev_jump.setEnabled(current > 1)
        self.btn_prev.setEnabled(current > 1)
        self.btn_next_jump.setEnabled(current < total)
        self.btn_next.setEnabled(current < total)

    def search_by_keyword(self, keyword):
        """
        입력된 키워드로 게시글 검색을 요청합니다.

        Args:
            keyword (str): 검색어
        """
        self.view_model.search_posts(keyword)
