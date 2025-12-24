from typing import Optional

from app.database import db
from app.models import Post


class PostDao:
    """
    게시글(Posts)과 관련한 DB 작업을 전담하는 클래스입니다.
    SQL 쿼리는 이 파일 안에만 존재해야 합니다.
    """

    def insert_post(self, post: Post) -> None:
        new_post = post
        with db.get_cursor() as cursor:
            sql = "INSERT INTO posts (title, content, author) VALUES (?, ?, ?)"
            cursor.execute(sql, (new_post.title, new_post.content, new_post.author))

    def get_all_posts(self) -> list[Post]:
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

    def get_post(self, id: int) -> Optional[Post]:
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

    def update_post(self, updated_post: Post) -> None:
        post = updated_post
        with db.get_cursor() as cursor:
            sql = "UPDATE posts SET title=?, content =?, author=?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
            cursor.execute(sql, (post.title, post.content, post.author, post.id))

    def delete_post(self, id: int) -> None:
        with db.get_cursor() as cursor:
            sql = "DELETE FROM posts WHERE id = ?"
            cursor.execute(sql, (id,))

    def delete_posts(self, ids: list[int]) -> int:
        if not ids:
            return 0
        count = 0
        with db.get_cursor() as cursor:
            placeholders = ', '.join(['?'] * len(ids))
            sql = "DELETE FROM posts WHERE id IN ({})".format(placeholders)
            cursor.execute(sql, ids)
            count = cursor.rowcount
        return count

    def get_posts_paginated(self, page: int, limit: int) -> list[Post]:
        offset = (page - 1) * limit
        with db.get_cursor() as cursor:
            sql = "SELECT * FROM posts ORDER BY created_at DESC LIMIT ? OFFSET ?"
            cursor.execute(sql, (limit, offset))
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

    def get_total_count(self) -> int:
        with db.get_cursor() as cursor:
            sql = "SELECT COUNT(*) FROM posts"
            cursor.execute(sql)
            count = cursor.fetchone()[0]
            return count if count else 0

    def search_post(self, keyword: str):
        with db.get_cursor() as cursor:
            sql = "SELECT * FROM posts WHERE title LIKE ? OR content LIKE ?"
            cursor.execute(sql, ('%' + keyword + '%', '%' + keyword + '%'))
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

    def get_search_count(self, keyword: str) -> int:
        with db.get_cursor() as cursor:
            sql = "SELECT COUNT(*) FROM posts WHERE title LIKE ? OR content LIKE ?"
            param = f"%{keyword}%"
            cursor.execute(sql, (param, param))
            result = cursor.fetchone()
            return result[0] if result else 0

    def get_search_posts_paginated(self, keyword: str, page: int, limit: int) -> list[Post]:
        offset = (page - 1) * limit
        with db.get_cursor() as cursor:
            sql = """
                  SELECT *
                  FROM posts
                  WHERE title LIKE ?
                     OR content LIKE ?
                  ORDER BY created_at DESC LIMIT ?
                  OFFSET ? \
                  """
            param = f"%{keyword}%"
            cursor.execute(sql, (param, param, limit, offset))
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
