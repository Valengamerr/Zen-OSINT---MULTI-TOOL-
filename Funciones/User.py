import sys
import os
import requests
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QTextEdit, QLabel, QFrame)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap

# --- CONFIGURACIÓN DE RUTAS ---
ruta_script = os.path.abspath(__file__)
ruta_raiz = os.path.dirname(os.path.dirname(ruta_script))
if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)

class ScannerThread(QThread):
    resultado_sig = pyqtSignal(str, str) # Nombre sitio, URL o None
    finalizado_sig = pyqtSignal()

    def __init__(self, username):
        super().__init__()
        self.username = username
        # Lista de sitios basada en UserRecon
        self.sitios = {
            "Instagram": f"https://www.instagram.com/{username}",
            "Facebook": f"https://www.facebook.com/{username}",
            "Twitter": f"https://www.twitter.com/{username}",
            "YouTube": f"https://www.youtube.com/{username}",
            "GitHub": f"https://github.com/{username}",
            "Reddit": f"https://www.reddit.com/user/{username}",
            "Pinterest": f"https://www.pinterest.com/{username}",
            "Spotify": f"https://open.spotify.com/user/{username}",
            "Steam": f"https://steamcommunity.com/id/{username}",
            "Twitch": f"https://www.twitch.tv/{username}",
            "SoundCloud": f"https://soundcloud.com/{username}",
            "Vimeo": f"https://vimeo.com/{username}",
            "DailyMotion": f"https://www.dailymotion.com/{username}",
            "Medium": f"https://medium.com/@{username}",
            "Behance": f"https://www.behance.net/{username}",
            "Pastebin": f"https://pastebin.com/u/{username}"
        }

    def run(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        for nombre, url in self.sitios.items():
            try:
                # Usamos requests para mayor velocidad (como el curl del script original)
                response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
                if response.status_code == 200:
                    # Algunas redes devuelven 200 pero dicen "Usuario no encontrado" en el texto
                    if "not found" in response.text.lower() or "doesn't exist" in response.text.lower():
                        self.resultado_sig.emit(nombre, None)
                    else:
                        self.resultado_sig.emit(nombre, url)
                else:
                    self.resultado_sig.emit(nombre, None)
            except:
                self.resultado_sig.emit(nombre, "Error")
        self.finalizado_sig.emit()

class UsernameTrackerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.ruta_iconos = os.path.join(ruta_raiz, "Iconos")
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Zen OSINT - Username Tracker | Valen_Qq")
        self.setFixedSize(650, 650)
        self.setStyleSheet("""
            QWidget { background-color: #050505; color: #e0e0e0; font-family: 'Segoe UI'; }
            #input_frame { background-color: #0d0d0f; border: 1px solid #1c1c1e; border-radius: 10px; min-height: 48px; }
            #input_frame:focus-within { border: 1px solid #A020F0; }
            QLineEdit { background-color: transparent; border: none; color: #ffffff; font-size: 14px; }
            QTextEdit { background-color: #08080a; border: 1px solid #1a1a1c; border-radius: 10px; color: #ffffff; font-family: 'Consolas', monospace; padding: 15px; }
            QLabel#header { font-size: 22px; font-weight: 900; color: white; }
            QLabel#credits { color: #555; font-size: 11px; font-weight: bold; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 20)

        header = QLabel("USERNAME TRACKER SCANNER")
        header.setObjectName("header")
        layout.addWidget(header)

        # Input con Icono (Usaremos el de Email.svg o podrías crear uno User.svg)
        self.input_frame = QFrame(objectName="input_frame")
        input_inner = QHBoxLayout(self.input_frame)
        self.icon_label = QLabel()
        path_icon = os.path.join(self.ruta_iconos, "ID.svg") # O el que prefieras
        if os.path.exists(path_icon):
            self.icon_label.setPixmap(QPixmap(path_icon).scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio))
        
        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Introduce el nombre de usuario")
        self.input_user.returnPressed.connect(self.iniciar_escaneo)
        input_inner.addWidget(self.icon_label)
        input_inner.addWidget(self.input_user)
        layout.addWidget(self.input_frame)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        layout.addWidget(self.console)

        credits = QLabel("Zen OSINT creado por Valen_Qq")
        credits.setObjectName("credits")
        layout.addWidget(credits, alignment=Qt.AlignmentFlag.AlignRight)

    def log(self, text, color="white"):
        self.console.append(f"<span style='color:{color};'>{text}</span>")

    def iniciar_escaneo(self):
        user = self.input_user.text().strip()
        if not user: return
        
        self.console.clear()
        self.log(f"[~] Rastreando usuario: {user} en múltiples redes...", "#A020F0")
        
        self.thread = ScannerThread(user)
        self.thread.resultado_sig.connect(self.mostrar_resultado)
        self.thread.finalizado_sig.connect(lambda: self.log("\n[!] Escaneo completado.", "#A020F0"))
        self.thread.start()

    def mostrar_resultado(self, nombre, url):
        if url == "Error":
            self.log(f"[!] {nombre}: Error de conexión", "orange")
        elif url:
            self.log(f"[+] {nombre}: ENCONTRADO -> {url}", "#00ff00")
        else:
            self.log(f"[-] {nombre}: No encontrado", "#555")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UsernameTrackerUI()
    window.show()
    sys.exit(app.exec())
