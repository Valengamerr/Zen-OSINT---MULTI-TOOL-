# Codigo creado por t.me/Valen_Qq
# Porfavor distribuir esta herramienta donde quieras, DarkWeb, Telegram, Github, Instagram, Tiktok, Discord. Pero porfavor dar creditos

import sys
import os
import socket
import requests
import time
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLineEdit, 
                             QTextEdit, QLabel, QPushButton, QProgressBar)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

os.environ["QT_LOGGING_RULES"] = "*=false"

class ScannerEngine(QThread):

    resultado_final = pyqtSignal(str)
    progreso_update = pyqtSignal(int)
    log_update = pyqtSignal(str)

    def __init__(self, target_url):
        super().__init__()
        self.url = target_url.replace("https://", "").replace("http://", "").split('/')[0].strip()

    def run(self):
        try:
            inicio = time.time()
            self.log_update.emit(f"[*] Analizando host: {self.url}...")


            try:
                ip = socket.gethostbyname(self.url)
                geo = requests.get(f"http://ip-api.com/json/{ip}", timeout=3).json()
                seguro = "SI" if self.url.startswith("") else "Revisando..." 
            except: ip, geo, seguro = "Error", {}, "No"


            try:
                r_err = requests.get(f"http://{self.url}/fake_path_{int(time.time())}", timeout=2)
                err_size = len(r_err.content)
            except: err_size = 0


            targets = [
                "/.env", "/config.php", "/wp-config.php", "/db.sql", "/database.sql", 
                "/backup.zip", "/dump.sql", "/phpmyadmin/", "/pma/", "/admin/", 
                "/administrator/", "/.git/config", "/.ssh/id_rsa", "/robots.txt", 
                "/server-status", "/logs/access.log", "/setup.php", "/api/.env",
                "/backup.sql", "/.htaccess", "basededatos.sql", "base_de_datos.sql",
                "BD.sql", "db.sql", "bd.sql", 
            ]
            
            confirmados = []
            firmas = ["db_password", "mysql", "index of", "phpmyadmin", "login", "root", "secret", "password", "contraseña", "Contraseña", "Usuario "]

            total = len(targets)
            for i, t in enumerate(targets):

                progreso = int(((i + 1) / total) * 100)
                self.progreso_update.emit(progreso)
                self.log_update.emit(f"[PROBANDO] {t}")

                try:
                    r = requests.get(f"http://{self.url}{t}", timeout=1.5, allow_redirects=True)
                    if r.status_code == 200 and len(r.content) != err_size:
                        match = any(f in r.text.lower() for f in firmas)
                        tag = "CONFIRMADO" if match else "VIVO"
                        color = "#00FF7F" if match else "#00BFFF"
                        confirmados.append(f"<span style='color:{color};'>{t.ljust(18)} [{tag}]</span>")
                    elif r.status_code == 403:
                        confirmados.append(f"<span style='color:#FF4500;'>{t.ljust(18)} [PROTEGIDO]</span>")
                except: continue
                time.sleep(0.1) 


            ms = round((time.time() - inicio) * 1000)
            res = "<pre style='font-family: monospace; font-size: 13px;'>"
            res += f"<span style='color:#A020F0;'>Dominio           </span> ➔ {self.url}\n"
            res += f"<span style='color:#A020F0;'>IP                </span> ➔ {ip}\n"
            res += f"<span style='color:#A020F0;'>ISP               </span> ➔ {geo.get('isp', 'N/A')}\n"
            res += f"<span style='color:#A020F0;'>Org               </span> ➔ {geo.get('org', 'N/A')}\n"
            res += f"<span style='color:#A020F0;'>Tiempo de respuesta</span> ➔ {ms} ms\n\n"

            res += f"<span style='color:white;'>┏━━━━━━━━━━━━━[ <span style='color:#ff4444;'>RESULTADOS FINALES</span> ]</span>\n"
            if confirmados:
                for c in confirmados: res += f"┣ {c}\n"
            else: res += "┣ <span style='color:#666;'>No se encontro nada...</span>\n"
            res += "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛</pre>"
            
            self.resultado_final.emit(res)
        except Exception as e:
            self.resultado_final.emit(f"Error: {str(e)}")

class ZenInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(700, 750)
        self.setWindowTitle("Zen OSINT - Informacion de una pagina web")
        self.setStyleSheet("background-color: #050505; color: #e0e0e0;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        self.status_label = QLabel("Esperando... | Creado por t.me/Valen_Qq")
        self.status_label.setStyleSheet("color: #A020F0; font-weight: bold; font-size: 14px;")
        layout.addWidget(self.status_label)

        self.input = QLineEdit(placeholderText="Introduce el dominio (ej. colegio.com)...")
        self.input.setStyleSheet("background:#111; border:1px solid #333; padding:15px; color:white; border-radius:5px;")
        layout.addWidget(self.input)

        self.btn = QPushButton("LANZAR ESCANEO")
        self.btn.setStyleSheet("background:#A020F0; color:white; font-weight:bold; padding:15px; border-radius:5px;")
        self.btn.clicked.connect(self.start_scan)
        layout.addWidget(self.btn)

        # Barra de progreso
        self.pbar = QProgressBar()
        self.pbar.setStyleSheet("""
            QProgressBar { border: 1px solid #333; border-radius: 5px; text-align: center; background: #111; }
            QProgressBar::chunk { background-color: #A020F0; }
        """)
        self.pbar.setValue(0)
        layout.addWidget(self.pbar)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setStyleSheet("background:#08080a; border:1px solid #121214; border-radius:10px; padding:15px;")
        layout.addWidget(self.console)

    def start_scan(self):
        url = self.input.text().strip()
        if not url: return
        
        self.btn.setEnabled(False)
        self.console.clear()
        self.pbar.setValue(0)
        
        self.worker = ScannerEngine(url)

        self.worker.progreso_update.connect(self.pbar.setValue)
        self.worker.log_update.connect(lambda m: self.status_label.setText(m))
        self.worker.resultado_final.connect(self.finish_scan)
        self.worker.start()

    def finish_scan(self, html):
        self.console.setHtml(html)
        self.status_label.setText("SCAN FINISHED")
        self.btn.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ZenInterface()
    win.show()
    sys.exit(app.exec())
