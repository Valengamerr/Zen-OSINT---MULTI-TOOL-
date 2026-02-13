# No se recomienda entrar a la darkweb
# Como entrar:  descarga TOR browser  en una maquina virtual con Anti virus y pega el link y listo
import sys
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QLabel, QPushButton, QFrame, QScrollArea, QGridLayout)
from PyQt6.QtGui import QFont, QColor, QIcon
from PyQt6.QtCore import Qt

class ZenLinkVault(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1150, 800)
        self.setWindowTitle("Zen OSINT - Dark web LINKS")
        

        self.database = {
            "DDOS ": [
                ("DDOSNOW", "https://ddosnow.com/"), ("STRESSER ZONE", "https://stresser.zone/"),
                ("STRESSE RU", "https://stresse.ru/"), ("STRESSE CAT", "https://stresse.cat/"),
                ("STARK STRESSER", "https://starkstresser.net/"), ("DDOS SERVICES", "https://ddos.services/")
            ],
            "IP LOGGERS": [
                ("IP LOGGER", "https://iplogger.org/"), ("GRABIFY LINK", "https://grabify.link/"),
                ("GRABIFY ICU", "https://grabify.icu/"), ("WHATS THEIR IP", "https://whatstheirip.tech/"),
                ("SPY LINK", "https://www.spylink.net/"), ("IP INFO", "https://ipinfo.io/")
            ],
            "OSINT / DOX / SEARCH": [
                ("DOXBIN", "https://doxbin.net/"), ("OSINT INDUSTRIES", "https://osint.industries"),
                ("EPIEOS", "https://epieos.com/"), ("NUWBER", "https://nuwber.fr/"),
                ("OSINT FRAMEWORK", "https://osintframework.com"), ("WHATS MY NAME", "https://whatsmyname.app/")
            ],
            "DARK WEB - Motores de busqueda": [
                ("TORCH", "http://xmh57jrknzkhv6y3ls3ubitzfqnkrwxhopf5aygthi7d6rplyvk3noyd.onion/"),
                ("DANEX", "http://danexio627wiswvlpt6ejyhpxl5gla5nt2tgvgm2apj2ofrgm44vbeyd.onion/"),
                ("SENTOR", "http://e27slbec2ykiyo26gfuovaehuzsydffbit5nlxid53kigw3pvz6uosqd.onion/")
            ],
            "DARK WEB - Cripto & Mercados": [
                ("DARK MIXER", "http://y22arit74fqnnc2pbieq3wqqvkfub6gnlegx3cl6thclos4f7ya7rvad.onion/"),
                ("MIXABIT", "http://hqfld5smkr4b4xrjcco7zotvoqhuuoehjdvoin755iytmpk4sm7cbwad.onion/"),
                ("EASYCOIN", "http://mp3fpv6xbrwka4skqliiifoizghfbjy5uyu77wwnfruwub5s4hly2oid.onion/"),
                ("DEEP MARKET", "http://deepmar4ai3iff7akeuos3u3727lvuutm4l5takh3dmo3pziznl5ywqd.onion/"),
                ("DATABASE LEAKS", "http://breachdbsztfykg2fdaq2gnqnxfsbj5d35byz3yzj73hazydk4vq72qd.onion/")
            ]
        }
        self.init_ui()

    def init_ui(self):

        self.setStyleSheet("""
            QWidget { background-color: #060609; color: #ffffff; font-family: 'Inter', 'Segoe UI'; }
            QLineEdit { 
                background: #0f0f15; border: 1px solid #1a1a25; border-radius: 12px; 
                padding: 18px; color: #A020F0; font-size: 15px; font-weight: bold;
            }
            QFrame#CategoryBox { background: #0a0a0f; border: 1px solid #14141c; border-radius: 15px; padding: 10px; }
            QFrame#LinkCard { background: #11111a; border-radius: 8px; border: 1px solid #1a1a25; }
            QFrame#LinkCard:hover { border: 1px solid #A020F0; background: #151522; }
            QLabel#CatTitle { color: #A020F0; font-size: 18px; font-weight: 800; margin-bottom: 10px; }
            QPushButton#CopyBtn { 
                background: #1a1a25; border: 1px solid #A020F0; border-radius: 6px; 
                color: #fff; font-size: 11px; font-weight: bold; 
            }
            QPushButton#CopyBtn:hover { background: #A020F0; }
            QScrollArea { border: none; background: transparent; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        

        header = QLabel("ZEN <span style='color:#A020F0;'>DarkWeb</span> Link")
        header.setFont(QFont("Arial Black", 36))
        layout.addWidget(header, alignment=Qt.AlignmentFlag.AlignCenter)
        

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("BUSCAR ENLACE O CATEGORIA (OSINT, DDOS, DARKWEB)...")
        self.search_bar.textChanged.connect(self.update_display)
        layout.addWidget(self.search_bar)


        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.container = QWidget()
        self.grid = QGridLayout(self.container)
        self.grid.setSpacing(25)
        
        self.scroll.setWidget(self.container)
        layout.addWidget(self.scroll)
        
        self.update_display()

    def update_display(self):

        for i in reversed(range(self.grid.count())): 
            widget = self.grid.itemAt(i).widget()
            if widget: widget.setParent(None)

        search_text = self.search_bar.text().lower()
        col, row = 0, 0

        for category, links in self.database.items():

            filtered_links = [l for l in links if search_text in l[0].lower() or search_text in category.lower()]
            if not filtered_links: continue


            cat_frame = QFrame()
            cat_frame.setObjectName("CategoryBox")
            cat_vbox = QVBoxLayout(cat_frame)
            
            cat_title = QLabel(category)
            cat_title.setObjectName("CatTitle")
            cat_vbox.addWidget(cat_title)

            for name, url in filtered_links:
                link_card = QFrame()
                link_card.setObjectName("LinkCard")
                link_card.setFixedHeight(50)
                link_h = QHBoxLayout(link_card)
                
                name_lbl = QLabel(f"<b>{name}</b>")
                name_lbl.setStyleSheet("font-size: 13px;")
                
                copy_btn = QPushButton("COPIAR")
                copy_btn.setObjectName("CopyBtn")
                copy_btn.setFixedSize(70, 28)
                copy_btn.clicked.connect(lambda ch, u=url: QApplication.clipboard().setText(u))
                
                link_h.addWidget(name_lbl)
                link_h.addStretch()
                link_h.addWidget(copy_btn)
                cat_vbox.addWidget(link_card)

            self.grid.addWidget(cat_frame, row, col)
            

            col += 1
            if col > 2:
                col = 0
                row += 1

    def copy_to_clipboard(self, text):
        QApplication.clipboard().setText(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ZenLinkVault()
    window.show()
    sys.exit(app.exec())
