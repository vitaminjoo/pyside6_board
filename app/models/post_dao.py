from app.database import db
from app.models.post_model import Post


class PostDao:
    """
    게시글(Posts)과 관련한 DB 작업을 전담하는 클래스입니다.
    SQL 쿼리는 이 파일 안에만 존재해야 합니다.
    """

    def insert_post(self, title, content, author="anonymous"):
        conn = db.get_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO posts (title, content, author) VALUES (?, ?, ?)"
        cursor.execute(sql, (title, content, author))

        conn.commit()
        conn.close()
        print(f"글 작성 완료: {title}")

    def get_all_posts(self):
        conn = db.get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM posts ORDER BY created_at DESC"
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()

        posts_obj = []
        for row in rows:
            post = Post(id=row['id'],
            title=row['title'],
            content=row['content'],
            author=row['author'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
            )
            posts_obj.append(post)
        return posts_obj

    def get_post(self, id):
        conn = db.get_connection()
        cursor = conn.cursor()

        sql = "SELECT * FROM posts WHERE id = ?"
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        conn.close()
        return row

    def update_post(self, id, title, content):
        conn = db.get_connection()
        cursor = conn.cursor()

        sql = "UPDATE posts SET title=?, content=?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        cursor.execute(sql, (title, content, id))
        conn.commit()
        conn.close()
        print(f"수정 완료: ID: {id}")

    def delete_post(self, id):
        conn = db.get_connection()
        cursor = conn.cursor()

        sql = "DELETE FROM posts WHERE id = ?"
        cursor.execute(sql, (id,))
        conn.commit()
        conn.close()
        print(f"삭제 완료: id: {id}")

