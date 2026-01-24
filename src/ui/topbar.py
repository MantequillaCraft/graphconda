from PySide6.QtWidgets import QHBoxLayout, QPushButton, QLabel, QFrame


class TopBar(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(
            "background-color: #252525; border-bottom: 1px solid #2d2d2d;"
        )
        self.setFixedHeight(50)
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)

        self.file_label = QLabel("untitled_flowchart.qfc  •")
        self.file_label.setStyleSheet("color: #e0e0e0;")
        layout.addWidget(self.file_label)

        layout.addStretch()

        self.run_btn = QPushButton("Run")
        self.run_btn.setObjectName("runButton")
        layout.addWidget(self.run_btn)

        layout.addSpacing(20)

        self.status_label = QLabel("Idle")
        self.status_label.setStyleSheet("color: #888888;")
        layout.addWidget(self.status_label)
