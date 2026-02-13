import sys
import os
import socket
import subprocess
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QTextEdit, QLabel, QFrame, QPushButton)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt6.QtGui import QPixmap, QIcon, QFont


os.environ["QT_LOGGING_RULES"] = "*=false"

class ScannerWorker(QThread):
    resultado = pyqtSignal(int, str)
    finalizado = pyqtSignal()

    def __init__(self, ip, start_p, end_p):
        super().__init__()
        self.ip = ip
        self.start_p = start_p
        self.end_p = end_p

    def run(self):
        for port in range(self.start_p, self.end_p + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.3)
            if sock.connect_ex((self.ip, port)) == 0:
                self.resultado.emit(port, "ABIERTO")
            sock.close()
        self.finalizado.emit()

class PortScannerZen(QWidget):
    def __init__(self):
        super().__init__()
        self.ruta_iconos = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Iconos")
        self.init_ui()

    def get_pix(self, name, size=18):
        path = os.path.join(self.ruta_iconos, name)
        if os.path.exists(path):
            return QPixmap(path).scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        return QPixmap()

    def init_ui(self):
        self.setWindowTitle("Zen OSINT - Port Scanner")
        self.setFixedSize(600, 680)
        

        self.setStyleSheet("""
            QWidget { background-color: #050505; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; }
            .InputFrame { border-bottom: 1px solid #1c1c1e; margin-bottom: 15px; background: transparent; }
            .InputFrame:focus-within { border-bottom: 1px solid #A020F0; }
            QLineEdit { background: transparent; border: none; color: white; font-size: 14px; padding: 10px; }
            QPushButton#main_btn { background: #A020F0; color: white; font-weight: bold; border-radius: 8px; padding: 12px; }
            QPushButton#main_btn:hover { background: #b545ff; }
            QPushButton#firewall_btn { background: #3d0a0a; color: #ff4444; border: 1px solid #ff4444; border-radius: 5px; font-weight: bold; padding: 8px; }
            QPushButton#firewall_btn:hover { background: #ff4444; color: white; }
            QTextEdit { background: #08080a; border: 1px solid #121214; border-radius: 10px; color: #00ff00; font-family: 'Consolas', monospace; padding: 10px; }
            QLabel#title { font-size: 22px; font-weight: 800; color: white; letter-spacing: 1px; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 30)

        layout.addWidget(QLabel("PORT SCANNER", objectName="title"))
        layout.addSpacing(15)


        self.f_ip = QFrame(); self.f_ip.setProperty("class", "InputFrame")
        lay_ip = QHBoxLayout(self.f_ip); lay_ip.setContentsMargins(0,0,0,0)
        ico_ip = QLabel(); ico_ip.setPixmap(self.get_pix("DNS.svg"))
        self.ip_input = QLineEdit(placeholderText="IP o Hostname...")
        lay_ip.addWidget(ico_ip); lay_ip.addWidget(self.ip_input)
        layout.addWidget(self.f_ip)


        self.f_range = QFrame(); self.f_range.setProperty("class", "InputFrame")
        lay_range = QHBoxLayout(self.f_range); lay_range.setContentsMargins(0,0,0,0)
        ico_range = QLabel(); ico_range.setPixmap(self.get_pix("Rango.svg"))
        self.range_input = QLineEdit(placeholderText="Rango (ej: 20-1000)...")
        lay_range.addWidget(ico_range); lay_range.addWidget(self.range_input)
        layout.addWidget(self.f_range)

        self.btn_scan = QPushButton("INICIAR ESCANEO", objectName="main_btn")
        self.btn_scan.clicked.connect(self.start_scan)
        layout.addWidget(self.btn_scan)

        self.console = QTextEdit(readOnly=True)
        layout.addWidget(self.console)

        layout.addSpacing(20)

  
        layout.addWidget(QLabel("Cerrar puertos", styleSheet="color: #555; font-weight: bold; font-size: 11px;"))
        self.f_fire = QHBoxLayout()
        self.port_close = QLineEdit(placeholderText="Puerto a bloquear...")
        self.port_close.setStyleSheet("background: #0d0d0f; border: 1px solid #1c1c1e; border-radius: 5px; padding: 8px;")
        self.btn_fire = QPushButton(" CERRAR PUERTO", objectName="firewall_btn")
        
        path_ico = os.path.join(self.ruta_iconos, "Cerrar_puerto.svg")
        if os.path.exists(path_ico): self.btn_fire.setIcon(QIcon(path_ico))
        
        self.btn_fire.clicked.connect(self.block_port)
        self.f_fire.addWidget(self.port_close); self.f_fire.addWidget(self.btn_fire)
        layout.addLayout(self.f_fire)

    def log(self, p, s):
        self.console.append(f"<span style='color:white;'>[{p}]</span> <span style='color:#A020F0;'>→</span> <span style='color:#00ff00;'>{s}</span>")

    def start_scan(self):
        target = self.ip_input.text().strip()
        rango = self.range_input.text().strip()
        if not target or "-" not in rango: return

        try:
            ip_val = socket.gethostbyname(target)
            start, end = map(int, rango.split('-'))
            self.console.clear()
            self.console.append(f"<i style='color:#888;'>Objetivo: {ip_val}</i><br>")
            self.btn_scan.setEnabled(False)
            
            self.worker = ScannerWorker(ip_val, start, end)
            self.worker.resultado.connect(self.log)
            self.worker.finalizado.connect(lambda: [self.btn_scan.setEnabled(True), self.console.append("<br><b style='color:white;'>Escaneo completado.</b>")])
            self.worker.start()
        except Exception as e:
            self.console.append(f"Error: {e}")

    def block_port(self):
        p = self.port_close.text().strip()
        if p:
            try:
                subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "tcp", "--dport", p, "-j", "DROP"], check=True)
                self.console.append(f"<span style='color:#ff4444;'>[!] Puerto {p} bloqueado en el sistema.</span>")
            except:
                self.console.append("<span style='color:orange;'>[!] Error: Requiere privilegios (sudo).</span>")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setDesktopSettingsAware(False)
    win = PortScannerZen()
    win.show()
    sys.exit(app.exec())
