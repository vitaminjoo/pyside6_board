from PySide6.QtCore import QObject, Signal
from app.models.post_dao import PostDao

class PostViewModel(QObject):
    """
    View와 Model 사이의 중계자
    화면 로직(상태 관리)가 여기서 수행됩니다.
    """

    post_list_updated = Signal(list)
    message_signal = Signal(str)

    def __init__(self):
        super().__init__()
        self.post_dao = PostDao()

    def fetch_posts(self):
        # DB에서 글 목록을 가져온 뒤, View 에게 알림
        data = self.post_dao.get_all_posts()
        self.post_list_updated.emit(data)

    def add_post(self, title, content, author=""):
        if not title or not content:
            self.message_signal.emit("제목과 내용을 모두 입력해주세요")
            return

        self.post_dao.insert_post(title, content, author)
        self.message_signal.emit("게시글이 성공적으로 등록되었습니다.")

        self.fetch_posts()

    def update_post(self, post_id, title, content):
        self.post_dao.update_post(post_id, title, content)
        self.message_signal.emit("게시글이 수정되었습니다.")
        self.fetch_posts()

    def delete_post(self, post_id):
        self.post_dao.delete_post(post_id)
        self.message_signal.emit("게시글이 삭제되었습니다.")
        self.fetch_posts()

