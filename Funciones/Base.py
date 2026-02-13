import sys
import os
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QTextEdit, QPushButton, QLabel, QDialog)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

os.environ["QT_LOGGING_RULES"] = "*=false"


RAW_KEY = b'\x16\x1b\x1f\x1d\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x20\x21\x22\x23\x24\x25\x26\x27\x28'

class ResultWindow(QDialog):
    def __init__(self, title, content):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(850, 650)
        self.setStyleSheet("background-color: #050505; color: #FFA07A;")
        layout = QVBoxLayout(self)
        
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlainText(content)
        self.output.setStyleSheet("border: 1px solid #A020F0; background: #000; padding: 20px; font-family: monospace; font-size: 14px;")
        layout.addWidget(self.output)
        
        btn_copy = QPushButton("COPIAR Y CERRAR")
        btn_copy.clicked.connect(self.copy_and_exit)
        btn_copy.setStyleSheet("background: #A020F0; color: white; padding: 15px; font-weight: bold; border: none;")
        layout.addWidget(btn_copy)

    def copy_and_exit(self):
        self.output.selectAll()
        self.output.copy()
        self.close()

class ZenAES(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(950, 850)
        self.setWindowTitle("Zen AES Engine V30")
        self.setStyleSheet("background-color: #050505; color: #e0e0e0; font-family: monospace;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)


        btn_layout = QHBoxLayout()
        

        self.btn_decode = self.create_btn("Iconos/Decode.svg", "DECODIFICAR")
        self.btn_encode = self.create_btn("Iconos/Cod.svg", "CODIFICAR")
        self.btn_aes = self.create_btn("Iconos/Xor.svg", "AES-256 PURE")
        
        btn_layout.addWidget(self.btn_decode)
        btn_layout.addWidget(self.btn_encode)
        btn_layout.addWidget(self.btn_aes)
        layout.addLayout(btn_layout)


        layout.addWidget(QLabel("STREAM DE DATOS:"))
        self.main_input = QTextEdit()
        self.main_input.setPlaceholderText("Pegue aquí el contenido...")
        self.main_input.setStyleSheet("""
            background: #080808; 
            border: 1px solid #222; 
            padding: 20px; 
            color: #e0e0e0; 
            font-size: 15px;
        """)
        layout.addWidget(self.main_input)


        self.btn_decode.clicked.connect(self.process_decode)
        self.btn_encode.clicked.connect(self.process_encode)
        self.btn_aes.clicked.connect(self.process_aes)

    def create_btn(self, path, text):
        btn = QPushButton(f" {text}")
        if os.path.exists(path):
            btn.setIcon(QIcon(path))
        btn.setStyleSheet("""
            QPushButton {
                background: #111; 
                border: 1px solid #A020F0; 
                padding: 20px; 
                color: white; 
                font-weight: bold;
            }
            QPushButton:hover { background: #A020F0; }
        """)
        return btn

    def process_aes(self):
        try:
            data = self.main_input.toPlainText().strip()

            cipher = AES.new(RAW_KEY, AES.MODE_CBC)
            ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))

            res = base64.b64encode(cipher.iv + ct_bytes).decode('utf-8')
            self.show_dialog("AES ENCRYPTED", res)
        except Exception as e:
            self.show_dialog("ERROR", str(e))

    def process_decode(self):
        try:
            data = self.main_input.toPlainText().strip()
            raw = base64.b64decode(data)
            

            if len(raw) >= 32:
                try:
                    iv, ct = raw[:16], raw[16:]
                    cipher = AES.new(RAW_KEY, AES.MODE_CBC, iv)
                    res = unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')
                    self.show_dialog("AES DECRYPTED", res)
                    return
                except: pass
            

            res = raw.decode('utf-8')
            self.show_dialog("BASE64 DECODED", res)
        except:
            self.show_dialog("ERROR", "Data corrupta o formato no reconocido.")

    def process_encode(self):
        try:
            data = self.main_input.toPlainText().strip()
            res = base64.b64encode(data.encode('utf-8')).decode('utf-8')
            self.show_dialog("BASE64 ENCODED", res)
        except Exception as e:
            self.show_dialog("ERROR", str(e))

    def show_dialog(self, title, content):
        win = ResultWindow(title, content)
        win.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ZenAES()
    win.show()
    sys.exit(app.exec())
