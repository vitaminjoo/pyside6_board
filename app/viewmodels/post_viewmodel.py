import math
from typing import Optional

from PySide6.QtCore import QObject, Signal

from app.database import PostDao
from app.models import Post


class PostViewModel(QObject):
    """
    View와 Model 사이의 중계자 역할을 하는 ViewModel 클래스입니다.
    화면 로직(상태 관리)과 데이터 처리 요청이 여기서 수행됩니다.
    """
    # 게시글 목록이 업데이트되었을 때 발생하는 시그널 (게시글 리스트 전달)
    post_list_updated = Signal(list)
    # 페이징 정보가 업데이트되었을 때 발생하는 시그널 (현재 페이지, 전체 페이지 수 전달)
    paging_info_updated = Signal(int, int)
    # 에러 메시지가 발생했을 때 전달하는 시그널
    error_message_signal = Signal(str)
    # 일반 알림 메시지를 전달하는 시그널
    message_signal = Signal(str)

    def __init__(self):
        """
        ViewModel 초기화 메서드입니다.
        DAO 인스턴스 생성 및 페이징 관련 변수를 초기화합니다.
        """
        super().__init__()
        self.post_dao = PostDao()
        self.current_page = 1
        self.items_per_page = 16
        self.total_count = 0
        self.total_pages = 1

        self.current_keyword = ""

    def fetch_posts(self) -> None:
        """
        현재 페이지와 검색어(있는 경우)에 맞춰 게시글 목록을 불러옵니다.
        데이터 로드 후 post_list_updated 및 paging_info_updated 시그널을 방출합니다.
        """
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
        """
        이전 페이지로 이동합니다.

        Args:
            step (int): 이동할 페이지 수 (기본값 1)
        """
        print(step)
        if self.current_page > 1:
            if self.current_page - step < 0:
                self.current_page = 1
            else:
                self.current_page -= step
            self.fetch_posts()

    def go_next_page(self, step: int = 1):
        """
        다음 페이지로 이동합니다.

        Args:
            step (int): 이동할 페이지 수 (기본값 1)
        """
        if self.current_page < self.total_pages:
            if self.current_page + step > self.total_pages:
                self.current_page = self.total_pages
            else:
                self.current_page += step
            self.fetch_posts()

    def go_to_page(self, page: int):
        """
        특정 페이지로 바로 이동합니다.

        Args:
            page (int): 이동할 페이지 번호
        """
        if 1 <= page <= self.total_pages:
            self.current_page = page
            self.fetch_posts()

    def get_post(self, id: int) -> Optional[Post]:
        """
        특정 ID의 게시글 상세 정보를 가져옵니다.

        Args:
            id (int): 게시글 ID

        Returns:
            Optional[Post]: 게시글 객체 또는 None
        """
        data = self.post_dao.get_post(id)
        return data

    def add_post(self, title: str, content: str, author: str = None) -> bool:
        """
        새로운 게시글을 추가합니다.

        Args:
            title (str): 제목
            content (str): 내용
            author (str, optional): 작성자 (기본값 "anonymous")

        Returns:
            bool: 성공 시 True, 실패 시 False
        """
        try:
            author = author if author else "anonymous"
            post = Post(title=title, content=content, author=author)
            self.post_dao.insert_post(post)
            self.message_signal.emit("Post Added.")
            self.fetch_posts()
            return True
        except Exception as e:
            self.error_message_signal.emit(str(e))
            return False

    def update_post(self, id: int, title: str, content: str, author: str = None) -> bool:
        """
        기존 게시글을 수정합니다.

        Args:
            id (int): 수정할 게시글 ID
            title (str): 제목
            content (str): 내용
            author (str, optional): 작성자

        Returns:
            bool: 성공 시 True, 실패 시 False
        """
        try:
            author = author if author else "anonymous"
            updated_post = Post(id=id, title=title, content=content, author=author)
            self.post_dao.update_post(updated_post)
            self.message_signal.emit("Post Updated.")
            self.fetch_posts()
            return True
        except Exception as e:
            self.error_message_signal.emit(str(e))
            return False

    def delete_post(self, id: int) -> bool:
        """
        게시글을 삭제합니다.

        Args:
            id (int): 삭제할 게시글 ID

        Returns:
            bool: 성공 시 True, 실패 시 False
        """
        try:
            self.post_dao.delete_post(id)
            self.fetch_posts()
            return True
        except Exception as e:
            self.error_message_signal.emit(str(e))
            return False

    def delete_posts(self, ids: list[int]) -> bool:
        """
        여러 게시글을 일괄 삭제합니다.

        Args:
            ids (list[int]): 삭제할 게시글 ID 리스트

        Returns:
            bool: 성공 시 True, 실패 시 False
        """
        try:
            self.post_dao.delete_posts(ids)
            self.fetch_posts()
            self.message_signal.emit(f"Posts Deleted. : {len(ids)} ")
            return True
        except Exception as e:
            self.error_message_signal.emit(str(e))
            return False

    def search_posts(self, keyword: str) -> list[Post] | None:
        """
        키워드로 게시글을 검색합니다. 검색 후 첫 페이지로 이동합니다.

        Args:
            keyword (str): 검색어

        Returns:
            list[Post] | None: 검색 결과 리스트 (실제 반환값은 fetch_posts를 통해 시그널로 전달됨)
        """
        try:
            self.current_keyword = keyword.strip()
            self.current_page = 1
            self.fetch_posts()
        except Exception as e:
            self.error_message_signal.emit(str(e))
            return []
