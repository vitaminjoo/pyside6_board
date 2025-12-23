import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget

from app.database import db
from app.models.post_model import Post

def init_app():
    conn = db.get_connection()
    Post.create_table(conn)
    conn.close()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    init_app()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())