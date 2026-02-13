import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import requests
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QPushButton, QTextEdit, QLabel)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont

try:
    from Config.Util import *
    from Config.Config import *
except Exception as e:

    try: ErrorModule(e)
    except: print(f"Advertencia: No se pudo cargar Config.Util: {e}")

class IPScannerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Zen OSINT - Informacion de IP")
        self.setFixedSize(650, 580)
        

        self.setStyleSheet("""
            QWidget { background-color: #050505; color: #e0e0e0; font-family: 'Segoe UI'; }
            
            QLineEdit {
                background-color: #0d0d0f;
                border: 1px solid #1c1c1e;
                border-radius: 8px;
                padding: 12px;
                color: #ffffff;
                font-size: 14px;
            }
            QLineEdit:focus { border: 1px solid #A020F0; }

            QTextEdit {
                background-color: #08080a;
                border: 1px solid #1a1a1c;
                border-radius: 10px;
                color: #ffffff;
                font-family: 'Consolas', monospace;
                font-size: 12px;
                padding: 15px;
            }

            QLabel#footer {
                color: #4b4b4b;
                font-size: 10px;
                font-weight: bold;
            }
            
            QLabel#header {
                font-size: 22px; 
                font-weight: 900; 
                color: #ffffff; 
                letter-spacing: 1px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 20)
        layout.setSpacing(15)


        header = QLabel("Busqueda por IP")
        header.setObjectName("header")
        layout.addWidget(header)

 
        self.input_ip = QLineEdit()
        self.input_ip.setPlaceholderText("Ingresa la IP")
        self.input_ip.returnPressed.connect(self.process_ip) 
        layout.addWidget(self.input_ip)


        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setPlaceholderText("Esperando IP...")
        layout.addWidget(self.console)


        footer_layout = QHBoxLayout()
        footer_layout.addStretch()
        credits = QLabel("Zen OSINT creado por t.me/Valen_Qq")
        credits.setObjectName("footer")
        footer_layout.addWidget(credits)
        layout.addLayout(footer_layout)

    def process_ip(self):
        ip = self.input_ip.text().strip()
        if not ip:
            return

        self.console.clear()
        self.console.append(f"<span style='color:#A020F0;'>[~] Obteniendo datos</span>")
        QApplication.processEvents() 

        try:

            response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
            data = response.json()
            
            if data["status"] == "fail":
                estado = "Invalida / Sin Datos"
                res = {k: "N/A" for k in ["country", "countryCode", "regionName", "region", "city", "zip", "lat", "lon", "timezone", "isp", "org", "as"]}
            else:
                estado = "Válida"
                res = data

            latitud = res.get('lat', '0')
            longitud = res.get('lon', '0')
            url_posicion = f"https://www.google.com/maps?q={latitud},{longitud}"


            result_template = f"""
            <div style='line-height: 150%;'>
            <b style='color:#A020F0;'>[+] IP           :</b> <span style='color:white;'>{ip}</span><br>
            <b style='color:#A020F0;'>[+] Estado       :</b> <span style='color:white;'>{estado}</span><br>
            <b style='color:#A020F0;'>[+] Pais         :</b> <span style='color:white;'>{res.get('country')} ({res.get('countryCode')})</span><br>
            <b style='color:#A020F0;'>[+] Region       :</b> <span style='color:white;'>{res.get('regionName')} ({res.get('region')})</span><br>
            <b style='color:#A020F0;'>[+] Cod. Postal  :</b> <span style='color:white;'>{res.get('zip')}</span><br>
            <b style='color:#A020F0;'>[+] Ciudad       :</b> <span style='color:white;'>{res.get('city')}</span><br>
            <b style='color:#A020F0;'>[+] Latitud      :</b> <span style='color:white;'>{latitud}</span><br>
            <b style='color:#A020F0;'>[+] Longitud     :</b> <span style='color:white;'>{longitud}</span><br>
            <b style='color:#A020F0;'>[+] Zona Horaria :</b> <span style='color:white;'>{res.get('timezone')}</span><br>
            <b style='color:#A020F0;'>[+] Proveedor ISP:</b> <span style='color:white;'>{res.get('isp')}</span><br>
            <b style='color:#A020F0;'>[+] Organizacion :</b> <span style='color:white;'>{res.get('org')}</span><br>
            <b style='color:#A020F0;'>[+] AS (Numero)  :</b> <span style='color:white;'>{res.get('as')}</span><br>
            </div>
            """
            self.console.setHtml(result_template)


            try:
                BrowserPrivate(site=url_posicion, title=f"Localizacion IP ({latitud}, {longitud})", search_bar=False)
            except:
                pass

        except Exception as e:
            self.console.append(f"<br><span style='color:#ff4444;'>[!] Error de conexion: {str(e)}</span>")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = IPScannerUI()
    window.show()
    sys.exit(app.exec())
