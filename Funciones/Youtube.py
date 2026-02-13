import sys
import os
from pytube import YouTube
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QTextEdit, QLabel, QFrame, QPushButton, QFileDialog)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon

# --- CONFIGURACIÓN DE RUTAS ---
ruta_script = os.path.abspath(__file__)
ruta_raiz = os.path.dirname(os.path.dirname(ruta_script))
if ruta_raiz not in sys.path: 
    sys.path.insert(0, ruta_raiz)

class YoutubePytubeUI(QWidget):
    def __init__(self):
        super().__init__()
        self.ruta_iconos = os.path.join(ruta_raiz, "Iconos")
        self.init_ui()

    def get_icon_pixmap(self, name, size=18):
        path = os.path.join(self.ruta_iconos, name)
        if os.path.exists(path):
            return QPixmap(path).scaled(size, size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        return QPixmap()

    def init_ui(self):
        self.setWindowTitle("Zen OSINT - Pytube Downloader | Valen_Qq")
        self.setFixedSize(650, 560)
        

        self.setStyleSheet("""
            QWidget { background-color: #050505; color: #e0e0e0; font-family: 'Segoe UI'; }
            .InputFrame { background-color: transparent; border-bottom: 1px solid #1c1c1e; margin-bottom: 15px; }
            .InputFrame:focus-within { border-bottom: 1px solid #A020F0; }
            QLineEdit { background-color: transparent; border: none; color: white; font-size: 14px; padding: 10px; }
            QPushButton#download_btn { background-color: #A020F0; border-radius: 8px; color: white; padding: 12px; font-weight: bold; }
            QPushButton#download_btn:hover { background-color: #b545ff; }
            QPushButton#browse_btn { background-color: #0d0d0f; border: 1px solid #1c1c1e; border-radius: 5px; color: #888; padding: 5px 12px; font-size: 11px; }
            QTextEdit { background-color: #08080a; border: 1px solid #121214; border-radius: 10px; color: #A020F0; font-family: 'Consolas'; padding: 10px; }
            QLabel#header { font-size: 20px; font-weight: 800; color: white; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 25)

        layout.addWidget(QLabel("PYTUBE DOWNLOADER", objectName="header"))
        layout.addSpacing(10)


        self.frame_url = QFrame(); self.frame_url.setProperty("class", "InputFrame")
        lay_url = QHBoxLayout(self.frame_url); lay_url.setContentsMargins(0,0,0,0)
        ico_url = QLabel(); ico_url.setPixmap(self.get_icon_pixmap("Video_nombre.svg"))
        self.url_input = QLineEdit(); self.url_input.setPlaceholderText("URL del video...")
        lay_url.addWidget(ico_url); lay_url.addWidget(self.url_input)
        layout.addWidget(self.frame_url)


        self.frame_name = QFrame(); self.frame_name.setProperty("class", "InputFrame")
        lay_name = QHBoxLayout(self.frame_name); lay_name.setContentsMargins(0,0,0,0)
        ico_name = QLabel(); ico_name.setPixmap(self.get_icon_pixmap("Nombre_archivo.svg"))
        self.name_input = QLineEdit(); self.name_input.setPlaceholderText("Nombre del archivo (sin .mp4)...")
        lay_name.addWidget(ico_name); lay_name.addWidget(self.name_input)
        layout.addWidget(self.frame_name)


        self.frame_path = QFrame(); self.frame_path.setProperty("class", "InputFrame")
        lay_path = QHBoxLayout(self.frame_path); lay_path.setContentsMargins(0,0,0,0)
        ico_path = QLabel(); ico_path.setPixmap(self.get_icon_pixmap("Carpeta_destino.svg"))
        self.path_input = QLineEdit(); self.path_input.setPlaceholderText("Ruta de guardado...")
        self.btn_browse = QPushButton(" Explorar", objectName="browse_btn")
        path_explorar = os.path.join(self.ruta_iconos, "Explorar.svg")
        if os.path.exists(path_explorar): self.btn_browse.setIcon(QIcon(path_explorar))
        self.btn_browse.clicked.connect(self.seleccionar_carpeta)
        lay_path.addWidget(ico_path); lay_path.addWidget(self.path_input); lay_path.addWidget(self.btn_browse)
        layout.addWidget(self.frame_path)


        self.btn_download = QPushButton("DESCARGAR CON PYTUBE", objectName="download_btn")
        self.btn_download.clicked.connect(self.descargar_pytube)
        layout.addWidget(self.btn_download)

        self.console = QTextEdit(); self.console.setReadOnly(True)
        layout.addWidget(self.console)

    def seleccionar_carpeta(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta")
        if folder: self.path_input.setText(folder)

    def log(self, text, is_error=False):
        color = "#ff4444" if is_error else "#A020F0"
        self.console.append(f"<span style='color:{color};'>» {text}</span>")
        QApplication.processEvents()

    def descargar_pytube(self):
        url = self.url_input.text().strip()
        path = self.path_input.text().strip()
        name = self.name_input.text().strip()

        if not url or not path:
            self.log("Faltan datos.", True)
            return

        try:
            self.log("Conectando con Pytube...")
            yt = YouTube(url)
            

            video = yt.streams.get_highest_resolution()
            
            self.log(f"Descargando: {yt.title}")
            

            out_file = video.download(output_path=path)
            

            if name:
                new_file = os.path.join(path, f"{name}.mp4")
                os.rename(out_file, new_file)
                self.log(f"Guardado como: {name}.mp4")
            else:
                self.log("Descarga completada con éxito.")

        except Exception as e:
            self.log(f"Error en Pytube: {str(e)}", True)
            self.log("TIP: Pytube falla seguido yt-dlp es más estable.", "#888")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = YoutubePytubeUI()
    win.show()
    sys.exit(app.exec())
