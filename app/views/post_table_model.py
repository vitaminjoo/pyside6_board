import re

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
            # 0 번째 컬럼: 글 번호(id)
            if col == 0:
                return str(post.id)
            # 1 번째 컬럼: 제목
            if col == 1:
                return post.title
            # 2 번째 컬럼: 작성자
            if col == 2:
                return post.author
            # 3 번째 컬럼: 날짜(연, 월, 일)
            if col == 3:
                target_date = post.updated_at or post.created_at
                date_str = str(target_date)
                # 연, 월, 일만 표현하도록 정규식 적용
                match = re.match(r"^(\d{4}-\d{2}-\d{2})", date_str)

                if match:
                    return match.group(1)  # "2025-12-26" 반환
                else:
                    return date_str  # 실패시 원본 반환

        if role == Qt.TextAlignmentRole:
            if index.column() != 1:
                return Qt.AlignCenter

        return None

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """
        헤더(컬럼명) 정보를 반환합니다.
        """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return None
