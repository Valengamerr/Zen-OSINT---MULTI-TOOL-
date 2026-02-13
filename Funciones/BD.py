# Base de datos  gratis de REDTIGER integrada
import sys
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QLabel, QPushButton, QTextEdit, 
                             QFrame, QScrollArea)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt, QThread, pyqtSignal

class SearchThread(QThread):

    result_signal = pyqtSignal(str)
    status_signal = pyqtSignal(str)

    def __init__(self, query, db_path):
        super().__init__()
        self.query = query
        self.db_path = db_path

    def run(self):
        files = ["1.txt", "2.txt", "3.txt", "4.txt", "5.txt"]
        found = False
        
        for file_name in files:
            full_path = os.path.join(self.db_path, file_name)
            self.status_signal.emit(f"Escaneando {file_name}...")
            
            if os.path.exists(full_path):
                try:
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            if self.query.lower() in line.lower():
                                formatted_res = f"<b>[ARCHIVO: {file_name}] [LÍNEA: {line_num}]</b><br>{line.strip()}<br><br>"
                                self.result_signal.emit(formatted_res)
                                found = True
                except Exception as e:
                    self.result_signal.emit(f"<span style='color:red;'>Error en {file_name}: {str(e)}</span>")
            else:
                self.result_signal.emit(f"<span style='color:#555;'>Archivo {file_name} no encontrado en la raíz.</span><br>")
        
        if not found:
            self.result_signal.emit("<span style='color:yellow;'>No se encontraron coincidencias en la base de datos.</span>")
        self.status_signal.emit("Búsqueda finalizada.")

class ZenDatabase(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1000, 750)
        self.setWindowTitle("Zen OSINT - Base de datos | 1, 2, 3, 4, 5, .txt|")
        self.db_folder = os.path.join(os.getcwd(), "Base_de_datos")
        self.init_ui()

    def init_ui(self):

        self.setStyleSheet("""
            QWidget { background-color: #040406; color: #e0e0e0; font-family: 'Consolas', 'Monospace'; }
            QLineEdit { 
                background: #0d0d14; border: 2px solid #1a1a25; border-radius: 10px; 
                padding: 15px; color: #A020F0; font-size: 16px; font-weight: bold;
            }
            QPushButton { 
                background: #1a1a25; border: 1px solid #A020F0; border-radius: 10px; 
                padding: 15px; font-weight: bold; color: #fff; text-transform: uppercase;
            }
            QPushButton:hover { background: #A020F0; box-shadow: 0 0 15px #A020F0; }
            QTextEdit { 
                background: #000; border: 1px solid #14141c; border-radius: 10px; 
                padding: 15px; color: #00ff00; font-size: 13px; line-height: 1.5;
            }
            QFrame#Header { border-bottom: 2px solid #A020F0; margin-bottom: 10px; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)


        header_frame = QFrame()
        header_frame.setObjectName("Header")
        h_layout = QVBoxLayout(header_frame)
        
        title = QLabel("Zen OSINT  <span style='color:#A020F0;'>Base de datos</span> 1.0 ")
        title.setFont(QFont("Arial Black", 28))
        h_layout.addWidget(title, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.status_label = QLabel("Estado: Listo para escanear.")
        self.status_label.setStyleSheet("color: #666; font-size: 11px;")
        h_layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        layout.addWidget(header_frame)


        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("BUSCAR ALGO EN LA BASE DE DATOS...")
        self.search_input.returnPressed.connect(self.start_search)
        layout.addWidget(self.search_input)

        self.search_btn = QPushButton("INICIAR ESCANEO DE REGISTROS")
        self.search_btn.clicked.connect(self.start_search)
        layout.addWidget(self.search_btn)


        layout.addWidget(QLabel("RESULTADOS DE INTELIGENCIA:"))
        self.results_area = QTextEdit()
        self.results_area.setReadOnly(True)
        layout.addWidget(self.results_area)

    def start_search(self):
        query = self.search_input.text().strip()
        if not query: return
        
        self.results_area.clear()
        self.search_btn.setEnabled(False)
        self.search_btn.setText("BUSCANDO...")
        

        self.thread = SearchThread(query, self.db_folder)
        self.thread.result_signal.connect(self.update_results)
        self.thread.status_signal.connect(self.update_status)
        self.thread.finished.connect(self.search_finished)
        self.thread.start()

    def update_results(self, text):
        self.results_area.append(text)

    def update_status(self, text):
        self.status_label.setText(f"Estado: {text}")

    def search_finished(self):
        self.search_btn.setEnabled(True)
        self.search_btn.setText("INICIAR ESCANEO DE REGISTROS")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    if not os.path.exists("Base_de_datos"):
        os.makedirs("Base_de_datos")
        for i in range(1, 6):
            with open(f"Base_de_datos/{i}.txt", "w") as f: f.write(f"Ejemplo de datos en archivo {i}")
            
    win = ZenDatabase()
    win.show()
    sys.exit(app.exec())
