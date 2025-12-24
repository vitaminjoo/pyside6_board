import math
from typing import Optional

from PySide6.QtCore import QObject, Signal

from app.database import PostDao
from app.models import Post


class PostViewModel(QObject):
    """
    View와 Model 사이의 중계자
    화면 로직(상태 관리)가 여기서 수행됩니다.
    """
    post_list_updated = Signal(list)
    paging_info_updated = Signal(int, int)
    error_message_signal = Signal(str)
    message_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.post_dao = PostDao()
        self.current_page = 1
        self.items_per_page = 16
        self.total_count = 0
        self.total_pages = 1

        self.current_keyword = ""

    def fetch_posts(self) -> None:
        try:
            # 검색한 결과 fetch
            if self.current_keyword:
                self.total_count = self.post_dao.get_search_count(self.current_keyword)
                posts = self.post_dao.get_search_posts_paginated(
                    self.current_keyword, self.current_page, self.items_per_page
                )
            # 전체 리스트 fetch
            else:
                self.total_count = self.post_dao.get_total_count()
                posts = self.post_dao.get_posts_paginated(
                    self.current_page, self.items_per_page
                )

            if self.total_count == 0:
                self.total_pages = 1
            else:
                self.total_pages = math.ceil(self.total_count / self.items_per_page)

            self.post_list_updated.emit(posts)
            self.paging_info_updated.emit(self.current_page, self.total_pages)

        except Exception as e:
            self.error_message_signal.emit(f"Data Load Failed: {e}")

    def go_prev_page(self, step: int = 1):
        print(step)
        if self.current_page > 1:
            if self.current_page - step < 0:
                self.current_page = 1
            else:
                self.current_page -= step
            self.fetch_posts()

    def go_next_page(self, step: int = 1):
        if self.current_page < self.total_pages:
            if self.current_page + step > self.total_pages:
                self.current_page = self.total_pages
            else:
                self.current_page += step
            self.fetch_posts()

    def go_to_page(self, page: int):
        if 1 <= page <= self.total_pages:
            self.current_page = page
            self.fetch_posts()

    def get_post(self, id: int) -> Optional[Post]:
        data = self.post_dao.get_post(id)
        return data

    def add_post(self, title: str, content: str, author: str = None) -> bool:
        try:
            author = author if author else "anonymous"
            post = Post(title=title, content=content, author=author)
            self.post_dao.insert_post(post)
            self.message_signal.emit("Post Added.")
            self.fetch_posts()
            return True
        except Exception as e:
            self.error_message_signal.emit(e)
            return False

    def update_post(self, id: int, title: str, content: str, author: str = None) -> bool:
        try:
            author = author if author else "anonymous"
            updated_post = Post(id=id, title=title, content=content, author=author)
            self.post_dao.update_post(updated_post)
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

    def delete_posts(self, ids: list[int]) -> bool:
        try:
            self.post_dao.delete_posts(ids)
            self.fetch_posts()
            self.message_signal.emit(f"Posts Deleted. : {len(ids)} ")
            return True
        except Exception as e:
            self.error_message_signal.emit(e)
            return False

    def search_posts(self, keyword: str) -> list[Post] | None:
        try:
            self.current_keyword = keyword.strip()
            self.current_page = 1
            self.fetch_posts()
        except Exception as e:
            self.error_message_signal.emit(e)
            return []
