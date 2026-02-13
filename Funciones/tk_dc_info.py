# TIP : No compartas tu TOKEN de discord a nadie.
import sys
import os
import requests
from datetime import datetime, timezone
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QLabel, QPushButton, QTextEdit)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

os.environ["QT_LOGGING_RULES"] = "*=false"

class ZenDiscordV33(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(900, 900)
        self.setWindowTitle("Zen OSINT - Creado por t.me/Valen_Qq  | Zo V1 |")
        self.setStyleSheet("background-color: #050505; color: #e0e0e0; font-family: monospace;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)


        header = QLabel("Extraer info de un token de DC.")
        header.setStyleSheet("color: #A020F0; font-size: 22px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(header, alignment=Qt.AlignmentFlag.AlignCenter)


        layout.addWidget(QLabel("PEGA EL TOKEN AQUÍ:"))
        self.token_input = QLineEdit()
        self.token_input.setPlaceholderText("wlll2hkA0jTkzm9yzoTc4zTIwNf...")
        self.token_input.setStyleSheet("background: #111; border: 1px solid #333; padding: 15px; color: #FFA07A; font-size: 14px;")
        layout.addWidget(self.token_input)


        self.btn_fetch = QPushButton(" ANALIZAR TOKEN")

        icon_path = "Iconos/Decode.svg"
        if os.path.exists(icon_path): self.btn_fetch.setIcon(QIcon(icon_path))
        
        self.btn_fetch.setStyleSheet("""
            QPushButton {
                background: #111; border: 1px solid #A020F0; padding: 20px; 
                color: white; font-weight: bold; margin-top: 10px; font-size: 16px;
            }
            QPushButton:hover { background: #A020F0; }
        """)
        self.btn_fetch.clicked.connect(self.run_full_osint)
        layout.addWidget(self.btn_fetch)


        layout.addWidget(QLabel("LOG DE INFORMACIÓN RECOLECTADA:"))
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("""
            background: #000; 
            border: 1px solid #222; 
            color: #ffffff; 
            padding: 15px; 
            font-size: 13px;
        """)
        layout.addWidget(self.log_output)

    def log(self, text):
        self.log_output.append(text)

    def run_full_osint(self):
        token = self.token_input.text().strip()
        if not token: return
        
        self.log_output.clear()
        headers = {'Authorization': token, 'Content-Type': 'application/json'}
        
        try:

            res = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
            if res.status_code != 200:
                self.log("<span style='color:red;'>[!] TOKEN INVÁLIDO</span>")
                return
            
            user = res.json()
            u_id = user.get('id', 'None')
            status = "Valido"
            

            premium = user.get('premium_type', 0)
            nitro = {0: 'Falso', 1: 'Nitro Classic', 2: 'Nitro Boosts', 3: 'Nitro Basic'}.get(premium, 'Falso')
            

            created = datetime.fromtimestamp(((int(u_id) >> 22) + 1420070400000) / 1000, timezone.utc)
            

            billing = requests.get('https://discord.com/api/v9/users/@me/billing/payment-sources', headers=headers).json()
            methods = ' / '.join(["CB" if m['type']==1 else "Paypal" if m['type']==2 else "Otro" for m in billing]) if billing else "Ninguno"


            guilds = requests.get('https://discord.com/api/v9/users/@me/guilds?with_counts=true', headers=headers).json()
            guild_count = len(guilds) if isinstance(guilds, list) else "0"
            owner_guilds = [f"{g['name']} ({g['id']})" for g in guilds if g['owner']] if isinstance(guilds, list) else []
            

            friends_req = requests.get('https://discord.com/api/v9/users/@me/relationships', headers=headers).json()
            friends = ' / '.join([f"{f['user']['username']}#{f['user']['discriminator']}" for f in friends_req[:10]]) if isinstance(friends_req, list) else "Ninguno"


            r, w = "#FF0000", "#FFFFFF" 
            
            def fmt(label, value):
                return f"<span style='color:{w};'>[</span><span style='color:{r};'>+</span><span style='color:{w};'>]</span> <span style='color:{r};'>{label} :</span> <span style='color:{w};'>{value}</span>"

            self.log(fmt("Estado", status))
            self.log(fmt("Token", token))
            self.log(fmt("Usuario", f"{user.get('username')}#{user.get('discriminator')}"))
            self.log(fmt("Nombre Visible", user.get('global_name', 'None')))
            self.log(fmt("ID", u_id))
            self.log(fmt("Creado", created.strftime('%d/%m/%Y %H:%M:%S')))
            self.log(fmt("Pais", user.get('locale', 'None')))
            self.log(fmt("Email", user.get('email', 'None')))
            self.log(fmt("Verificado", user.get('verified', 'None')))
            self.log(fmt("Telefono", user.get('phone', 'None')))
            self.log(fmt("Nitro", nitro))
            self.log(fmt("MFA (2FA)", user.get('mfa_enabled', 'None')))
            self.log(fmt("Facturación", methods))
            self.log(fmt("Servidores", guild_count))
            self.log(fmt("Dueño de", f"({len(owner_guilds)}) " + " / ".join(owner_guilds) if owner_guilds else "Ninguno"))
            self.log(fmt("Bio", user.get('bio', 'None').strip() or "Ninguna"))
            self.log(fmt("Amigos (Top 10)", friends))
            self.log(fmt("Avatar URL", f"https://cdn.discordapp.com/avatars/{u_id}/{user.get('avatar')}.png"))

        except Exception as e:
            self.log(f"<span style='color:red;'>[!] Error: {str(e)}</span>")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ZenDiscordV33()
    win.show()
    sys.exit(app.exec())
