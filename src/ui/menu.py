from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtGui import QAction

from src.ui.styles import STYLES
from src.ui.leftpanel import LeftPanel
from src.ui.rightpanel import RightPanel
from src.ui.topbar import TopBar
from src.ui.canvas import Canvas


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QuetzalFlowchart")
        self.setGeometry(100, 100, 1400, 900)
        self.create_menus()
        self.setStyleSheet(STYLES)
        self.setup_ui()

    def create_menus(self):
        menubar = self.menuBar()

        # Menú File
        file_menu = menubar.addMenu("File")

        new_action = QAction("Nuevo", self)
        new_action.triggered.connect(lambda: self.text_edit.clear())
        file_menu.addAction(new_action)

        exit_action = QAction("Salir", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Menú View
        view_menu = menubar.addMenu("View")

        zoom_in = QAction("Acercar", self)
        zoom_in.triggered.connect(lambda: self.text_edit.zoomIn())
        view_menu.addAction(zoom_in)

        zoom_out = QAction("Alejar", self)
        zoom_out.triggered.connect(lambda: self.text_edit.zoomOut())
        view_menu.addAction(zoom_out)

        # Menú Help
        help_menu = menubar.addMenu("Help")

        about_action = QAction("Acerca de", self)
        about_action.triggered.connect(
            lambda: self.text_edit.append("\n--- App Simple PySide6 ---")
        )
        help_menu.addAction(about_action)

    def setup_ui(self):
        # Widget central
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Panel izquierdo
        self.left_panel = LeftPanel()
        main_layout.addWidget(self.left_panel)

        # Área central
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(0)

        self.top_bar = TopBar()
        center_layout.addWidget(self.top_bar)

        self.canvas = Canvas()
        center_layout.addWidget(self.canvas)

        main_layout.addWidget(center_widget, stretch=1)

        # Panel derecho
        self.right_panel = RightPanel()
        main_layout.addWidget(self.right_panel)

        # Conectar eventos (ejemplo)
        self.connect_signals()

    def connect_signals(self):
        # Aquí puedes conectar tus señales
        self.left_panel.btn_open.clicked.connect(self.on_open)
        self.left_panel.btn_save.clicked.connect(self.on_save)
        self.left_panel.btn_run.clicked.connect(self.on_run)

    def on_open(self):
        print("Open clicked")

    def on_save(self):
        print("Save clicked")

    def on_run(self):
        print("Run clicked")
