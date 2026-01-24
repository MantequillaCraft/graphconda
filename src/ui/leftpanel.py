from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLabel, QListWidget, QFrame


class LeftPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("leftPanel")
        self.setFixedWidth(200)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Header
        header = QLabel("QuetzalFlowchart")
        header.setObjectName("header")
        layout.addWidget(header)

        subtitle = QLabel("Visual Execution Engine")
        subtitle.setStyleSheet("color: #888888; font-size: 11px; background-color: transparent;")
        layout.addWidget(subtitle)

        layout.addSpacing(20)

        # Botones principales
        self.btn_open = QPushButton("Open Flowchart")
        layout.addWidget(self.btn_open)

        self.btn_save = QPushButton("Save")
        layout.addWidget(self.btn_save)

        self.btn_run = QPushButton("Run")
        self.btn_run.setObjectName("runButton")
        layout.addWidget(self.btn_run)

        self.btn_visual = QPushButton("Visual Mode")
        layout.addWidget(self.btn_visual)

        layout.addSpacing(20)

        # Recent files
        recent_label = QLabel("RECENT FILES")
        recent_label.setStyleSheet(
            "color: #666666; font-size: 10px; font-weight: bold;"
        )
        layout.addWidget(recent_label)

        self.recent_list = QListWidget()
        self.recent_list.addItem("sorting_algorithm.qfc")
        self.recent_list.addItem("user_login.qfc")
        self.recent_list.addItem("calculator.qfc")
        layout.addWidget(self.recent_list)

        layout.addStretch()

        # Footer
        footer = QLabel("v1.0.0          Python 3.11")
        footer.setStyleSheet("color: #666666; font-size: 10px;")
        layout.addWidget(footer)
