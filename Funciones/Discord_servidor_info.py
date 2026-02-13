import sys
import requests
import threading
import time
import os
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QLabel, QPushButton, QTextEdit, 
                             QFrame, QStackedWidget, QScrollArea)
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt

class ZenCommander(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1200, 850)
        self.setWindowTitle("ZEN OSINT - Raider no verificado + Info server")
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget { background-color: #020202; color: #e0e0e0; font-family: 'Consolas', monospace; }
            

            QLineEdit { 
                background: #080808; 
                border: 2px solid #330000; 
                border-radius: 5px;
                padding: 15px; 
                color: #ffffff; 
                font-size: 14px; 
                margin-bottom: 10px;
            }
            QLineEdit:focus { border: 2px solid #FF0000; background: #0c0000; }


            #Sidebar { background-color: #050505; border-right: 2px solid #1a0000; }
            #MenuBtn { 
                background: transparent; border: none; color: #444; 
                padding: 25px; text-align: left; font-size: 13px; font-weight: bold;
                text-transform: uppercase;
            }
            #MenuBtn:checked { color: #FF0000; background: #0a0000; border-left: 5px solid #FF0000; }
            

            #ActionBtn { 
                background: #660000; color: #fff; border: 1px solid #FF0000; 
                padding: 18px; font-weight: bold; border-radius: 4px; 
            }
            #ActionBtn:hover { background: #FF0000; color: #000; }


            QTextEdit { 
                background-color: #000000; border: 1px solid #1a1a1a; 
                color: #FF0000; font-size: 11px; padding: 10px;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)


        self.sidebar = QFrame(); self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(220)
        s_layout = QVBoxLayout(self.sidebar)
        
        self.btn_raid = QPushButton(" ⚔  RAID "); self.btn_raid.setCheckable(True)
        self.btn_info = QPushButton(" 🔍  Server info"); self.btn_info.setCheckable(True)
        
        for b in [self.btn_raid, self.btn_info]:
            b.setObjectName("MenuBtn")
            s_layout.addWidget(b)
        
        self.btn_raid.setChecked(True)
        s_layout.addStretch()
        layout.addWidget(self.sidebar)


        self.pages = QStackedWidget()
        

        self.p_raid = QWidget(); l_raid = QVBoxLayout(self.p_raid)
        l_raid.setContentsMargins(30, 30, 30, 30)
        self.r_token = QLineEdit(placeholderText="[!] USER TOKEN")
        self.r_chan = QLineEdit(placeholderText="[!] Canal ID")
        self.r_msg = QLineEdit(placeholderText="[!] SPAM Mensaje")
        self.btn_exec_raid = QPushButton("Ejecutar", objectName="ActionBtn")
        self.btn_exec_raid.clicked.connect(self.start_raid)
        l_raid.addWidget(QLabel("Creado por t.me/Valen_Qq")); l_raid.addWidget(self.r_token)
        l_raid.addWidget(self.r_chan); l_raid.addWidget(self.r_msg)
        l_raid.addWidget(self.btn_exec_raid); l_raid.addStretch()


        self.p_info = QWidget(); l_info = QVBoxLayout(self.p_info)
        l_info.setContentsMargins(30, 30, 30, 30)
        self.i_inv = QLineEdit(placeholderText="[!] discord.gg/invitacion")
        self.btn_exec_info = QPushButton("Buscar", objectName="ActionBtn")
        self.btn_exec_info.clicked.connect(self.fetch_intel)
        l_info.addWidget(QLabel("Creado por t.me/Valen_Qq")); l_info.addWidget(self.i_inv)
        l_info.addWidget(self.btn_exec_info); l_info.addStretch()

        self.pages.addWidget(self.p_raid); self.pages.addWidget(self.p_info)
        layout.addWidget(self.pages)


        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setFixedWidth(500)
        layout.addWidget(self.console)

        self.btn_raid.clicked.connect(lambda: self.switch(0))
        self.btn_info.clicked.connect(lambda: self.switch(1))

    def switch(self, i):
        self.pages.setCurrentIndex(i)
        self.btn_raid.setChecked(i==0); self.btn_info.setChecked(i==1)

    def log_raw(self, key, value):

        self.console.append(f"<span style='color:#ffffff;'>[</span><span style='color:#FF0000;'>+</span><span style='color:#ffffff;'>]</span> <span style='color:#FF0000;'>{key:<30}:</span> <span style='color:#ffffff;'>{value}</span>")

    def fetch_intel(self):
        invite_input = self.i_inv.text().strip()
        code = invite_input.split("/")[-1]
        self.console.clear()
        self.console.append(f"<b style='color:#FF0000;'>--- INFORMACION ---</b><br>")

        try:
            r = requests.get(f"https://discord.com/api/v9/invites/{code}?with_counts=true&with_expiration=true")
            if r.status_code == 200:
                data = r.json()
                guild = data.get('guild', {})
                chan = data.get('channel', {})
                inviter = data.get('inviter', {})

 
                self.log_raw("Invitation", invite_input)
                self.log_raw("Tipo", data.get('type'))
                self.log_raw("Codigo", data.get('code'))
                self.log_raw("Expira", data.get('expires_at', 'Never'))
                self.log_raw("Servidor ID", guild.get('id'))
                self.log_raw("Servidor nombre", guild.get('name'))
                self.log_raw("Canal ID", chan.get('id'))
                self.log_raw("Canal Nombre", chan.get('name'))
                self.log_raw("Canal tipo", chan.get('type'))
                self.log_raw("Servidor icono", guild.get('icon'))
                self.log_raw("Caracteristicas del Servidor", ", ".join(guild.get('features', [])))
                self.log_raw("Servidor Nivel NSFW", guild.get('nsfw_level'))
                self.log_raw("Servidor NSFW", guild.get('nsfw'))
                self.log_raw("Banderas", data.get('flags'))
                self.log_raw("Nivel de verificación del servidor", guild.get('verification_level'))
                self.log_raw("Servidor de suscripción premium", guild.get('premium_subscription_count', 0))

                self.console.append(f"<br><b style='color:#FF0000;'>Informacion del invitador:</b>")
  
                self.log_raw("ID", inviter.get('id'))
                self.log_raw("Nombre de usuario", inviter.get('username'))
                self.log_raw("Nombre global", inviter.get('global_name'))
                self.log_raw("Avatar", inviter.get('avatar'))
                self.log_raw("Discriminador", inviter.get('discriminator'))
                self.log_raw("Banderas publicas", inviter.get('public_flags'))
                self.log_raw("Banderas", inviter.get('flags'))
                self.log_raw("Banner", inviter.get('banner'))
                self.log_raw("Acento color", inviter.get('accent_color'))
                self.log_raw("Banner Color", inviter.get('banner_color'))

            else:
                self.console.append(f"<span style='color:orange;'>[!] Error {r.status_code}: Invite expirada o inválida.</span>")
        except Exception as e:
            self.console.append(f"<span style='color:red;'>[X] Error Crítico: {e}</span>")

    def start_raid(self):
        token = self.r_token.text().strip()
        channel = self.r_chan.text().strip()
        message = self.r_msg.text()
        
        def run_raid():
            headers = {"Authorization": token, "Content-Type": "application/json"}
            while True:
                r = requests.post(f"https://discord.com/api/v9/channels/{channel}/messages", 
                                  headers=headers, json={"content": message})
                if r.status_code in [200, 201]:
                    self.console.append(f"<span style='color:#00FF00;'>[HIT] Sent to {channel}</span>")
                elif r.status_code == 429:
                    time.sleep(r.json().get('retry_after', 1))
                else:
                    self.console.append(f"<span style='color:#FF0000;'>[FAIL] {r.status_code}</span>")
                    break

        threading.Thread(target=run_raid, daemon=True).start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ZenCommander()
    window.show()
    sys.exit(app.exec())
