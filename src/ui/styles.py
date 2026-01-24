STYLES = """
    QMainWindow, QWidget {
        background-color: #1e1e1e;
        color: #e0e0e0;
    }
    QLabel {
        background-color: transparent;
    }
    QPushButton {
        background-color: #2d2d2d;
        border: 1px solid #3d3d3d;
        border-radius: 4px;
        padding: 8px 16px;
        color: #e0e0e0;
    }
    QPushButton:hover {
        background-color: #3d3d3d;
    }
    QPushButton#runButton {
        background-color: #2d8659;
        color: #ffffff;
        font-weight: bold;
    }
    QPushButton#runButton:hover {
        background-color: #3a9d6d;
    }
    QListWidget {
        background-color: #252525;
        border: none;
        padding: 4px;
    }
    QListWidget::item {
        padding: 8px;
        border-radius: 4px;
    }
    QListWidget::item:hover {
        background-color: #2d2d2d;
    }
    QFrame#leftPanel, QFrame#rightPanel {
        background-color: #1a1a1a;
        border-right: 1px solid #2d2d2d;
    }
    QFrame#canvas {
        background-color: #1e1e1e;
        border: none;
    }
    QLineEdit, QTextEdit {
        background-color: #2d2d2d;
        border: 1px solid #3d3d3d;
        border-radius: 4px;
        padding: 6px;
        color: #e0e0e0;
    }
    QLabel#header {
        font-size: 18px;
        font-weight: bold;
        color: #2d8659;
    }
"""
