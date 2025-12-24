from app.database import db
from app.models.post_model import Post


class PostDao:
    """
    게시글(Posts)과 관련한 DB 작업을 전담하는 클래스입니다.
    SQL 쿼리는 이 파일 안에만 존재해야 합니다.
    """

    def insert_post(self, title, content, author):
        if not author:
            author = "anonymous"

        with db.get_cursor() as cursor:
            sql = "INSERT INTO posts (title, content, author) VALUES (?, ?, ?)"
            cursor.execute(sql, (title, content, author))
        print(f"글 작성 완료: {title}")

    def get_all_posts(self):

        with db.get_cursor() as cursor:
            sql = "SELECT * FROM posts ORDER BY created_at DESC"
            cursor.execute(sql)
            rows = cursor.fetchall()

        posts_obj = []
        for row in rows:
            post = Post(
                id=row['id'],
                title=row['title'],
                content=row['content'],
                author=row['author'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
            posts_obj.append(post)
        return posts_obj

    def get_post(self, id):

        with db.get_cursor() as cursor:
            sql = "SELECT * FROM posts WHERE id = ?"
            cursor.execute(sql, (id,))
            row = cursor.fetchone()

        if row:
            return Post(
                id=row['id'],
                title=row['title'],
                content=row['content'],
                author=row['author'],
                created_at=row['created_at'],
                updated_at=row['updated_at']
            )
        else:
            return None

    def update_post(self, id, title, author, content):
        if not author:
            author = "anonymous"

        with db.get_cursor() as cursor:
            sql = "UPDATE posts SET title=?, author =?, content=?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
            cursor.execute(sql, (title, author, content, id))

    def delete_post(self, id):
        with db.get_cursor() as cursor:
            sql = "DELETE FROM posts WHERE id = ?"
            cursor.execute(sql, (id,))
        print(f"삭제 완료: id: {id}")
