import sys
from PySide6.QtWidgets import (
    QApplication, 
    QLabel, 
    QFileDialog, 
    QPushButton, 
    QVBoxLayout, 
    QWidget
)

from src.core import Flowchart

class MainWindow(QApplication):
    def __init__(self):
        super().__init__(sys.argv)

        # Se crea el box principal que almacena todo
        window = QWidget()
        window.setWindowTitle("QuetzalFlowchart")
        window.setGeometry(100, 100, 400, 200)
        layout = QVBoxLayout()
        window.setLayout(layout)
        window.show()
        label = QLabel("Hola, QuetzalFlowchart!")
        button = QPushButton("Seleccionar archivo de diagrama de flujo")
        button.clicked.connect(self.open_file_dialog)
        layout.addWidget(label)
        layout.addWidget(button)
        sys.exit(self.exec())

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            None,
            "Seleccionar archivo de diagrama de flujo",
            "",
            "Archivos JSON (*.json);;Archivos YAML (*.yaml *.yml)"
        )
        if file_path:
            flowchart_dict, file_name = Flowchart.load_flowchart(file_path)
            print(flowchart_dict)


if __name__ == "__main__":
    app = MainWindow()
