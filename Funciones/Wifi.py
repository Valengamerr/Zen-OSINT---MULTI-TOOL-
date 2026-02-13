
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# Zen Osint Creado por t.me/Valen_Qq 
# Si quieres mas herramientas como Un INFORSTEALER, Ransomware, Herramientas de administracion remota (rats) GRATIS !!! Visita este Github : Valengamerr    
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!     ----/   Porfavor distribuir esta herramienta donde quieras DarkWeb, Tiktok, BreachForus \--- !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!      ----/   No cambiar derechos de autor   \----
# En caso de error contactar a t.me/Valen_Qq
#
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# @--- LIBRERIAS ---@    - Asegurar de tener todas instaladas 
import sys
import os
import socket
import speedtest
import subprocess
from concurrent.futures import ThreadPoolExecutor
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QProgressBar, QFrame, QTextEdit)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap
# @---         Fin- Libs                --- @

os.environ["QT_LOGGING_RULES"] = "*=false"

class TurboScanner(QThread):
    resultado_final = pyqtSignal(str)
    progreso = pyqtSignal(int)
    speed_data = pyqtSignal(float, float)
    log = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.dispositivos = []

    def check_ip(self, ip):

        param = "-n" if os.name == "nt" else "-c"

        try:
            res = subprocess.call(["ping", param, "1", "-w", "200", ip], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if res == 0:
                try:
                    name = socket.gethostbyaddr(ip)[0]
                except:
                    name = "Unknown"
                return (ip, name)
        except:
            pass
        return None

    def run(self):
        try:

            self.log.emit("[*] MIDIENDO BANDA ANCHA...")
            st = speedtest.Speedtest()
            st.get_best_server()
            down = st.download() / 1_000_000
            up = st.upload() / 1_000_000
            self.speed_data.emit(up, down)
            self.progreso.emit(10)


            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            base_ip = ".".join(local_ip.split(".")[:-1])


            self.log.emit(f"[*] LANZANDO ESCANEO PARALELO EN {base_ip}.0/24...")
            ips_a_escanear = [f"{base_ip}.{i}" for i in range(1, 255)]
            

            with ThreadPoolExecutor(max_workers=50) as executor:
                resultados = list(executor.map(self.check_ip, ips_a_escanear))
            
            self.dispositivos = [r for r in resultados if r is not None]
            self.progreso.emit(90)


            res = "<pre style='font-family: monospace; font-size: 13px; color: white;'>"
            res += f"<span style='color:#A020F0;'>GATEWAY  </span> ➔ {base_ip}.1\n"
            res += f"<span style='color:#A020F0;'>MI IP        </span> ➔ {local_ip}\n\n"

            res += "<span style='color:white;'>┏━━━━━━━━━━━━━[ DISPOSITIVOS DETECTADOS ]</span>\n"
            for ip, name in self.dispositivos:
                tipo = "MODEM/GW" if ip.endswith(".1") else "HOST"
                res += f"┣ {tipo.ljust(10)} ➔ {ip.ljust(15)} | {name}\n"
            
            res += "┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛</pre>"
            
            self.progreso.emit(100)
            self.resultado_final.emit(res)

        except Exception as e:
            self.resultado_final.emit(f"ERROR: {str(e)}")

class ZenInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(750, 800)
        self.setWindowTitle("Zen Osint - Wifi test")
        self.setStyleSheet("background-color: #050505; color: #e0e0e0;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)


        speed_h = QHBoxLayout()
        path_iconos = os.path.join(os.getcwd(), "Iconos")


        self.box_down = QFrame()
        self.box_down.setStyleSheet("background: #0a0a0a; border: 1px solid #00ffff; border-radius: 4px;")
        v_down = QVBoxLayout(self.box_down)
        self.img_down = QLabel()
        pix_down = QPixmap(os.path.join(path_iconos, "Descarga.svg"))
        if not pix_down.isNull():
            self.img_down.setPixmap(pix_down.scaled(35, 35))
        else: self.img_down.setText("[V]")
        v_down.addWidget(self.img_down, alignment=Qt.AlignmentFlag.AlignCenter)
        self.val_down = QLabel("0.0")
        self.val_down.setStyleSheet("font-size: 26px; font-weight: bold; border:none;")
        v_down.addWidget(self.val_down, alignment=Qt.AlignmentFlag.AlignCenter)


        self.box_up = QFrame()
        self.box_up.setStyleSheet("background: #0a0a0a; border: 1px solid #A020F0; border-radius: 4px;")
        v_up = QVBoxLayout(self.box_up)
        self.img_up = QLabel()
        pix_up = QPixmap(os.path.join(path_iconos, "Subida.svg"))
        if not pix_up.isNull():
            self.img_up.setPixmap(pix_up.scaled(35, 35))
        else: self.img_up.setText("[^]")
        v_up.addWidget(self.img_up, alignment=Qt.AlignmentFlag.AlignCenter)
        self.val_up = QLabel("0.0")
        self.val_up.setStyleSheet("font-size: 26px; font-weight: bold; border:none;")
        v_up.addWidget(self.val_up, alignment=Qt.AlignmentFlag.AlignCenter)

        speed_h.addWidget(self.box_down)
        speed_h.addWidget(self.box_up)
        layout.addLayout(speed_h)

        self.btn = QPushButton("FULL SCAN (254 IPs)")
        self.btn.setStyleSheet("background:#A020F0; color:white; font-weight:bold; padding:15px; border-radius:2px;")
        self.btn.clicked.connect(self.start)
        layout.addWidget(self.btn)

        self.pbar = QProgressBar()
        self.pbar.setStyleSheet("QProgressBar { border: 1px solid #222; background: #000; height: 4px; } QProgressBar::chunk { background: #00ffff; }")
        layout.addWidget(self.pbar)

        self.status = QLabel("READY")
        self.status.setStyleSheet("color: #444; font-family: monospace;")
        layout.addWidget(self.status)

        self.console = QTextEdit(readOnly=True)
        self.console.setStyleSheet("background:#000; border:1px solid #111; padding:15px; font-family: monospace;")
        layout.addWidget(self.console)

    def start(self):
        self.btn.setEnabled(False)
        self.pbar.setValue(0)
        self.worker = TurboScanner()
        self.worker.speed_data.connect(lambda u, d: [self.val_up.setText(str(round(u,1))), self.val_down.setText(str(round(d,1)))])
        self.worker.progreso.connect(self.pbar.setValue)
        self.worker.log.connect(self.status.setText)
        self.worker.resultado_final.connect(lambda r: [self.console.setHtml(r), self.btn.setEnabled(True)])
        self.worker.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ZenInterface()
    win.show()
    sys.exit(app.exec())
