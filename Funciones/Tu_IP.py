import sys
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt

class VisorIP(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(450, 300)
        self.setWindowTitle("Zen OSINT - Ver TU IP Publica")
        self.dibujar()

    def dibujar(self):
        self.setStyleSheet("""
            QWidget { 
                background-color: #050508; 
                color: #e0e0e0; 
                font-family: 'Consolas'; 
            }
            #MarcoPrincipal {
                border: 2px solid #00d4ff;
                border-radius: 10px;
                background-color: #0a0a12;
            }
            QLabel { 
                font-size: 18px; 
                font-weight: bold;
                color: #00d4ff; 
            }
            #Resultado {
                font-size: 24px;
                color: #ffffff;
                background: #111122;
                border-radius: 5px;
                padding: 10px;
                border: 1px solid #333;
            }
            QPushButton { 
                background: #00d4ff; 
                color: #000000; 
                border: none; 
                padding: 15px; 
                font-weight: bold; 
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover { 
                background: #0099bb; 
            }
        """)

        layout = QVBoxLayout(self)
        
        self.marco = QFrame()
        self.marco.setObjectName("MarcoPrincipal")
        layout_marco = QVBoxLayout(self.marco)

        titulo = QLabel("DIRECCIÓN IP PUBLICA")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.etiqueta_ip = QLabel("CARGANDO...")
        self.etiqueta_ip.setObjectName("Resultado")
        self.etiqueta_ip.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        boton = QPushButton("REFRESCAR CONEXION")
        boton.clicked.connect(self.obtener_ip)
        
        layout_marco.addWidget(titulo)
        layout_marco.addWidget(self.etiqueta_ip)
        layout_marco.addWidget(boton)
        
        layout.addWidget(self.marco)
        
        self.obtener_ip()

    def obtener_ip(self):
        try:

            respuesta = requests.get("https://api.ipify.org?format=json").json()
            ip = respuesta["ip"]
            self.etiqueta_ip.setText(ip)
        except:
            self.etiqueta_ip.setText("SIN CONEXIÓN")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VisorIP()
    ventana.show()
    sys.exit(app.exec())
