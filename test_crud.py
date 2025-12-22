from app.database import db
from app.models.post_dao import PostDao

def run_test():

    db.init_db()
    dao = PostDao()
    print("====== TEST ======")

    # [Create] 글 생성
    print("\n1. 글 추가 실행")
    dao.insert_post("Git Test", "This is Testing.")
    dao.insert_post("Git Test", "This is Testing.", "MVVM Master")

    # [Read] 글 조회
    print("\n2. 글 조회 실행")
    posts = dao.get_all_posts()
    for post in posts:
        print(f" -> ID {post['id']} | 제목: {post['title']} | 내용: {post['content']}")

    if posts:
        target_id = posts[0]['id']

        # [Update] 글 수정
        print("\n3. 글 수정 실행")
        dao.update_post(target_id, "Updated Title", "Updated Content")

        # 수정 글 확인
        updated_post = dao.get_post(target_id)
        print(updated_post['title'], updated_post['content'], updated_post['updated_at'])

        # [Delete] 글 삭제
        print("\n4. 글 삭제 실행")
        dao.delete_post(target_id)

        final_list = dao.get_all_posts()
        print(f" -> 삭제 후 남은 글 개수: {len(final_list)}")

    print("\n 테스트 종료 ")

if __name__ == '__main__':
    run_test()