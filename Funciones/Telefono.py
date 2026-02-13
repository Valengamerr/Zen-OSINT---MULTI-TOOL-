import phonenumbers
import sys
import os
import requests
import webbrowser
from phonenumbers import geocoder, carrier, timezone

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QTextEdit, QLabel, QFrame)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QPixmap, QIcon

class TelefonoScannerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.icon_path = os.path.join(os.path.dirname(self.script_dir), "Iconos")
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Zen OSINT - Info de Numero | t.me/Valen_Qq")
        self.setFixedSize(650, 620)
        

        self.setStyleSheet("""
            QWidget { background-color: #050505; color: #e0e0e0; font-family: 'Segoe UI'; }
            
            #input_frame {
                background-color: #0d0d0f;
                border: 1px solid #1c1c1e;
                border-radius: 10px;
                max-height: 45px;
            }
            #input_frame:focus-within { border: 1px solid #A020F0; }

            QLineEdit {
                background-color: transparent;
                border: none;
                color: #ffffff;
                font-size: 14px;
                padding: 5px;
            }

            QTextEdit {
                background-color: #08080a;
                border: 1px solid #1a1a1c;
                border-radius: 10px;
                color: #ffffff;
                font-family: 'Consolas', monospace;
                padding: 15px;
            }
            
            QLabel#header { font-size: 22px; font-weight: 900; color: #ffffff; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 20)
        layout.setSpacing(15)

        header = QLabel("Buscar por numero de telefono")
        header.setObjectName("header")
        layout.addWidget(header)


        self.input_frame = QFrame()
        self.input_frame.setObjectName("input_frame")
        input_layout = QHBoxLayout(self.input_frame)
        input_layout.setContentsMargins(10, 0, 10, 0)
        input_layout.setSpacing(10)


        icon_label = QLabel()
        pix = QPixmap(os.path.join(self.icon_path, "Telefono.svg"))
        if not pix.isNull():
            icon_label.setPixmap(pix.scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        
        self.input_phone = QLineEdit()
        self.input_phone.setPlaceholderText("Ej: +34 911 333 333")
        self.input_phone.returnPressed.connect(self.process_number)

        input_layout.addWidget(icon_label)
        input_layout.addWidget(self.input_phone)
        layout.addWidget(self.input_frame)


        self.console = QTextEdit()
        self.console.setReadOnly(True)

        self.console.mousePressEvent = self.handle_links 
        layout.addWidget(self.console)

        footer = QLabel("Zen OSINT creado por t.me/Valen_Qq")
        footer.setStyleSheet("color: #444; font-size: 10px;")
        layout.addWidget(footer, alignment=Qt.AlignmentFlag.AlignRight)

    def handle_links(self, event):

        anchor = self.console.anchorAt(event.pos())
        if anchor:
            webbrowser.open(anchor)
        else:
            super(QTextEdit, self.console).mousePressEvent(event)

    def process_number(self):
        raw_input = self.input_phone.text().strip()
        cleaned = "".join(filter(lambda x: x.isdigit() or x == '+', raw_input))
        
        if cleaned and not cleaned.startswith('+'):
            cleaned = '+' + cleaned

        if not cleaned or len(cleaned) < 3: return

        self.console.clear()
        self.console.append(f"<span style='color:#A020F0;'>[~] Buscando.</span>")
        QApplication.processEvents()

        try:
            parsed = phonenumbers.parse(cleaned, None)
            es_valido = phonenumbers.is_valid_number(parsed)
            

            op = carrier.name_for_number(parsed, "es") or "Desconocido"
            reg = geocoder.description_for_number(parsed, "es") or "Desconocida"
            pais_nom = geocoder.country_name_for_number(parsed, "es")
            
            tipos = {0: "Fijo", 1: "Movil", 2: "Fijo/Movil", 3: "Gratuito", 4: "Premium", 6: "VoIP"}
            tipo = tipos.get(phonenumbers.number_type(parsed), "Especial")
            
            zonas = timezone.time_zones_for_number(parsed)
            iso = phonenumbers.region_code_for_number(parsed)
            
            f_int = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
            f_nac = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL)
            f_e164 = phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
            
            wa_link = f"https://wa.me/{cleaned.replace('+', '')}"

            res = f"""
            <div style='line-height: 150%;'>
            <b style='color:#BF40FF;'>[ RESULTADOS GENERALES ]</b><br>
            <b style='color:#A020F0;'>[+] Estado:</b> <span style='color:{'#00ff00' if es_valido else '#ffaa00'};'>{'Válido / Activo' if es_valido else 'Desconocido/Local'}</span><br>
            <b style='color:#A020F0;'>[+] Int. Formato:</b> <span style='color:white;'>{f_int}</span><br>
            <b style='color:#A020F0;'>[+] Nac. Formato:</b> <span style='color:white;'>{f_nac}</span><br>
            <b style='color:#A020F0;'>[+] E.164:</b> <span style='color:white;'>{f_e164}</span><br><br>

            <b style='color:#BF40FF;'>[ DATOS DE UBICACIÓN ]</b><br>
            <b style='color:#A020F0;'>[+] Pais:</b> <span style='color:white;'>{pais_nom} ({iso})</span><br>
            <b style='color:#A020F0;'>[+] Region:</b> <span style='color:white;'>{reg}</span><br>
            <b style='color:#A020F0;'>[+] Zona H.:</b> <span style='color:white;'>{', '.join(zonas)}</span><br><br>

            <b style='color:#BF40FF;'>[ INFORMACIÓN DE RED ]</b><br>
            <b style='color:#A020F0;'>[+] Operador:</b> <span style='color:white;'>{op}</span><br>
            <b style='color:#A020F0;'>[+] Tipo Linea:</b> <span style='color:white;'>{tipo}</span><br><br>
            
            <b style='color:#BF40FF;'>[ HERRAMIENTAS DIRECTAS ]</b><br>
            <b style='color:#A020F0;'>[+] WhatsApp:</b> <a href='{wa_link}' style='color:#00ff00; text-decoration: none;'>Abrir Chat en Navegador</a><br>
            <span style='color:#555;'>Link: {wa_link}</span>
            </div>
            """
            self.console.setHtml(res)

        except Exception as e:
            self.console.setHtml(f"<b style='color:#ff4444;'>[!] Error:</b> {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TelefonoScannerUI()
    window.show()
    sys.exit(app.exec())
