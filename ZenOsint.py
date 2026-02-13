import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFrame, QGridLayout)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QPixmap

class ZenOsint(QWidget):
    def __init__(self):
        super().__init__()

        self.dir_base = os.path.dirname(os.path.abspath(__file__))
        self.icon_path = os.path.join(self.dir_base, "Iconos")
        self.func_path = os.path.join(self.dir_base, "Funciones")
        
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Zen OSINT Suite")
        self.setFixedSize(940, 620)
        

        self.setStyleSheet("""
            QWidget { 
                background-color: #080808; 
                color: #d1d1d1; 
                font-family: 'Segoe UI', Tahoma, sans-serif; 
            }
            QPushButton#nav-action {
                background-color: #121212;
                border: 1px solid #222;
                border-radius: 8px;
                padding: 8px 15px;
                font-weight: 600;
                color: #efefef;
            }
            QPushButton#nav-action:hover {
                background-color: #1a1a1a;
                border-color: #3d5afe;
                color: #3d5afe;
            }
            QFrame#container {
                background-color: #0c0c0c;
                border: 1px solid #181818;
                border-radius: 12px;
            }
            QLabel#tool-item {
                color: #777;
                font-size: 13px;
                padding: 4px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 40)


        nav = QHBoxLayout()
        
        logo = QLabel()
        logo.setPixmap(QPixmap(os.path.join(self.icon_path, "Logo.png")).scaled(32, 32, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        
        title = QLabel("ZEN OSINT")
        title.setStyleSheet("font-size: 16px; font-weight: 800; letter-spacing: 1.5px; color: #fff;")
        
        nav.addWidget(logo)
        nav.addWidget(title)
        nav.addStretch()


        self.btn_info = QPushButton(" INFO")
        self.btn_info.setObjectName("nav-action")
        self.btn_info.setIcon(QIcon(os.path.join(self.icon_path, "Info.png")))
        self.btn_info.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_info.clicked.connect(lambda: self.run_module("Info.py"))

        self.btn_tools = QPushButton(" HERRAMIENTAS")
        self.btn_tools.setObjectName("nav-action")
        self.btn_tools.setIcon(QIcon(os.path.join(self.icon_path, "Herramientas.png")))
        self.btn_tools.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_tools.clicked.connect(lambda: self.run_module("Herramientas.py"))

        nav.addWidget(self.btn_info)
        nav.addSpacing(10)
        nav.addWidget(self.btn_tools)
        layout.addLayout(nav)

        layout.addSpacing(40)


        hero = QVBoxLayout()
        welcome_txt = QLabel("Bienvenido a Zen Osint")
        welcome_txt.setStyleSheet("font-size: 32px; font-weight: 700; color: #fff;")
        hero.addWidget(welcome_txt, alignment=Qt.AlignmentFlag.AlignCenter)
        
        desc_txt = QLabel("Motor de búsqueda y análisis de inteligencia de fuentes abiertas")
        desc_txt.setStyleSheet("color: #555; font-size: 14px; margin-bottom: 20px;")
        hero.addWidget(desc_txt, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addLayout(hero)


        grid_frame = QFrame()
        grid_frame.setObjectName("container")
        grid = QGridLayout(grid_frame)
        grid.setContentsMargins(25, 25, 25, 25)
        grid.setSpacing(10)

        herramientas_lista = [
            "Buscar por IP", "Número de teléfono", "Email footprint", 
            "Buscar usuario", "Información Web", "Escaneo de puertos",
            "Test de WiFi", "Tu dirección IP", "Status Servidor",
            "YouTube Downloader", "Base de Datos", "Discord Token",
            "ID de Roblox", "Usuario Roblox", "Server Discord",
            "Vulnerabilidad SQL", "Generador QR", "Webhook Spammer", "Links",
            "Y mas..."
        ]


        for i, h in enumerate(herramientas_lista):
            item = QLabel(f"• {h}")
            item.setObjectName("tool-item")
            grid.addWidget(item, i // 4, i % 4) 

        layout.addWidget(grid_frame)

    def run_module(self, filename):
        target = os.path.join(self.func_path, filename)
        if os.path.exists(target):

            subprocess.Popen([sys.executable, target])
        else:
            print(f"Error: No se encuentra el archivo en {target}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = ZenOsint()
    window.show()
    sys.exit(app.exec())
