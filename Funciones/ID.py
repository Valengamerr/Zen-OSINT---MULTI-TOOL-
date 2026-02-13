import sys
import os
import random
from faker import Faker
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QLabel, QPushButton, QTextEdit)
from PyQt6.QtCore import Qt

os.environ["QT_LOGGING_RULES"] = "*=false"

class ZenIdentityV21(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(700, 850)
        self.setWindowTitle("Zen OSINT - Generador de identidad falsa")
        self.setStyleSheet("background-color: #050505; color: #e0e0e0; font-family: monospace;")
        
        self.init_ui()
        self.generate_new_identity()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)

        header = QLabel("Generador de identidad falsa")
        header.setStyleSheet("font-size: 20px; font-weight: bold; color: #A020F0; letter-spacing: 3px;")
        layout.addWidget(header, alignment=Qt.AlignmentFlag.AlignCenter)

        self.display = QTextEdit()
        self.display.setReadOnly(True)
        self.display.setStyleSheet("""
            background-color: #000; 
            border: 1px solid #1a1a1a; 
            padding: 25px; 
            font-size: 14px;
        """)
        layout.addWidget(self.display)

        self.btn = QPushButton("GENERAR DATASET")
        self.btn.setStyleSheet("""
            QPushButton {
                background: #A020F0; 
                color: white; 
                font-weight: bold; 
                padding: 20px; 
                border: 1px solid white;
            }
            QPushButton:hover { background: #B545FF; }
        """)
        self.btn.clicked.connect(self.generate_new_identity)
        layout.addWidget(self.btn)

    def generate_new_identity(self):
 
        loc = random.choice(['es_ES', 'es_MX', 'es_AR', 'en_US', 'pt_BR'])
        fk = Faker(loc)
        

        marcas = ["VISA", "MASTERCARD", "AMERICAN EXPRESS", "DISCOVER", "DINERS CLUB"]
        marca_random = random.choice(marcas)
        num_tarjeta = fk.credit_card_number()
        

        celular_raw = "".join([str(random.randint(0, 9)) for _ in range(11)])
        

        dni = f"{random.randint(10, 99)}.{random.randint(100, 999)}.{random.randint(100, 999)}"
        

        arr = "<span style='color:#FFA07A;'>➔</span>"
        
        res = "<pre style='color: white; line-height: 1.6;'>"
        res += f"<span style='color:#A020F0;'>Nombre completo   </span> {arr} {fk.name().upper()}\n"
        res += f"<span style='color:#A020F0;'>DNI / ID          </span> {arr} {dni}\n"
        res += f"<span style='color:#A020F0;'>IP                </span> {arr} {fk.ipv4()}\n"
        res += f"<span style='color:#A020F0;'>Pais              </span> {arr} {fk.country().upper()}\n"
        res += f"<span style='color:#A020F0;'>Tarjeta de credi. </span> {arr} {marca_random} | {num_tarjeta}\n"
        res += f"<span style='color:#A020F0;'>Celular           </span> {arr} {celular_raw}\n"
        res += f"<span style='color:#A020F0;'>Direccion         </span> {arr} {fk.address().replace('\\n', ', ').upper()}\n"
        res += f"<span style='color:#A020F0;'>Padre             </span> {arr} {fk.name_male().upper()}\n"
        res += f"<span style='color:#A020F0;'>Madre             </span> {arr} {fk.name_female().upper()}\n"
        res += f"<span style='color:#A020F0;'>Nacimiento        </span> {arr} {fk.date_of_birth(minimum_age=20, maximum_age=70).strftime('%d/%m/%Y')}\n"
        res += f"<span style='color:#A020F0;'>Trabajo           </span> {arr} {fk.job().upper()}\n"
        res += f"<span style='color:#A020F0;'>Num. Telefono     </span> {arr} {celular_raw}\n"
        res += "</pre>"
        
        self.display.setHtml(res)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ZenIdentityV21()
    win.show()
    sys.exit(app.exec())
