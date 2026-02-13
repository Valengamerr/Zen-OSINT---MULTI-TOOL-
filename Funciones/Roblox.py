import sys
import os
import requests
import json
import webbrowser
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QLabel, QPushButton, QTextEdit, 
                             QTabWidget, QFrame, QScrollArea)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt

os.environ["QT_LOGGING_RULES"] = "*=false"

class ZenRobloxTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1000, 800)
        self.setWindowTitle("Zen OSINT - Buscar por usuario de roblox + Herramientas de Cookies ")
        self.init_ui()

    def init_ui(self):

        self.setStyleSheet("""
            QWidget { background-color: #060608; color: #ffffff; font-family: 'Inter', 'Segoe UI'; }
            QTabWidget::pane { border: 1px solid #1a1a20; background: #0a0a0f; border-radius: 10px; }
            QTabBar::tab { 
                background: #111; color: #777; padding: 12px 25px; 
                border-top-left-radius: 8px; border-top-right-radius: 8px; 
            }
            QTabBar::tab:selected { background: #0a0a0f; color: #A020F0; border-bottom: 2px solid #A020F0; }
            QLineEdit { 
                background: #0f0f15; border: 1px solid #222; border-radius: 8px; 
                padding: 15px; color: #FFA07A; font-size: 14px;
            }
            QPushButton { 
                background: #1a1a1f; border: 1px solid #A020F0; border-radius: 8px; 
                padding: 12px; font-weight: bold; color: #fff;
            }
            QPushButton:hover { background: #A020F0; }
            QTextEdit { background: #000; border: 1px solid #111; border-radius: 8px; padding: 10px; color: #fff; }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)


        header = QLabel("ZEN <span style='color:#A020F0;'>ROBLOX</span> OSINT")
        header.setFont(QFont("Arial Black", 32))
        main_layout.addWidget(header, alignment=Qt.AlignmentFlag.AlignCenter)

        self.tabs = QTabWidget()


        self.tab_info = QWidget()
        l_info = QVBoxLayout(self.tab_info)
        
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("INGRESA USERNAME O ID DE ROBLOX...")
        l_info.addWidget(self.user_input)

        h_btns = QHBoxLayout()
        btn_user = QPushButton("BUSCAR POR USERNAME")
        btn_user.clicked.connect(self.get_info_by_name)
        btn_id = QPushButton("BUSCAR POR ID")
        btn_id.clicked.connect(self.get_info_by_id)
        h_btns.addWidget(btn_user)
        h_btns.addWidget(btn_id)
        l_info.addLayout(h_btns)

        self.info_log = QTextEdit()
        self.info_log.setReadOnly(True)
        l_info.addWidget(self.info_log)


        self.tab_cookie = QWidget()
        l_cookie = QVBoxLayout(self.tab_cookie)
        
        self.cookie_input = QLineEdit()
        self.cookie_input.setPlaceholderText("PEGA EL .ROBLOSECURITY AQUI...")
        l_cookie.addWidget(self.cookie_input)

        h_c_btns = QHBoxLayout()
        btn_c_info = QPushButton("EXTRAER INFO COOKIE")
        btn_c_info.clicked.connect(self.get_cookie_info)
        btn_c_login = QPushButton("LOGIN EN NAVEGADOR")
        btn_c_login.clicked.connect(self.cookie_login)
        h_c_btns.addWidget(btn_c_info)
        h_c_btns.addWidget(btn_c_login)
        l_cookie.addLayout(h_c_btns)

        self.cookie_log = QTextEdit()
        self.cookie_log.setReadOnly(True)
        l_cookie.addWidget(self.cookie_log)

        self.tabs.addTab(self.tab_info, "USER / ID ")
        self.tabs.addTab(self.tab_cookie, "Herrmientas de COOKIES ")
        main_layout.addWidget(self.tabs)

    def log_data(self, target_log, data):
        target_log.clear()
        r, w = "#FF0000", "#FFFFFF"
        for k, v in data.items():
            formatted = f"<span style='color:{w};'>[</span><span style='color:{r};'>+</span><span style='color:{w};'>]</span> <span style='color:{r};'>{k}:</span> {v}"
            target_log.append(formatted)

    def get_info_by_name(self):
        name = self.user_input.text().strip()
        try:
            res = requests.post("https://users.roblox.com/v1/usernames/users", json={"usernames": [name], "excludeBannedUsers": False})
            user_id = res.json()['data'][0]['id']
            self.fetch_roblox_api(user_id)
        except: self.info_log.setText("USUARIO NO ENCONTRADO")

    def get_info_by_id(self):
        uid = self.user_input.text().strip()
        self.fetch_roblox_api(uid)

    def fetch_roblox_api(self, uid):
        try:
            u = requests.get(f"https://users.roblox.com/v1/users/{uid}").json()
            data = {
                "Nombre-usuario": u.get('name'),
                "ID": u.get('id'),
                "Nombre": u.get('displayName'),
                "BIO": u.get('description') or "None",
                "Creado": u.get('created'),
                "BANN": u.get('isBanned'),
                "VERIFICADO": u.get('hasVerifiedBadge')
            }
            self.log_data(self.info_log, data)
        except: self.info_log.setText("ID NO VÁLIDO")

    def get_cookie_info(self):
        cookie = self.cookie_input.text().strip()
        try:
            res = requests.get("https://www.roblox.com/mobileapi/userinfo", cookies={".ROBLOSECURITY": cookie})
            if res.status_code != 200: raise Exception
            info = res.json()
            data = {
                "Estado": "Valid",
                "Usuario": info.get('UserName'),
                "Usuario ID": info.get('UserID'),
                "Robux": info.get('RobuxBalance'),
                "Premium": info.get('IsPremium'),
                "BUILDERS CLUB": info.get('IsAnyBuildersClubMember'),
                "THUMBNAIL": info.get('ThumbnailUrl')
            }
            self.log_data(self.cookie_log, data)
        except: self.cookie_log.setText("COOKIE INVALIDA O EXPIRADA")

    def cookie_login(self):

        self.cookie_log.append("<br><span style='color:yellow;'>[!] Para login manual rapido: Abre consola (F12) en Roblox.com > Application > Cookies > .ROBLOSECURITY > Pega el valor</span>")
        webbrowser.open("https://www.roblox.com/home")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ZenRobloxTool()
    window.show()
    sys.exit(app.exec())
