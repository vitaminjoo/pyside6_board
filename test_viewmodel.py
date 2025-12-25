import sys

from PySide6.QtCore import QCoreApplication

from app.viewmodels.post_viewmodel import PostViewModel

app = QCoreApplication(sys.argv)

vm = PostViewModel()


def on_post_list_received(data):
    print(f"\n 게시판 글 개수: {len(data)}")
    for post in data:
        print(f" - {post['title']}")


def on_message_received(msg):
    print(f"[View] 알림창 뜸: {msg}")


vm.post_list_updated.connect(on_post_list_received)
vm.message_signal.connect(on_message_received)

print("--- 1. 데이터 불러오기 요청 ---")
vm.fetch_posts()

print("\n--- 2. 새 글 작성 요청 ---")
vm.add_post("뷰모델 테스트", "신호와 슬롯 작동 확인 중")

print("\n--- 테스트 종료 ---")
