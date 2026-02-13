import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QFrame
from PyQt6.QtCore import Qt, QTimer

class InfoValen(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 400)
        self.setWindowTitle("DATOS DEL CREADOR")
        self.posicion_x = -300
        self.armar_ventana()

    def armar_ventana(self):
        self.setStyleSheet("""
            QWidget { 
                background-color: #020205; 
                color: #ffffff; 
                font-family: 'Consolas', monospace; 
            }
            #CajaMovil {
                background-color: #050510;
                border-bottom: 2px solid #00d4ff;
                padding: 10px;
            }
            #TextoBrillante {
                color: #00ffaa;
                font-size: 16px;
                font-weight: bold;
            }
            #CajaDatos {
                background: #0a0a15;
                border: 1px solid #1a1a30;
                border-radius: 15px;
                margin: 20px;
                padding: 30px;
            }
            #EtiquetaRedes {
                font-size: 20px;
                margin-bottom: 10px;
            }
            #ValorRedes {
                color: #00d4ff;
                font-size: 22px;
                font-weight: bold;
                margin-bottom: 20px;
            }
        """)

        layout_total = QVBoxLayout(self)
        layout_total.setContentsMargins(0, 0, 0, 0)

        self.marco_movil = QFrame()
        self.marco_movil.setObjectName("CajaMovil")
        self.marco_movil.setFixedHeight(50)
        
        self.texto_marquesina = QLabel("Creado por t.me/Valen_Qq en 2026", self.marco_movil)
        self.texto_marquesina.setObjectName("TextoBrillante")
        self.texto_marquesina.adjustSize()
        self.texto_marquesina.move(self.posicion_x, 15)

        self.cuerpo_info = QFrame()
        self.cuerpo_info.setObjectName("CajaDatos")
        layout_cuerpo = QVBoxLayout(self.cuerpo_info)
        layout_cuerpo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        git_titulo = QLabel("Github:")
        git_titulo.setObjectName("EtiquetaRedes")
        git_valor = QLabel("Valengamerr")
        git_valor.setObjectName("ValorRedes")

        tele_titulo = QLabel("Telegram:")
        tele_titulo.setObjectName("EtiquetaRedes")
        tele_valor = QLabel("Valen_Qq")
        tele_valor.setObjectName("ValorRedes")

        layout_cuerpo.addWidget(git_titulo)
        layout_cuerpo.addWidget(git_valor)
        layout_cuerpo.addWidget(tele_titulo)
        layout_cuerpo.addWidget(tele_valor)

        layout_total.addWidget(self.marco_movil)
        layout_total.addWidget(self.cuerpo_info)

        self.reloj = QTimer()
        self.reloj.timeout.connect(self.mover_texto)
        self.reloj.start(10)

    def mover_texto(self):
        self.posicion_x += 2
        if self.posicion_x > self.width():
            self.posicion_x = -350
        self.texto_marquesina.move(self.posicion_x, 15)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = InfoValen()
    ventana.show()
    sys.exit(app.exec())
