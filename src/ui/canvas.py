from PySide6.QtWidgets import QVBoxLayout, QLabel, QFrame
from PySide6.QtCore import Qt

class Canvas(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("canvas")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        placeholder = QLabel("Canvas Area\n(Aquí iría el flowchart)")
        placeholder.setStyleSheet("color: #666666; font-size: 14px;")
        placeholder.setAlignment(Qt.AlignCenter)
        layout.addWidget(placeholder)
