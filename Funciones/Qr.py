import sys
import os
import qrcode
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QLabel, QPushButton, QFileDialog, QFrame)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

os.environ["QT_LOGGING_RULES"] = "*=false"

class ZenQRGeneratorV19(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(650, 850)
        self.setWindowTitle("Zen QR Generator V19")
        self.setStyleSheet("background-color: #050505; color: #e0e0e0; font-family: monospace;")
        
        self.path_iconos = os.path.join(os.getcwd(), "Iconos")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(15)


        layout.addWidget(QLabel("Creado por t.me/Valen_Qq"))
        row_data = QHBoxLayout()
        self.ico_qr = QLabel()
        self.ico_qr.setPixmap(QPixmap(os.path.join(self.path_iconos, "Qr.svg")).scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        
        self.input_data = QLineEdit()
        self.input_data.setPlaceholderText("https://qr.com/...")
        self.input_data.setStyleSheet("background:#111; border:1px solid #333; padding:12px; color:white;")
        row_data.addWidget(self.ico_qr)
        row_data.addWidget(self.input_data)
        layout.addLayout(row_data)


        layout.addWidget(QLabel(""))
        row_folder = QHBoxLayout()
        self.ico_folder = QLabel()
        self.ico_folder.setPixmap(QPixmap(os.path.join(self.path_iconos, "Carpeta_destino.svg")).scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        
        self.input_folder = QLineEdit()
        self.input_folder.setPlaceholderText("Carpeta donde se guardara el codigo qr (RUTA)")
        self.input_folder.setStyleSheet("background:#111; border:1px solid #333; padding:12px; color:white;")
        
        self.btn_browse = QPushButton("BROWSE")
        self.btn_browse.setStyleSheet("background:#333; color:white; padding:12px; font-weight:bold; border:1px solid #555;")
        self.btn_browse.clicked.connect(self.get_folder)
        
        row_folder.addWidget(self.ico_folder)
        row_folder.addWidget(self.input_folder)
        row_folder.addWidget(self.btn_browse)
        layout.addLayout(row_folder)


        layout.addWidget(QLabel(""))
        row_filename = QHBoxLayout()
        self.ico_file = QLabel()
        self.ico_file.setPixmap(QPixmap(os.path.join(self.path_iconos, "Archivo_qr.svg")).scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        
        self.input_filename = QLineEdit()
        self.input_filename.setPlaceholderText("ej: mi_codigo_especial")
        self.input_filename.setStyleSheet("background:#111; border:1px solid #333; padding:12px; color:white;")
        row_filename.addWidget(self.ico_file)
        row_filename.addWidget(self.input_filename)
        layout.addLayout(row_filename)


        self.btn_generate = QPushButton("GENERAR Y GUARDAR QR")
        self.btn_generate.setStyleSheet("background:#A020F0; color:white; font-weight:bold; padding:20px; border-radius:0px; margin-top:10px;")
        self.btn_generate.clicked.connect(self.generate_qr)
        layout.addWidget(self.btn_generate)


        self.preview_box = QFrame()
        self.preview_box.setFixedSize(320, 320)
        self.preview_box.setStyleSheet("background:#000; border:2px solid #111; margin-top:20px;")
        p_layout = QVBoxLayout(self.preview_box)
        
        self.preview_label = QLabel("SIN PREVIEW")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setStyleSheet("color:#333; font-weight:bold; border:none;")
        p_layout.addWidget(self.preview_label)
        
        layout.addWidget(self.preview_box, alignment=Qt.AlignmentFlag.AlignCenter)

    def get_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Seleccionar Carpeta")
        if folder:
            self.input_folder.setText(folder)

    def generate_qr(self):
        data = self.input_data.text().strip()
        folder = self.input_folder.text().strip()
        name = self.input_filename.text().strip()

        if not data or not folder or not name:
            self.preview_label.setText("FALTAN DATOS")
            return


        if not name.lower().endswith(".png"):
            name += ".png"
        
        full_path = os.path.join(folder, name)

        try:
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")
            img.save(full_path)


            pix = QPixmap(full_path)
            self.preview_label.setPixmap(pix.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio))
        except Exception as e:
            self.preview_label.setText(f"ERROR: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ZenQRGeneratorV19()
    win.show()
    sys.exit(app.exec())
