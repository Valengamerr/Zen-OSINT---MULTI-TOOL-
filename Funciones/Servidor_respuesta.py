import sys
import requests
import time
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton, QFrame
from PyQt6.QtCore import Qt

class ProbadorServidor(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(500, 400)
        self.setWindowTitle("Zen OSINT - Respuesta de servidor")
        self.armar_pantalla()

    def armar_pantalla(self):
        self.setStyleSheet("""
            QWidget { background-color: #030305; color: #ffffff; font-family: 'Consolas'; }
            
            QLineEdit { 
                background: #0d0d15; border: 2px solid #0055ff; 
                border-radius: 5px; padding: 15px; color: #00d4ff; font-size: 14px;
            }
            QLineEdit:focus { border: 2px solid #00ffcc; }

            #CajaInfo {
                background: #101020; border: 1px solid #1a1a30; 
                border-radius: 8px; padding: 20px;
            }

            #Resultado { 
                font-size: 32px; font-weight: bold; color: #00ffcc; 
            }

            QPushButton { 
                background: #0055ff; color: #ffffff; border: none; 
                padding: 15px; font-weight: bold; border-radius: 5px;
            }
            QPushButton:hover { background: #0033aa; }
        """)

        capa_total = QVBoxLayout(self)

        self.url_texto = QLineEdit()
        self.url_texto.setPlaceholderText("PEGA EL LINK PARA MEDIR (ej: google.com)")
        
        self.cuadro = QFrame()
        self.cuadro.setObjectName("CajaInfo")
        capa_cuadro = QVBoxLayout(self.cuadro)

        self.etiqueta_ms = QLabel("0 ms")
        self.etiqueta_ms.setObjectName("Resultado")
        self.etiqueta_ms.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.etiqueta_estado = QLabel("ESPERANDO...")
        self.etiqueta_estado.setAlignment(Qt.AlignmentFlag.AlignCenter)

        capa_cuadro.addWidget(self.etiqueta_ms)
        capa_cuadro.addWidget(self.etiqueta_estado)

        boton_medir = QPushButton("MEDIR VELOCIDAD")
        boton_medir.clicked.connect(self.medir)

        capa_total.addWidget(QLabel("Zen OSINT creado por t.me/Valen_Qq"))
        capa_total.addWidget(self.url_texto)
        capa_total.addWidget(self.cuadro)
        capa_total.addWidget(boton_medir)

    def medir(self):
        objetivo = self.url_texto.text().strip()
        if not objetivo: return
        
        if not objetivo.startswith("http"):
            objetivo = "https://" + objetivo

        try:
            inicio = time.time()
            pedido = requests.get(objetivo, timeout=10)
            fin = time.time()
            
            latencia = round((fin - inicio) * 1000)
            self.etiqueta_ms.setText(f"{latencia} ms")

            if latencia < 200:
                self.etiqueta_ms.setStyleSheet("color: #00ff00;")
                self.etiqueta_estado.setText("CONEXIÓN EXCELENTE")
            elif latencia < 600:
                self.etiqueta_ms.setStyleSheet("color: #ffff00;")
                self.etiqueta_estado.setText("CONEXIÓN LENTA")
            else:
                self.etiqueta_ms.setStyleSheet("color: #ffaa00;")
                self.etiqueta_estado.setText("MUY LENTO / LAG")

        except:
            self.etiqueta_ms.setText("---")
            self.etiqueta_ms.setStyleSheet("color: #ff3333;")
            self.etiqueta_estado.setText("SERVIDOR CAIDO O ERROR")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = ProbadorServidor()
    ventana.show()
    sys.exit(app.exec())
