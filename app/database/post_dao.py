from typing import Optional

from app.database import db
from app.models import Post


class PostDao:
    """
    게시글(Posts)과 관련한 DB 작업을 전담하는 클래스입니다.
    SQL 쿼리는 이 파일 안에만 존재해야 합니다.
    """

    def insert_post(self, post: Post) -> None:
        """
        새로운 게시글을 데이터베이스에 추가합니다.

        Args:
            post (Post): 추가할 게시글 객체 (title, content, author 정보 포함)
        """
        new_post = post
        with db.get_cursor() as cursor:
            sql = "INSERT INTO posts (title, content, author) VALUES (?, ?, ?)"
            cursor.execute(sql, (new_post.title, new_post.content, new_post.author))

    def get_all_posts(self) -> list[Post]:
        """
        모든 게시글을 작성일 역순(최신순)으로 조회합니다.

        Returns:
            list[Post]: 모든 게시글 객체의 리스트
        """
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
        """
        특정 ID를 가진 게시글을 조회합니다.

        Args:
            id (int): 조회할 게시글의 ID

        Returns:
            Optional[Post]: 해당 ID의 게시글 객체, 없으면 None 반환
        """
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
        """
        기존 게시글의 정보를 업데이트합니다.
        제목, 내용, 작성자를 수정하며, 수정 시간(updated_at)을 현재 시간으로 갱신합니다.

        Args:
            updated_post (Post): 업데이트할 정보가 담긴 게시글 객체 (id 필수)
        """
        post = updated_post
        with db.get_cursor() as cursor:
            sql = "UPDATE posts SET title=?, content =?, author=?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
            cursor.execute(sql, (post.title, post.content, post.author, post.id))

    def delete_post(self, id: int) -> None:
        """
        특정 ID의 게시글을 삭제합니다.

        Args:
            id (int): 삭제할 게시글의 ID
        """
        with db.get_cursor() as cursor:
            sql = "DELETE FROM posts WHERE id = ?"
            cursor.execute(sql, (id,))

    def delete_posts(self, ids: list[int]) -> int:
        """
        여러 개의 게시글을 한 번에 삭제합니다.

        Args:
            ids (list[int]): 삭제할 게시글 ID들의 리스트

        Returns:
            int: 삭제된 게시글의 수
        """
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
        """
        게시글 목록을 페이지네이션하여 조회합니다.

        Args:
            page (int): 조회할 페이지 번호 (1부터 시작)
            limit (int): 한 페이지당 보여줄 게시글 수

        Returns:
            list[Post]: 해당 페이지의 게시글 객체 리스트
        """
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
        """
        전체 게시글의 개수를 조회합니다.

        Returns:
            int: 전체 게시글 수
        """
        with db.get_cursor() as cursor:
            sql = "SELECT COUNT(*) FROM posts"
            cursor.execute(sql)
            count = cursor.fetchone()[0]
            return count if count else 0

    def search_post(self, keyword: str):
        """
        제목이나 내용에 키워드가 포함된 게시글을 검색합니다.

        Args:
            keyword (str): 검색할 키워드

        Returns:
            list[Post]: 검색된 게시글 객체 리스트
        """
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
        """
        검색 조건(제목 또는 내용)에 맞는 게시글의 총 개수를 조회합니다.

        Args:
            keyword (str): 검색할 키워드

        Returns:
            int: 검색된 게시글 수
        """
        with db.get_cursor() as cursor:
            sql = "SELECT COUNT(*) FROM posts WHERE title LIKE ? OR content LIKE ?"
            param = f"%{keyword}%"
            cursor.execute(sql, (param, param))
            result = cursor.fetchone()
            return result[0] if result else 0

    def get_search_posts_paginated(self, keyword: str, page: int, limit: int) -> list[Post]:
        """
        검색된 게시글 목록을 페이지네이션하여 조회합니다.

        Args:
            keyword (str): 검색할 키워드
            page (int): 조회할 페이지 번호
            limit (int): 한 페이지당 보여줄 게시글 수

        Returns:
            list[Post]: 해당 페이지의 검색된 게시글 객체 리스트
        """
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
