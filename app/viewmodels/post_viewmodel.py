from typing import Optional

from PySide6.QtCore import QObject, Signal

from app.models.post_dao import PostDao
from app.models.post_model import Post


class PostViewModel(QObject):
    """
    View와 Model 사이의 중계자
    화면 로직(상태 관리)가 여기서 수행됩니다.
    """
    post_list_updated = Signal(list)
    error_message_signal = Signal(str)
    message_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.post_dao = PostDao()

    def fetch_posts(self) -> None:
        # DB에서 글 목록을 가져온 뒤, View 에게 알림
        data = self.post_dao.get_all_posts()
        self.post_list_updated.emit(data)

    def get_post(self, id: int) -> Optional[Post]:
        data = self.post_dao.get_post(id)
        return data

    def add_post(self, title: str, content: str, author: str = None) -> bool:
        try:
            self.post_dao.insert_post(title, content, author)
            self.message_signal.emit("Post Added.")
            self.fetch_posts()
            return True
        except Exception as e:
            self.error_message_signal.emit(e)
            return False

    def update_post(self, id: int, title: str, content: str, author: str = None) -> bool:
        try:
            self.post_dao.update_post(id, title, content, author)
            self.message_signal.emit("Post Updated.")
            self.fetch_posts()
            return True
        except Exception as e:
            self.error_message_signal.emit(e)
            return False

    def delete_post(self, id: int) -> bool:
        try:
            self.post_dao.delete_post(id)
            self.fetch_posts()
            return True
        except Exception as e:
            self.error_message_signal.emit(e)
            return False

    def delete_posts(self, ids : list[int]) -> bool:
        try:
            self.post_dao.delete_posts(ids)
            self.fetch_posts()
            self.message_signal.emit(f"Posts Deleted. : {len(ids)} ")
            return True
        except Exception as e:
            self.error_message_signal.emit(e)
            return False