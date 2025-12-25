from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex


class PostTableModel(QAbstractTableModel):
    """
    게시글 목록을 QTableView에 표시하기 위한 데이터 모델입니다.
    """
    def __init__(self, posts=None):
        """
        PostTableModel 초기화 메서드입니다.

        Args:
            posts (list[Post], optional): 표시할 게시글 리스트
        """
        super().__init__()
        self.posts = posts or []
        self._headers = ["No.", "Subject", "Author", "Date"]

    def rowCount(self, parent=QModelIndex()):
        """
        행(Row)의 개수를 반환합니다.
        """
        return len(self.posts)

    def columnCount(self, parent=QModelIndex()):
        """
        열(Column)의 개수를 반환합니다.
        """
        return len(self._headers)

    def data(self, index, role: Qt.DisplayRole):
        """
        특정 셀(index)에 표시할 데이터를 반환합니다.

        Args:
            index (QModelIndex): 데이터의 위치 정보
            role (int): 데이터의 역할 (DisplayRole 등)

        Returns:
            Any: 해당 셀에 표시할 데이터
        """
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            post = self.posts[index.row()]
            col = index.column()
            if col == 0:
                return str(post.id)
            if col == 1:
                return post.title
            if col == 2:
                return post.author
            if col == 3:
                return post.updated_at or post.created_at

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """
        헤더(컬럼명) 정보를 반환합니다.
        """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return None
