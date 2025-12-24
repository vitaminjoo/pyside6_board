from PySide6.QtCore import QAbstractTableModel, Qt, QModelIndex

class PostTableModel(QAbstractTableModel):
    def __init__(self, posts=None):
        super().__init__()
        self.posts = posts or []
        self._headers = ["No.", "Subject", "Author", "Date"]

    def rowCount(self, parent=QModelIndex()):
        return len(self.posts)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index, role: Qt.DisplayRole):
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
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return None



