# DDE Free Board

![Python](https://img.shields.io/badge/Python-3.12.10-3776AB?style=flat-square&logo=python&logoColor=white)
![PySide6](https://img.shields.io/badge/PySide-6.10.1-41CD52?style=flat-square&logo=qt&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=flat-square&logo=sqlite&logoColor=white)

> **PySide6(Qt for Python)로 개발한 MVVM 아키텍처 기반의 데스크톱 게시판 애플리케이션입니다.**
##  주요 기능 (Features)

*   **게시글 관리 (CRUD)**: 게시글 작성, 조회, 수정, 삭제 기능
*   **페이징 (Pagination)**: 게시글 목록 페이지네이션 지원 (이전/다음 블록 이동)
*   **검색 (Search)**: 제목 및 내용을 통한 게시글 검색
*   **데이터 저장**: SQLite를 이용한 로컬 데이터베이스 저장

##  기술 스택 (Tech Stack)

*   **Language**: Python 3.12.10
*   **GUI Framework**: PySide 6.10.1
*   **Database**: SQLite3
*   **Architecture**: MVVM (Model-View-ViewModel)

##  프로젝트 구조 (Project Structure)

```
project_dde/
├── app/
│   ├── database/    # DB 연결 및 DAO (Data Access Object)
│   ├── models/      # 데이터 모델 (Post)
│   ├── utils/       # 유틸 모듈 (Icon Manager, Style 적용)
│   ├── viewmodels/  # 비즈니스 로직 및 뷰 상태 관리
│   └── views/       # UI 화면 (List, Detail, Editor)
├── dist/
│   ├── DDE_Board.exe # 애플리케이션 빌드 파일
├── main.py          # 애플리케이션 진입점
├── README.md        # 프로젝트 설명 문서
├── requirements.txt # 외부 라이브러리 설치를 위한 파일
└── test_data.sql    # 테스트 데이터 생성용 SQL 스크립트
```

##  설치 및 실행 (Setup & Run)

1.  **가상환경 생성 및 활성화 (선택 사항)**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # Mac/Linux
    source venv/bin/activate
    ```

2.  **필수 라이브러리 설치**
    ```bash
    pip install -r requirements.txt
    ```

3.  **애플리케이션 실행**
    ```bash
    python main.py
    ```

4.  **실행 파일 빌드 (선택 사항)**
    ```bash
    pyinstaller DDE_Board.spec
    ```
    빌드된 파일은 `dist/DDE_Board.exe`에 생성됩니다.
