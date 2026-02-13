import sys
import os
import requests
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLineEdit, QTextEdit, QLabel, QFrame)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap


ruta_script = os.path.abspath(__file__)
ruta_raiz = os.path.dirname(os.path.dirname(ruta_script))
if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)

class ScannerThread(QThread):
    resultado_sig = pyqtSignal(str, str) 
    finalizado_sig = pyqtSignal()

    def __init__(self, username):
        super().__init__()
        self.username = username

        self.sitios = {
            "Instagram": f"https://www.instagram.com/{username}",
            "Facebook": f"https://www.facebook.com/{username}",
            "Twitter": f"https://www.twitter.com/{username}",
            "YouTube": f"https://www.youtube.com/{username}",
            "GitHub": f"https://github.com/{username}",
            "Reddit": f"https://www.reddit.com/user/{username}",
            "Pinterest": f"https://www.pinterest.com/{username}",
            "Spotify": f"https://open.spotify.com/user/{username}",
            "Steam": f"https://steamcommunity.com/id/{username}",
            "Twitch": f"https://www.twitch.tv/{username}",
            "SoundCloud": f"https://soundcloud.com/{username}",
            "Vimeo": f"https://vimeo.com/{username}",
            "DailyMotion": f"https://www.dailymotion.com/{username}",
            "Medium": f"https://medium.com/@{username}",
            "Behance": f"https://www.behance.net/{username}",
            "Pastebin": f"https://pastebin.com/u/{username}",
            "TikTok": f"https://www.tiktok.com/@{username}",
            "LinkedIn": f"https://www.linkedin.com/in/{username}",
            "Snapchat": f"https://www.snapchat.com/add/{username}",
            "Telegram": f"https://t.me/{username}",
            "Discord": f"https://discord.com/users/{username}",
            "Flickr": f"https://www.flickr.com/people/{username}",
            "Tumblr": f"https://{username}.tumblr.com",
            "DeviantArt": f"https://www.deviantart.com/{username}",
            "Dribbble": f"https://dribbble.com/{username}",
            "Quora": f"https://www.quora.com/profile/{username}",
            "GitLab": f"https://gitlab.com/{username}",
            "Bitbucket": f"https://bitbucket.org/{username}",
            "Patreon": f"https://www.patreon.com/{username}",
            "Mastodon": f"https://mastodon.social/@{username}",
            "Letterboxd": f"https://letterboxd.com/{username}",
            "Goodreads": f"https://www.goodreads.com/{username}",
            "Last.fm": f"https://www.last.fm/user/{username}",
            "Roblox": f"https://www.roblox.com/user.aspx?username={username}",
            "CodePen": f"https://codepen.io/{username}",
            "Xbox": f"https://www.xboxgamertag.com/search/{username}",
            "Speedrun": f"https://www.speedrun.com/user/{username}",
            "Keybase": f"https://keybase.io/{username}",
            "HackerNews": f"https://news.ycombinator.com/user?id={username}",
            "ProductHunt": f"https://www.producthunt.com/@{username}",
            "DockerHub": f"https://hub.docker.com/u/{username}",
            "PyPi": f"https://pypi.org/user/{username}",
            "NPM": f"https://www.npmjs.com/~{username}",
            "Arduino": f"https://create.arduino.cc/projecthub/{username}",
            "Kaggle": f"https://www.kaggle.com/{username}",
            "Scratch": f"https://scratch.mit.edu/users/{username}",
            "Itch.io": f"https://{username}.itch.io",
            "Replit": f"https://replit.com/@{username}",
            "Chess.com": f"https://www.chess.com/member/{username}",
            "Gitee": f"https://gitee.com/{username}",
            "Launchpad": f"https://launchpad.net/~{username}",
            "SourceForge": f"https://sourceforge.net/u/{username}",
            "HackTheBox": f"https://www.hackthebox.eu/profile/{username}",
            "TryHackMe": f"https://tryhackme.com/p/{username}",
            "GeeksForGeeks": f"https://auth.geeksforgeeks.org/user/{username}",
            "Linktree": f"https://linktr.ee/{username}",
            "Strava": f"https://www.strava.com/athletes/{username}",
            "Duolingo": f"https://www.duolingo.com/profile/{username}",
            "MyFitnessPal": f"https://www.myfitnesspal.com/profile/{username}",
            "AllTrails": f"https://www.alltrails.com/members/{username}",
            "TripAdvisor": f"https://www.tripadvisor.com/Profile/{username}",
            "Trustpilot": f"https://www.trustpilot.com/users/{username}",
            "Disqus": f"https://disqus.com/by/{username}",
            "SlideShare": f"https://www.slideshare.net/{username}",
            "Freelancer": f"https://www.freelancer.com/u/{username}",
            "Fiverr": f"https://www.fiverr.com/{username}",
            "Upwork": f"https://www.upwork.com/freelancers/~{username}",
            "Gumroad": f"https://{username}.gumroad.com",
            "Contently": f"https://{username}.contently.com",
            "AboutMe": f"https://about.me/{username}",
            "EyeEm": f"https://www.eyeem.com/u/{username}",
            "Canva": f"https://www.canva.com/{username}",
            "VK": f"https://vk.com/{username}",
            "OK.ru": f"https://ok.ru/{username}",
            "Weibo": f"https://weibo.com/{username}",
            "Taringa": f"https://www.taringa.net/{username}",
            "Xing": f"https://www.xing.com/profile/{username}",
            "Skyrock": f"https://{username}.skyrock.com",
            "LiveJournal": f"https://{username}.livejournal.com",
            "Bandcamp": f"https://bandcamp.com/{username}",
            "Mixcloud": f"https://www.mixcloud.com/{username}",
            "ReverbNation": f"https://www.reverbnation.com/{username}",
            "Discogs": f"https://www.discogs.com/user/{username}",
            "Giphy": f"https://giphy.com/{username}",
            "Imgur": f"https://imgur.com/user/{username}",
            "Instructables": f"https://www.instructables.com/member/{username}",
            "Etsy": f"https://www.etsy.com/people/{username}",
            "Grailed": f"https://www.grailed.com/{username}",
            "Poshmark": f"https://poshmark.com/closet/{username}",
            "eBay": f"https://www.ebay.com/usr/{username}",
            "Amazon": f"https://www.amazon.com/gp/profile/amzn1.account.{username}",
            "Yelp": f"https://www.yelp.com/user_details?userid={username}",
            "OpenTable": f"https://www.opentable.com/user/{username}",
            "Zomato": f"https://www.zomato.com/{username}",
            "Poshmark": f"https://poshmark.com/closet/{username}",
            "Depop": f"https://www.depop.com/{username}",
            "Mercari": f"https://www.mercari.com/u/{username}",
            "HackerRank": f"https://www.hackerrank.com/{username}",
            "LeetCode": f"https://leetcode.com/{username}",
            "Codechef": f"https://www.codechef.com/users/{username}",
            "Topcoder": f"https://www.topcoder.com/members/{username}",
            "Codewars": f"https://www.codewars.com/users/{username}",
            "Dev.to": f"https://dev.to/{username}",
            "Hashnode": f"https://hashnode.com/@{username}",
            "SpeakerDeck": f"https://speakerdeck.com/{username}",
            "MyAnimeList": f"https://myanimelist.net/profile/{username}",
            "AniList": f"https://anilist.co/user/{username}",
            "Trakt": f"https://trakt.tv/users/{username}",
            "RateYourMusic": f"https://rateyourmusic.com/~{username}",
            "Genius": f"https://genius.com/{username}",
            "Wattpad": f"https://www.wattpad.com/user/{username}",
            "Archive.org": f"https://archive.org/details/@{username}",
            "Komoot": f"https://www.komoot.com/user/{username}",
            "Garmin": f"https://connect.garmin.com/modern/profile/{username}",
            "Geocaching": f"https://www.geocaching.com/p/default.aspx?u={username}",
            "Fitbit": f"https://www.fitbit.com/user/{username}",
            "500px": f"https://500px.com/p/{username}",
            "GuruShots": f"https://gurushots.com/{username}/photos",
            "PhotoBlog": f"https://www.photoblog.com/{username}",
            "Vsco": f"https://vsco.co/{username}/gallery",
            "Linktree": f"https://linktr.ee/{username}",
            "Carrd": f"https://{username}.carrd.co",
            "About.me": f"https://about.me/{username}",
            "Bento.me": f"https://bento.me/{username}",
            "BuyMeACoffee": f"https://www.buymeacoffee.com/{username}",
            "Ko-fi": f"https://ko-fi.com/{username}",
            "Kiva": f"https://www.kiva.org/lender/{username}",
            "SlideShare": f"https://www.slideshare.net/{username}",
            "Scribd": f"https://www.scribd.com/{username}",
            "Issuu": f"https://issuu.com/{username}",
        }

    def run(self):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        for nombre, url in self.sitios.items():
            try:
                # Usamos requests para mayor velocidad (como el curl del script original)
                response = requests.get(url, headers=headers, timeout=5, allow_redirects=True)
                if response.status_code == 200:
                    # Algunas redes devuelven 200 pero dicen "Usuario no encontrado" en el texto
                    if "not found" in response.text.lower() or "doesn't exist" in response.text.lower():
                        self.resultado_sig.emit(nombre, None)
                    else:
                        self.resultado_sig.emit(nombre, url)
                else:
                    self.resultado_sig.emit(nombre, None)
            except:
                self.resultado_sig.emit(nombre, "Error")
        self.finalizado_sig.emit()

