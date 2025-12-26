"""
app/utils/styles.py

애플리케이션 전체의 스타일시트(CSS)를 관리하는 모듈입니다.
공통 스타일을 변수로 분리하여 중복을 제거했습니다.
"""

# --------------------------------------------------------------------------
# 1. 색상 상수 정의 (Color Palette)
# --------------------------------------------------------------------------
COLOR_PRIMARY = "#3498db"          # 메인 파란색
COLOR_PRIMARY_BORDER = "#2980b9"   # 메인 파란색 (진함/테두리)
COLOR_DANGER = "#b5334b"           # 경고/삭제 빨간색
COLOR_SELECTED = "#5f6369"         # 테이블 선택 행 배경색
COLOR_TEXT_BASE = "#2f3640"        # 기본 글자색 (필요 시 사용)

# --------------------------------------------------------------------------
# 2. 공통 스타일 조각 - 중복 제거용
# --------------------------------------------------------------------------

# 전체 폰트 및 기본 설정
_BASE_STYLE = """
    QWidget {
        font-family: 'Malgun Gothic';
        font-size: 14px;
    }
"""

# Post(작성/저장) 버튼 스타일
_BTN_POST_STYLE = f"""
    QPushButton#btn_post {{
        min-width: 60px;        
        padding: 4px 8px;     
        background-color: {COLOR_PRIMARY};
        color: white;
        font-weight: bold;      
        font-size: 14px;       
        border-radius: 5px;  
        border: 1px solid {COLOR_PRIMARY_BORDER};
    }}
    QPushButton#btn_post:hover {{
        background-color: {COLOR_PRIMARY_BORDER};
    }}
"""

# 입력창(LineEdit, TextEdit) 기본 패딩
_INPUT_BASE_STYLE = """
    QLineEdit, QTextEdit {
        padding: 10px;
    }
"""

# --------------------------------------------------------------------------
# 3. 화면별 최종 스타일 정의
# --------------------------------------------------------------------------

# [List] 게시글 목록 화면
LIST_STYLE = _BASE_STYLE + _BTN_POST_STYLE + f"""
    QTableView {{
        outline: 0;
    }}
    QTableView::item:focus {{
        border: none;
        outline: none;
    }}
    QTableView::item:selected {{
        background-color: {COLOR_SELECTED};
        color: white;
        border: none;
    }}

    QPushButton#btn_delete {{
        background-color: {COLOR_DANGER};
        border: none;
        border-radius: 4px;
        padding: 2px;
    }}
    
    QPushButton#btn_delete:disabled {{ 
        background-color: {COLOR_SELECTED};
        border: none;
    }}
"""

# [Editor] 게시글 작성/수정 화면
EDITOR_STYLE = _BASE_STYLE + _BTN_POST_STYLE + _INPUT_BASE_STYLE + f"""
    QLineEdit:focus, QTextEdit:focus {{
        border: 1px solid {COLOR_PRIMARY};
    }}
    
    QLabel {{
        font-weight: bold;
    }}
"""

# [Detail] 게시글 상세 화면
DETAIL_STYLE = _BASE_STYLE + _INPUT_BASE_STYLE + f"""
    QLabel#lable_subject {{
        font-size: 20px;
        font-weight: bold;
        margin-bottom: 10px;
    }}

    QPushButton#btn_delete {{
        font-weight: bold;
        background-color: {COLOR_SELECTED};
        padding: 2px;
        border-radius: 4px;
    }}

    QPushButton#btn_delete:hover {{
        background-color: {COLOR_DANGER};
    }}
"""