import sys
import os
import io
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit,
    QLabel, QTextEdit, QHBoxLayout
)
from selenium_func import SeleniumDebugger


# ---------- Redirect print ----------
class EmittingStream(io.TextIOBase):
    """Redirect print to PyQt QTextEdit"""
    def __init__(self, signal):
        super().__init__()
        self.signal = signal

    def write(self, text):
        if text.strip() != "":
            self.signal.emit(text)

    def flush(self):
        pass


# ---------- Selenium Worker ----------
class ConnectWorker(QThread):
    finished = pyqtSignal(object)
    error = pyqtSignal(str)

    def __init__(self, bot, url):
        super().__init__()
        self.bot = bot
        self.url = url

    def run(self):
        try:
            driver = self.bot.connect_selenium_debug(self.url)
            self.finished.emit(driver)
        except Exception as e:
            self.error.emit(str(e))

def resource_path(relative_path):
    """Get absolute path for PyInstaller"""
    if getattr(sys, 'frozen', False):  # ถ้าเป็น .exe
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ---------- Custom Title Bar ----------
class CustomTitleBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setFixedHeight(50)
        self.setStyleSheet("background-color: transparent; color: #fff;")

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)

        # Logo
        self.logo_label = QLabel()
        pixmap = QPixmap(resource_path("BOTBOSS.png")).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.logo_label.setPixmap(pixmap)
        layout.addWidget(self.logo_label)

        # Title
        self.title = QLabel("BOTBOSS Concert")
        self.title.setStyleSheet("font-weight: bold; margin-left: 10px; color: #fff;")
        layout.addWidget(self.title)

        layout.addStretch()

        # Minimize & Close
        self.btn_min = QPushButton("-")
        self.btn_min.setFixedSize(30, 30)
        self.btn_min.setStyleSheet("background-color: #2e2e3e; border-radius: 5px; color: #fff;")
        self.btn_min.clicked.connect(self.parent.showMinimized)
        layout.addWidget(self.btn_min)

        self.btn_close = QPushButton("x")
        self.btn_close.setFixedSize(30, 30)
        self.btn_close.setStyleSheet("background-color: #e74c3c; border-radius: 5px; color: #fff;")
        self.btn_close.clicked.connect(self.parent.close)
        layout.addWidget(self.btn_close)

        self.setLayout(layout)
        self.old_pos = None

    # Drag window
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.old_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.parent.move(self.parent.pos() + delta)
            self.old_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.old_pos = None


# ---------- Main GUI ----------
class TestGUI(QWidget):
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setGeometry(1380, 80, 500, 900)
        self.setFont(QFont("Inter", 10))

        self.bot = SeleniumDebugger()
        self.driver = None

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0,0,0,0)
        main_layout.setSpacing(0)

        # Custom title bar
        self.title_bar = CustomTitleBar(self)
        main_layout.addWidget(self.title_bar)

        # Content widget
        content = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(15)
        content.setLayout(content_layout)

        # Logo
        self.logo_label = QLabel()
        pixmap = QPixmap(resource_path("BOTBOSS.png")).scaled(500, 500, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.addWidget(self.logo_label)

        # Zone input
        self.zone_input = QLineEdit()
        self.zone_input.setPlaceholderText("Zone (ex: A1)")
        content_layout.addWidget(self.zone_input)

        # Connect button
        self.btn_connect = QPushButton("Connect Chrome")
        self.btn_connect.clicked.connect(self.connect_chrome)
        content_layout.addWidget(self.btn_connect)

        # Status
        self.status = QLabel("Status: Idle")
        self.status.setObjectName("status_label")
        content_layout.addWidget(self.status)

        # Log window
        self.log_window = QTextEdit()
        self.log_window.setReadOnly(True)
        content_layout.addWidget(self.log_window)

        main_layout.addWidget(content)
        self.setLayout(main_layout)

        # Timer
        self.zone_timer = QTimer(self)
        self.zone_timer.setInterval(1000)
        self.zone_timer.timeout.connect(self.check_zone_page)

        # Redirect print
        self.log_signal.connect(self.append_log)
        sys.stdout = EmittingStream(self.log_signal)
        sys.stderr = EmittingStream(self.log_signal)

        # Main stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e2f;
                color: #ffffff;
            }
            QLineEdit {
                background-color: #2e2e3e;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 5px;
                color: #fff;
            }
            QTextEdit {
                background-color: #2e2e3e;
                border: 1px solid #444;
                border-radius: 8px;
                padding: 5px;
                color: #fff;
            }
            QPushButton {
                background-color: #4b6cb7;
                border: none;
                border-radius: 12px;
                padding: 10px;
                color: #fff;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a57a1;
            }
            QLabel#status_label {
                font-weight: bold;
                color: #f39c12;
            }
        """)

    # ---------- Log ----------
    def append_log(self, text):
        self.log_window.append(text)

    # ---------- CONNECT ----------
    def connect_chrome(self):
        print("[GUI] Click connect")
        self.status.setText("Status: Connecting...")
        self.btn_connect.setEnabled(False)

        url_login = "https://booking.thaiticketmajor.com/user/signin.php"
        self.worker = ConnectWorker(self.bot, url_login)
        self.worker.finished.connect(self.on_connected)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_connected(self, driver):
        print("[GUI] Chrome connected")
        self.driver = driver
        self.status.setText("Status: Waiting for zone page...")
        self.zone_timer.start()

    # ---------- ZONE CHECK ----------
    def check_zone_page(self):
        if not self.driver:
            return
        print("[GUI] check_zone_page:", self.driver.current_url)
        if self.bot.is_on_zone_page():
            print("[GUI] Zone page detected")
            self.zone_timer.stop()

            zone = self.zone_input.text().strip()
            if not zone:
                self.status.setText("Status: Zone empty")
                return

            self.status.setText("Status: Bot running...")
            self.bot.select_zone(zone)

    def on_error(self, msg):
        print("[GUI] Error:", msg)
        self.status.setText(f"Error: {msg}")
        self.btn_connect.setEnabled(True)


# ---------- Run ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = TestGUI()
    win.show()
    sys.exit(app.exec())