class UsernameTrackerUI(QWidget):
    def __init__(self):
        super().__init__()
        self.ruta_iconos = os.path.join(ruta_raiz, "Iconos")
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Zen OSINT - Username Tracker | Valen_Qq")
        self.setFixedSize(650, 650)
        self.setStyleSheet("""
            QWidget { background-color: #050505; color: #e0e0e0; font-family: 'Segoe UI'; }
            #input_frame { background-color: #0d0d0f; border: 1px solid #1c1c1e; border-radius: 10px; min-height: 48px; }
            #input_frame:focus-within { border: 1px solid #A020F0; }
            QLineEdit { background-color: transparent; border: none; color: #ffffff; font-size: 14px; }
            QTextEdit { background-color: #08080a; border: 1px solid #1a1a1c; border-radius: 10px; color: #ffffff; font-family: 'Consolas', monospace; padding: 15px; }
            QLabel#header { font-size: 22px; font-weight: 900; color: white; }
            QLabel#credits { color: #555; font-size: 11px; font-weight: bold; }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 30, 35, 20)

        header = QLabel("USERNAME TRACKER SCANNER")
        header.setObjectName("header")
        layout.addWidget(header)

        # Input con Icono (Usaremos el de Email.svg o podrías crear uno User.svg)
        self.input_frame = QFrame(objectName="input_frame")
        input_inner = QHBoxLayout(self.input_frame)
        self.icon_label = QLabel()
        path_icon = os.path.join(self.ruta_iconos, "Usuario.svg") # O el que prefieras
        if os.path.exists(path_icon):
            self.icon_label.setPixmap(QPixmap(path_icon).scaled(20, 20, Qt.AspectRatioMode.KeepAspectRatio))
        
        self.input_user = QLineEdit()
        self.input_user.setPlaceholderText("Introduce el nombre de usuario y pulsa Enter...")
        self.input_user.returnPressed.connect(self.iniciar_escaneo)
        input_inner.addWidget(self.icon_label)
        input_inner.addWidget(self.input_user)
        layout.addWidget(self.input_frame)

        self.console = QTextEdit()
        self.console.setReadOnly(True)
        layout.addWidget(self.console)

        credits = QLabel("Zen OSINT creado por Valen_Qq")
        credits.setObjectName("credits")
        layout.addWidget(credits, alignment=Qt.AlignmentFlag.AlignRight)

    def log(self, text, color="white"):
        self.console.append(f"<span style='color:{color};'>{text}</span>")

    def iniciar_escaneo(self):
        user = self.input_user.text().strip()
        if not user: return
        
        self.console.clear()
        self.log(f"[~] Rastreando usuario: {user} en múltiples redes...", "#A020F0")
        
        self.thread = ScannerThread(user)
        self.thread.resultado_sig.connect(self.mostrar_resultado)
        self.thread.finalizado_sig.connect(lambda: self.log("\n[!] Escaneo completado.", "#A020F0"))
        self.thread.start()

    def mostrar_resultado(self, nombre, url):
        if url == "Error":
            self.log(f"[!] {nombre}: Error de conexión", "orange")
        elif url:
            self.log(f"[+] {nombre}: ENCONTRADO -> {url}", "#00ff00")
        else:
            self.log(f"[-] {nombre}: No encontrado", "#555")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UsernameTrackerUI()
    window.show()
    sys.exit(app.exec())
