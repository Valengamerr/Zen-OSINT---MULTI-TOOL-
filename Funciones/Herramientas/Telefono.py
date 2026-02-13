import sys
import os



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QTextEdit, QLabel)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor


try:
    from Herramientas.Logica_Telefono import buscar_telefono
except ImportError:

    from Herramientas.Telefono import buscar_telefono

class TelefonoVista(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Zen OSINT - Interfaz Teléfono")
        self.setFixedSize(650, 580)
        

        self.setStyleSheet("""
            QWidget { background-color: #050505; color: #e0e0e0; font-family: 'Segoe UI'; }
            QLineEdit {
                background-color: #0d0d0f;
                border: 1px solid #1c1c1e;
                border-radius: 10px;
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
                padding: 15px;
            }
            QLabel#footer { color: #444; font-size: 10px; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 20)
        
        header = QLabel("BÚSQUEDA TELEFÓNICA")
        header.setStyleSheet("font-size: 22px; font-weight: 900; color: #ffffff;")
        layout.addWidget(header)

        self.input_phone = QLineEdit()
        self.input_phone.setPlaceholderText("Escribe el número y presiona Enter...")
        self.input_phone.returnPressed.connect(self.ejecutar_busqueda)
        layout.addWidget(self.input_phone)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        layout.addWidget(self.console)


        footer = QLabel("Zen OSINT creado por t.me/Valen_Qq")
        footer.setObjectName("footer")
        layout.addWidget(footer, alignment=Qt.AlignmentFlag.AlignRight)

    def ejecutar_busqueda(self):
        numero = self.input_phone.text().strip()
        if not numero: return

        self.console.clear()
        self.console.append(f"<span style='color:#A020F0;'>[~] Consultando motor lógico...</span>")
        QApplication.processEvents()


        resultado = buscar_telefono(numero)

        if resultado["success"]:
            d = resultado["data"]
            res_html = f"""
            <div style='line-height: 160%;'>
            <b style='color:#A020F0;'>[+] Número       :</b> <span style='color:white;'>{d['phone']}</span><br>
            <b style='color:#A020F0;'>[+] Formato      :</b> <span style='color:white;'>{d['formatted']}</span><br>
            <b style='color:#A020F0;'>[+] Estado       :</b> <span style='color:#00ff00;'>{d['status']}</span><br>
            <b style='color:#A020F0;'>[+] País         :</b> <span style='color:white;'>{d['country_iso']}</span><br>
            <b style='color:#A020F0;'>[+] Región       :</b> <span style='color:white;'>{d['region']}</span><br>
            <b style='color:#A020F0;'>[+] Operador     :</b> <span style='color:white;'>{d['operator']}</span><br>
            <b style='color:#A020F0;'>[+] Tipo         :</b> <span style='color:white;'>{d['type']}</span><br>
            <b style='color:#A020F0;'>[+] Zona Horaria :</b> <span style='color:white;'>{d['timezone']}</span><br>
            </div>
            """
            self.console.setHtml(res_html)
        else:
            self.console.setHtml(f"<b style='color:#ff4444;'>[!] Error: {resultado['error']}</b>")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = TelefonoVista()
    win.show()
    sys.exit(app.exec())
