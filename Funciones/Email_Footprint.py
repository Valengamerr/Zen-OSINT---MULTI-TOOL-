# Asegurate de tener todas las librerias, att : Valen_Qq
# Creado por t.me/Valen_Qq
import sys
import os
import time


ruta_script = os.path.abspath(__file__)
carpeta_funciones = os.path.dirname(ruta_script)
ruta_raiz = os.path.dirname(carpeta_funciones)

if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)


from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QTextEdit, QLabel, QFrame, QComboBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from deep_translator import GoogleTranslator

class EmailFootprintUI(QWidget):
    def __init__(self):
        super().__init__()
        self.ruta_iconos = os.path.join(ruta_raiz, "Iconos")
        self.driver = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Zen OSINT - Email Tracker | Valen_Qq")
        self.setFixedSize(650, 650)
        
        self.setStyleSheet("""
            QWidget { background-color: #050505; color: #e0e0e0; font-family: 'Segoe UI'; }
            #input_frame { background-color: #0d0d0f; border: 1px solid #1c1c1e; border-radius: 10px; min-height: 48px; }
            #input_frame:focus-within { border: 1px solid #A020F0; }
            QLineEdit { background-color: transparent; border: none; color: #ffffff; font-size: 14px; }
            QComboBox { background-color: #0d0d0f; border: 1px solid #1c1c1e; color: white; border-radius: 5px; padding: 5px; min-width: 180px; }
            QTextEdit { background-color: #08080a; border: 1px solid #1a1a1c; border-radius: 10px; color: #ffffff; font-family: 'Consolas', monospace; padding: 15px; }
            QLabel#header { font-size: 22px; font-weight: 900; color: white; }
            QLabel#credits { color: #555; font-size: 11px; font-weight: bold; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 20)
        layout.setSpacing(15)

        layout.addWidget(QLabel("EMAIL FOOTPRINT TRACKER", objectName="header"))


        nav_lay = QHBoxLayout()
        nav_lay.addWidget(QLabel("Browser:"))
        self.browser_choice = QComboBox()
        self.browser_choice.setIconSize(QSize(18, 18))
        path_chrome = os.path.join(self.ruta_iconos, "Chrome.svg")
        icon_chrome = QIcon(path_chrome) if os.path.exists(path_chrome) else QIcon()
        self.browser_choice.addItem(icon_chrome, "Chrome (Visible)")
        self.browser_choice.addItem(icon_chrome, "Chrome (Headless)")
        nav_lay.addWidget(self.browser_choice)
        nav_lay.addStretch()
        layout.addLayout(nav_lay)

 
        self.input_frame = QFrame(objectName="input_frame")
        input_inner = QHBoxLayout(self.input_frame)
        self.icon_label = QLabel()
        path_email_svg = os.path.join(self.ruta_iconos, "Email.svg")
        if os.path.exists(path_email_svg):
            self.icon_label.setPixmap(QPixmap(path_email_svg).scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio))
        
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Introduce el email a investigar...")
        self.input_email.returnPressed.connect(self.ejecutar_rastro)
        input_inner.addWidget(self.icon_label)
        input_inner.addWidget(self.input_email)
        layout.addWidget(self.input_frame)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        layout.addWidget(self.console)

        credits = QLabel("Zen OSINT creado por Valen_Qq")
        credits.setObjectName("credits")
        layout.addWidget(credits, alignment=Qt.AlignmentFlag.AlignRight)

    def log(self, text, color="white"):
        self.console.append(f"<span style='color:{color};'>{text}</span>")
        QApplication.processEvents()

    def check_site(self, nombre, url, selector_type, selector_val, email, keyword_found):
        self.log(f"[~] Verificando {nombre}...", "#777")
        try:
            self.driver.get(url)
            wait = WebDriverWait(self.driver, 10)
            

            campo = wait.until(EC.presence_of_element_located((selector_type, selector_val)))
            campo.send_keys(email)
            campo.send_keys(Keys.RETURN)
            
            time.sleep(8)
            

            page_text = self.driver.execute_script("return document.documentElement.innerText")
            translated = GoogleTranslator(source='auto', target='en').translate(page_text)
            
            if keyword_found.lower() in translated.lower():
                self.log(f"[+] {nombre}: REGISTRADO", "#00ff00")
            else:
                self.log(f"[-] {nombre}: No registrado", "#555")
        except Exception as e:
            self.log(f"[!] {nombre}: Error (Timeout/Captcha)", "orange")

    def ejecutar_rastro(self):
        email = self.input_email.text().strip()
        if not email: return
        
        self.console.clear()
        self.log(f"[~] Iniciando motor OSINT para: {email}", "#A020F0")

        opts = webdriver.ChromeOptions()
        if "Headless" in self.browser_choice.currentText():
            opts.add_argument("--headless")
        
        try:
            self.driver = webdriver.Chrome(options=opts)
            

            sitios = [
                ("Google", "https://accounts.google.com/signin/v2/identifier", By.NAME, "identifier", "Enter your password"),
                ("Instagram", "https://www.instagram.com/accounts/emailsignup/", By.NAME, "emailOrPhone", "Another account uses"),
                ("Microsoft", "https://login.microsoftonline.com/", By.NAME, "loginfmt", "Enter password"),
                ("Snapchat", "https://accounts.snapchat.com/", By.ID, "ai_input", "Confirm it's you")
            ]

            for s in sitios:
                self.check_site(s[0], s[1], s[2], s[3], email, s[4])

            self.driver.quit()
            self.log("\n[!] Análisis finalizado con éxito.", "#A020F0")
            
        except Exception as e:
            self.log(f"[!] Error crítico: {e}", "red")
            if self.driver: self.driver.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmailFootprintUI()
    window.show()
    sys.exit(app.exec())

