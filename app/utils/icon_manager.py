import os
import sys

from PySide6.QtGui import QIcon


class IconManager:
    """
    앱 전체에서 아이콘을 관리하는 정적 클래스입니다.
    """

    # 아이콘 이름과 실제 파일명을 연결하는 매핑 테이블
    ICONS = {
        "delete": "trash.png",
    }

    @staticmethod
    def _get_resource_path(filename):
        """실행 환경(PyInstaller 여부)에 따라 적절한 경로를 반환합니다."""

        # 빌드된 실행파일 환경 (임시 폴더 _MEIPASS에서 실행됨)
        if hasattr(sys, '_MEIPASS'):
            # exe 실행 시: 임시폴더/resources/파일명
            return os.path.join(sys._MEIPASS, "resources", filename)

        # 개발 환경
        current_dir = os.path.dirname(os.path.abspath(__file__))
        root_dir = os.path.dirname(os.path.dirname(current_dir))
        return os.path.join(root_dir, "resources", filename)

    @staticmethod
    def get(name: str) -> QIcon:
        """
        등록된 이름으로 QIcon 객체를 반환합니다.
        사용법: IconManager.get("delete")
        """
        filename = IconManager.ICONS.get(name)

        if not filename:
            return QIcon()  # 빈 아이콘 반환

        full_path = IconManager._get_resource_path(filename)

        # 파일이 실제로 있는지 확인 (디버깅용)
        if not os.path.exists(full_path):
            return QIcon()

        return QIcon(full_path)
