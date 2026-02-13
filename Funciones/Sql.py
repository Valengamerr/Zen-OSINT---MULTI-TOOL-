import sys
import os
import threading
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QLabel, QPushButton, QTextEdit, QComboBox)
from PyQt6.QtCore import Qt

class PantallaPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(900, 650)
        self.setWindowTitle("AUDITORIA")
        self.armar_todo()

    def armar_todo(self):
        self.setStyleSheet("""
            QWidget { background-color: #010103; color: #ffffff; font-family: 'Consolas'; }
            QLineEdit { 
                background: #0a0b10; border: 2px solid #004d40; 
                border-radius: 5px; padding: 12px; color: #00ffaa; font-size: 14px;
            }
            QPushButton { 
                background: #004d40; color: #ffffff; border: none; 
                padding: 15px; font-weight: bold; border-radius: 5px;
            }
            QPushButton:hover { background: #00796b; }
            QTextEdit { 
                background-color: #000000; border: 1px solid #004d40; 
                color: #00ff41; font-size: 12px;
            }
            QComboBox { background: #0a0b10; color: #00ffaa; border: 1px solid #004d40; padding: 8px; }
        """)

        capa = QVBoxLayout(self)
        
        self.barra_url = QLineEdit()
        self.barra_url.setPlaceholderText("PEGA EL LINK ACA...")
        
        fila = QHBoxLayout()
        self.nivel = QComboBox()
        self.nivel.addItems(["1", "2", "3"])
        
        self.boton_ir = QPushButton("ARRANCAR")
        self.boton_ir.clicked.connect(self.comenzar)
        
        fila.addWidget(QLabel("RIESGO:"))
        fila.addWidget(self.nivel)
        fila.addWidget(self.boton_ir)

        self.pizarra = QTextEdit()
        self.pizarra.setReadOnly(True)
        self.pizarra.setText("1. Pega el link\n2. Dale a Arrancar\n3. Se abre una ventana nueva para que no se trabe.")

        capa.addWidget(QLabel("LINK DEL SITIO:"))
        capa.addWidget(self.barra_url)
        capa.addLayout(fila)
        capa.addWidget(self.pizarra)

    def comenzar(self):
        link = self.barra_url.text().strip()
        if not link: return
        
        fuerza = self.nivel.currentText()
        self.pizarra.append(f"\n[*] LANZANDO...")
        
        threading.Thread(target=self.tarea, args=(link, fuerza), daemon=True).start()

    def tarea(self, link, f):
        orden = f"sqlmap -u '{link}' --batch --risk {f} --random-agent"
        os.system(f"xterm -hold -e \"{orden}\" || gnome-terminal -- bash -c \"{orden}; exec bash\" || {orden}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = PantallaPrincipal()
    ventana.show()
    sys.exit(app.exec())
