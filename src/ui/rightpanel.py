from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTextEdit,
    QFrame,
    QLineEdit,
)


class RightPanel(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName("rightPanel")
        self.setFixedWidth(300)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(12)

        # Inspector header
        inspector_label = QLabel("Inspector")
        inspector_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(inspector_label)

        # Canvas Controls
        controls_label = QLabel("Canvas Controls")
        controls_label.setStyleSheet(
            "color: #2d8659; font-weight: bold; margin-top: 10px;"
        )
        layout.addWidget(controls_label)

        instructions = QLabel(
            "• Click nodes to view properties\n• Press Run to execute flowchart\n• Drag to pan, scroll to zoom"
        )
        instructions.setStyleSheet("color: #888888; font-size: 11px;")
        layout.addWidget(instructions)

        # Description
        desc_label = QLabel("DESCRIPTION")
        desc_label.setStyleSheet(
            "color: #666666; font-size: 10px; font-weight: bold; margin-top: 20px;"
        )
        layout.addWidget(desc_label)

        self.desc_text = QTextEdit()
        self.desc_text.setPlaceholderText("Entry point of the flowchart")
        self.desc_text.setMaximumHeight(100)
        layout.addWidget(self.desc_text)

        # Node ID
        node_label = QLabel("NODE ID")
        node_label.setStyleSheet(
            "color: #666666; font-size: 10px; font-weight: bold; margin-top: 10px;"
        )
        layout.addWidget(node_label)

        self.node_input = QLineEdit("node1")
        layout.addWidget(self.node_input)

        layout.addStretch()

        # Action buttons
        self.apply_btn = QPushButton("Apply Changes")
        self.apply_btn.setObjectName("runButton")
        layout.addWidget(self.apply_btn)

        self.delete_btn = QPushButton("Delete Node")
        self.delete_btn.setStyleSheet("background-color: #4d3333; color: #ff6b6b;")
        layout.addWidget(self.delete_btn)

        self.help_btn = QPushButton("?")
        self.help_btn.setFixedSize(30, 30)
        self.help_btn.setStyleSheet("border-radius: 15px; background-color: #2d2d2d;")
        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.help_btn)
        layout.addLayout(bottom_layout)
