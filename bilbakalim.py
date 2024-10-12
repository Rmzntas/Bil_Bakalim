from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QLineEdit
from PyQt5.QtGui import QPixmap, QPalette
from PyQt5.QtCore import Qt
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtCore import QTimer, QEventLoop

import settings
import pandas as pd
import random
import time
import datetime


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager



kullanici_adi = "asartepe"
sifre = "4444"


class MyWindow(QMainWindow):

    def wait(self, milliseconds):
        loop = QEventLoop()
        QTimer.singleShot(milliseconds, loop.quit)
        loop.exec_()

    def __init__(self):
        super().__init__()
        uic.loadUi("design.ui", self)  # .ui dosyasını yükler
        self.showFullScreen()


        ###### VARIABLES ######

        self.giris_ekrani : QWidget
        self.bitis : QWidget
        self.son_karar_ekrani : QWidget

        self.giris_asartepe : QLabel
        self.giris_bil_bakalim : QLabel
        self.button_giris : QPushButton
        self.hatali_giris : QLabel
        self.line_username : QLineEdit
        self.line_password : QLineEdit
        self.button_giris_basla : QPushButton



        self.bil_bakalim : QLabel 
        self.asartepe : QLabel
        self.label_50 : QLabel
        self.label_seyirci : QLabel
        self.label_2x : QLabel
        self.label_soru_no : QLabel
        self.label_soru : QLabel
        self.label_a : QLabel
        self.button_a : QPushButton
        self.label_b : QLabel
        self.button_b : QPushButton
        self.label_c : QLabel
        self.button_c : QPushButton
        self.label_d : QLabel
        self.button_d : QPushButton
        self.label_zaman : QLabel
        self.label_soru_no_text : QLabel
        self.label_soru_text : QLabel

        self.button_50 : QPushButton
        self.button_seyirci : QPushButton
        self.button_2x : QPushButton

        self.label_qr : QLabel


        self.button_evet : QPushButton
        self.button_hayir : QPushButton
        self.son_karar_ekrani.hide()

        self.label_next : QLabel
        self.label_next.hide()
        self.button_next : QPushButton
        self.button_next.hide()


        
        self.button_anamenu : QPushButton
        self.button_exit : QPushButton
        self.label_kaybet : QLabel
        self.label_kazan : QLabel
        self.label_kaybet.hide()
        self.label_kazan.hide()
        self.label_odul_miktari : QLabel

        self.bitis.hide()

        self.label_soru_text.setWordWrap(True)

        self.islost = False

        self.all_kolay_sorular = []
        self.all_orta_sorular = []
        self.all_zor_sorular = []


        self.kolay_sorular = []
        self.orta_sorular = []
        self.zor_sorular = []

        self.current_soru = 1

        self.flag_seyirci = False
        self.flag_2x = False
        self.flag_hazir = False
        self.flag_iscorrect = False

        self.key_flag = False

        self.gri_odul_style = "border-radius: 15px;color: red; padding: 10px; font-size: 30px; background-color: grey;"
        self.odul_style = "background-color: #92d14f; border-radius: 15px; padding: 10px; color: white; font-size: 30px;"
        self.baraj_style = "background-color: rgb(255, 192, 0); border-radius: 15px;color: red; padding: 10px; font-size: 30px;"


        ###### sesler ######
        self.cevap_sesi = QMediaPlayer()
        self.cevap_sesi.setMedia(QMediaContent(QUrl.fromLocalFile('src/cevap.mp3')))

        self.yanlis_sesi = QMediaPlayer()
        self.yanlis_sesi.setMedia(QMediaContent(QUrl.fromLocalFile('src/yanlış.mp3')))

        self.dogru_sesi = QMediaPlayer()
        self.dogru_sesi.setMedia(QMediaContent(QUrl.fromLocalFile('src/dogru.mp3')))

        self._25_saniye_sesi = QMediaPlayer()
        self._25_saniye_sesi.setMedia(QMediaContent(QUrl.fromLocalFile('src/25_saniye.mp3')))
        
        self._60_saniye_sesi = QMediaPlayer()
        self._60_saniye_sesi.setMedia(QMediaContent(QUrl.fromLocalFile('src/60_saniye.mp3')))

        self.soru_sesi = QMediaPlayer()
        self.soru_sesi.setMedia(QMediaContent(QUrl.fromLocalFile('src/soru.mp3')))



        #set soru_no
        pixmap = QPixmap('src/soru_numarası.png')
        self.label_soru_no.setPixmap(pixmap)

        #set soru
        pixmap = QPixmap('src/soru.png')
        print(pixmap.width(), pixmap.height())
        self.label_soru.resize(pixmap.width(), pixmap.height())
        self.label_soru.setPixmap(pixmap)

        #set şık kutuları
        pixmap = QPixmap('src/şık_kutusu.png')
        self.label_a.resize(pixmap.width(), pixmap.height())
        self.label_a.setPixmap(pixmap)
        self.label_b.resize(pixmap.width(), pixmap.height())
        self.label_b.setPixmap(pixmap)
        self.label_c.resize(pixmap.width(), pixmap.height())
        self.label_c.setPixmap(pixmap)
        self.label_d.resize(pixmap.width(), pixmap.height())
        self.label_d.setPixmap(pixmap)

        # set qr
        pixmap = QPixmap('src/qr.png')
        pixmap = pixmap.scaled(560, 560)
        self.label_qr.setPixmap(pixmap)
        self.label_qr.resize(pixmap.width(), pixmap.height())
        self.label_qr.hide()
        


        self.set_giris_sayfası()
        self.enable_for_last_choice()
        self.connect_buttons()


    


    def set_giris_sayfası(self):

        self.hatali_giris.hide()
        self.button_giris_basla.hide()
        ##set asartepe foto
        pixmap = QPixmap('src/Asartepe.png')
        pixmap = pixmap.scaled(500, 500)
        self.giris_asartepe.resize(pixmap.width(), pixmap.height())
        self.giris_asartepe.setPixmap(pixmap)
        ##set bilbakalım foto
        pixmap = QPixmap('src/1.png')
        pixmap = pixmap.scaled(500, 500)
        self.giris_bil_bakalim.resize(pixmap.width(), pixmap.height())
        self.giris_bil_bakalim.setPixmap(pixmap)
        

        self.button_giris.clicked.connect(self.giris_kontrol)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_1:
            self.button_a.click()
        elif event.key() == Qt.Key_2:
            self.button_b.click()
        elif event.key() == Qt.Key_3:
            self.button_c.click()
        elif event.key() == Qt.Key_4:
            self.button_d.click()
        elif event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.button_evet.click()
        elif event.key() == Qt.Key_Escape:
            self.button_hayir.click()
        elif event.key() == Qt.Key_A:
            self.button_50.click()
        elif event.key() == Qt.Key_S:
            self.button_seyirci.click()
        elif event.key() == Qt.Key_D:
            self.button_2x.click()
        elif event.key() == Qt.Key_N:
            self.button_next.click()

    def giris_kontrol(self):
        username = self.line_username.text()
        password = self.line_password.text()
        if username == kullanici_adi and password == sifre:
            self.set_soru_sayfası()
            self.button_giris_basla.show()
            self.key_flag = True
            self.button_giris_basla.clicked.connect(self.basla)  # Butona tıklandığında basla fonksiyonunu çalıştır

        else:
            self.hatali_giris.show()
            self.line_username.clear()
            self.line_password.clear()

    def basla(self):
        self.label_a.hide()
        self.label_b.hide()
        self.label_c.hide()
        self.label_d.hide()
        self.label_soru_no.hide()
        self.label_soru.hide()
        self.label_zaman.hide()
        self.label_soru_no_text.hide()
        self.label_soru_text.hide()
        self.button_a.hide()
        self.button_b.hide()
        self.button_c.hide()
        self.button_d.hide()
        self.giris_ekrani.hide()
        self.get_all_questions()
        self.set_soru_sayfası()
        self.label_kaybet.hide()
        self.label_kazan.hide()

        #jokerler
        self.label_50.setEnabled(True)
        self.button_50.show()
        self.label_2x.setEnabled(True)
        self.button_2x.show()
        self.label_seyirci.setEnabled(True)
        self.button_seyirci.show()

        self.label_kazan.hide()
        self.bitis.hide()

        self.islost = False
        self.current_soru = 1


        QTimer.singleShot(10, self.start_soru)

        


    def start_soru(self):
        self.soru_sesi.play()

        self.label_a.hide()
        self.label_b.hide()
        self.label_c.hide()
        self.label_d.hide()
        self.label_soru_no.hide()
        self.label_soru.hide()
        self.label_zaman.hide()
        self.label_soru_no_text.hide()
        self.label_soru_text.hide()
        self.button_a.hide()
        self.button_b.hide()
        self.button_c.hide()
        self.button_d.hide()

        self.label_next.hide()
        self.button_next.hide()

        self.enable_for_last_choice()

        self.flag_iscorrect = False

        self.label_a.setPixmap(QPixmap('src/şık_kutusu.png'))
        self.label_b.setPixmap(QPixmap('src/şık_kutusu.png'))
        self.label_c.setPixmap(QPixmap('src/şık_kutusu.png'))
        self.label_d.setPixmap(QPixmap('src/şık_kutusu.png'))
        
        self.wait(5500)
        
        self.label_soru_no.show()
        self.set_soru_no(self.current_soru)
        self.label_soru_no_text.show()
        
        self.set_soru()

        self.label_zaman.show()
        self.zamanlayici()

        


    def set_soru_sayfası(self):
        ### set bilbakalım foto
        pixmap = QPixmap('src/2.png')
        pixmap = pixmap.scaled(int(pixmap.width()*0.5), int(pixmap.height()*0.5))
        print(pixmap.width(), pixmap.height())
        self.bil_bakalim.resize(pixmap.width(), pixmap.height())
        self.bil_bakalim.setPixmap(pixmap)

        ### set asartepe foto
        pixmap = QPixmap('src/Asartepe.png')
        pixmap = pixmap.scaled(int(pixmap.width()*0.15), int(pixmap.height()*0.15))
        print(pixmap.width(), pixmap.height())
        self.asartepe.resize(pixmap.width(), pixmap.height())
        self.asartepe.setPixmap(pixmap)

        #set 2x joker
        pixmap = QPixmap('src/2x.png')
        pixmap = pixmap.scaled(120,120)
        self.label_2x.resize(pixmap.width(), pixmap.height())
        self.label_2x.setPixmap(pixmap)

        #set 50 joker
        pixmap = QPixmap('src/50.png')
        pixmap = pixmap.scaled(120,120)
        self.label_50.resize(pixmap.width(), pixmap.height())
        self.label_50.setPixmap(pixmap)

        #set seyirci joker
        pixmap = QPixmap('src/seyirci.png')
        pixmap = pixmap.scaled(120,120)
        self.label_seyirci.resize(pixmap.width(), pixmap.height())
        self.label_seyirci.setPixmap(pixmap)

        pixmap = QPixmap('src/next.png')
        pixmap = pixmap.scaled(60,60)
        self.label_next.resize(pixmap.width(), pixmap.height())
        self.label_next.setPixmap(pixmap)
        
        self.set_oduls()
        self.make_grey_oduls()
        
    
    def zamanlayici(self):
        self.soru_zamani = 25

        self._25_saniye_sesi.play()

        while self.soru_zamani >= 0 and not self.islost and not self.flag_iscorrect and not self.flag_seyirci:
            self.label_zaman.setText(str(self.soru_zamani))
            if self.soru_zamani == 0:
                self.islost = True
                self.yanlis_sesi.play()
                self.findChild(QLabel, f"label_{self.soru[5]}").setPixmap(QPixmap('src/yanlış.png'))
                self.wait(3000)
                self.get_bitis_sayfasi()
                break
            self.soru_zamani -= 1
            self.wait(1000)



    def make_grey_oduls(self):
        for i in range(15):
            self.findChild(QLabel, f"odul_{i+1}").setStyleSheet(self.gri_odul_style)


    def joker_50(self):
        print("50/50 jokeri kullanıldı")
        cevap = self.soru[5]
        liste = ['a', 'b', 'c', 'd']

        liste.remove(cevap)
        print("silinebilecekler ", liste)
        for i in range(2):
            silinecek = random.choice(liste)
            liste.remove(silinecek)
            self.findChild(QPushButton, f"button_{silinecek}").setText("")
            self.findChild(QPushButton, f"button_{silinecek}").hide()

            self.label_50.setEnabled(False)
            self.button_50.hide()

    def joker_2x(self):
        print("2x jokeri kullanıldı")
        self.label_2x.setEnabled(False)
        self.button_2x.hide()
        self.flag_2x = True
            
    def joker_seyirci(self):
        print("seyirci jokeri kullanıldı")
        self.label_seyirci.setEnabled(False)
        self.button_seyirci.hide()
        self.bil_bakalim.hide()
        self.label_qr.show()
        self.flag_seyirci = True
        self.start_60()

    def start_60(self):

        self._25_saniye_sesi.pause()
        self._60_saniye_sesi.play()
        zaman = 60

        # label_zaman koyu mavi yapılacak
        style = self.label_zaman.styleSheet()
        style += "background-color: blue;"
        self.label_zaman.setStyleSheet(style)


        while zaman>=0:
            self.label_zaman.setText(str(zaman))
            if self.soru_zamani == 0:
                self.islost = True
                break
            zaman -= 1
            self.wait(1000)

        self._60_saniye_sesi.stop()
        self.open_form()
        self._25_saniye_sesi.play()

    

    def open_form(self):

        # open url with selenium bot
        service = Service(EdgeChromiumDriverManager().install())
        options = Options()
        options.add_experimental_option("detach", True)

        #full screen
        options.add_argument("--start-maximized")

        driver = webdriver.Edge(service=service, options=options)
        driver.get(settings.url)

        self.bil_bakalim.show()
        self.label_qr.hide()
        style = self.label_zaman.styleSheet()
        style += "background-color: grey;"
        self.label_zaman.setStyleSheet(style)
        
        self.wait(15000)
        driver.close()

        self.flag_seyirci = False


        
    def disable_for_last_choice(self):
        self.button_a.setEnabled(False)
        self.button_b.setEnabled(False)
        self.button_c.setEnabled(False)
        self.button_d.setEnabled(False)
        self.button_50.setEnabled(False)
        self.button_seyirci.setEnabled(False)
        self.button_2x.setEnabled(False)

    def enable_for_last_choice(self):
        self.button_a.setEnabled(True)
        self.button_b.setEnabled(True)
        self.button_c.setEnabled(True)
        self.button_d.setEnabled(True)
        self.button_50.setEnabled(True)
        self.button_seyirci.setEnabled(True)
        self.button_2x.setEnabled(True)

    def last_choice(self,button):
        print("Son karar ekranı")
        self.son_karar_ekrani.show()
        self.son_karar_ekrani.raise_()
        self.disable_for_last_choice()

        try:
            self.button_evet.clicked.disconnect()
        except TypeError:
            pass  # Eğer daha önce bağlanmamışsa, hata vermesini önlemek için pass

        try:
            self.button_hayir.clicked.disconnect()
        except TypeError:
            pass

        self.button_evet.clicked.connect(lambda: self.last_choice_yes(button))
        self.button_hayir.clicked.connect(self.last_choice_no)
    

    def last_choice_yes(self, button):
        print("Son karar ekranı evet")

        self._25_saniye_sesi.stop()

        self.cevap_sesi.play()

        self.son_karar_ekrani.hide()
        cevap = self.soru[5]
        if button != cevap:
            print("Kaybettiniz")
            self.wait(3000)
            #TODO : kaybetme ekranı yapılacak

            if self.flag_2x:
                self._25_saniye_sesi.play()
                self.findChild(QLabel, f"label_{button}").setPixmap(QPixmap('src/ilk_seçim.png'))
                self.enable_for_last_choice()
                self.findChild(QPushButton, f"button_{button}").setEnabled(False)
                self.flag_2x = False
            else:
                self.yanlis_sesi.play()
                self.islost = True
                self.findChild(QLabel, f"label_{button}").setPixmap(QPixmap('src/yanlış.png'))

                self.wait(3000)

                self.get_bitis_sayfasi()

        else:
            print("Doğru cevap")
            self.wait(3000)
            self.dogru_sesi.play()
            self.findChild(QLabel, f"label_{button}").setPixmap(QPixmap('src/dogru.png'))
            self.flag_2x = False
            self.flag_iscorrect = True

            if self.current_soru == 5 or self.current_soru == 10:
                self.findChild(QLabel, f"odul_{self.current_soru}").setStyleSheet(self.baraj_style)
            else:
                self.findChild(QLabel, f"odul_{self.current_soru}").setStyleSheet(self.odul_style)

            self.wait(2000)

            if self.current_soru < 15:
                self.current_soru += 1
                
                self.label_next.show()
                self.button_next.show()

            else:
                self.get_bitis_sayfasi()

    def get_bitis_sayfasi(self):
        
        if self.islost:
            self.label_kaybet.show()
            self.label_kazan.hide()
        else:
            self.label_kaybet.hide()
            self.label_kazan.show()

            
        if self.current_soru <=5:
            self.label_odul_miktari.setText(f"{settings.oduller[0]} TL")

        elif self.current_soru <10:
            self.label_odul_miktari.setText(f"{settings.oduller[4]} TL")
        
        elif self.current_soru  <15:
            self.label_odul_miktari.setText(f"{settings.oduller[9]} TL")
        
        else:
            self.label_odul_miktari.setText(f"{settings.oduller[14]} TL")
            
        self.bitis.show()

        self.wait(2000)
        


    def last_choice_no(self):
        self.son_karar_ekrani.hide()
        self.enable_for_last_choice()


    def connect_buttons(self):
        self.button_50.clicked.connect(self.joker_50)
        self.button_2x.clicked.connect(self.joker_2x)
        self.button_seyirci.clicked.connect(self.joker_seyirci)
        
        self.button_a.clicked.connect(lambda: self.last_choice("a"))
        self.button_b.clicked.connect(lambda: self.last_choice("b"))
        self.button_c.clicked.connect(lambda: self.last_choice("c"))
        self.button_d.clicked.connect(lambda: self.last_choice("d"))

        self.button_next.clicked.connect(self.start_soru)

        self.button_anamenu.clicked.connect(self.go_to_giris)
        self.button_exit.clicked.connect(self.close)

    
    def go_to_giris(self):
        self.bitis.hide()
        self.giris_ekrani.show()
    
    def set_soru_no(self, no):
        self.label_soru_no_text.setText(f"SORU {str(no)}")
    
    def set_oduls(self):
        oduller = settings.oduller
        for i in range(15):
            self.findChild(QLabel, f"odul_{i+1}").setText(f"{str(oduller[i])} TL")
        
    def get_all_questions(self):
        df = pd.read_excel('sorular.xlsx')
        
        for i in range(len(df)):
            soru = df['Soru'][i]
            a = df['A'][i]
            b = df['B'][i]
            c = df['C'][i]
            d = df['D'][i]
            cevap = df['Cevap'][i]
            zorluk = df['Zorluk'][i]
            if zorluk == 'K':
                self.all_kolay_sorular.append([soru, a, b, c, d, cevap])
            elif zorluk == 'O':
                self.all_orta_sorular.append([soru, a, b, c, d, cevap])
            else:
                self.all_zor_sorular.append([soru, a, b, c, d, cevap])

        self.get_questions()

    def get_questions(self):

        self.kolay_sorular = self.random_5_soru(self.all_kolay_sorular)
        print(self.kolay_sorular)
        self.orta_sorular = self.random_5_soru(self.all_orta_sorular)
        print(self.orta_sorular)
        self.zor_sorular = self.random_5_soru(self.all_zor_sorular)
        print(self.zor_sorular)

    def random_5_soru(self,sorular):
        # 5 soru seç
        return random.sample(sorular, 5)
    
    def set_soru(self):
        if self.current_soru <= 5:
            self.soru = self.kolay_sorular[self.current_soru -1]
            self.label_soru.show()
            self.label_soru_text.setText(self.soru[0])
            self.label_soru_text.show()
            self.wait(5000)
            self.button_a.setText(str(self.soru[1]))
            self.label_a.show()
            self.button_a.show()
            self.wait(1500)
            self.button_b.setText(str(self.soru[2]))
            self.label_b.show()
            self.button_b.show()
            self.wait(1500)
            self.button_c.setText(str(self.soru[3]))
            self.label_c.show()
            self.button_c.show()
            self.wait(1500)
            self.button_d.setText(str(self.soru[4]))
            self.label_d.show()
            self.button_d.show()
            self.wait(1500)

        elif self.current_soru <= 10:
            self.soru = self.orta_sorular[self.current_soru - 6]
            self.label_soru.show()
            self.label_soru_text.setText(self.soru[0])
            self.label_soru_text.show()
            self.wait(5000)
            self.button_a.setText(str(self.soru[1]))
            self.label_a.show()
            self.button_a.show()
            self.wait(1500)
            self.button_b.setText(str(self.soru[2]))
            self.label_b.show()
            self.button_b.show()
            self.wait(1500)
            self.button_c.setText(str(self.soru[3]))
            self.label_c.show()
            self.button_c.show()
            self.wait(1500)
            self.button_d.setText(str(self.soru[4]))
            self.label_d.show()
            self.button_d.show()
            self.wait(1500)
            
        else:
            self.soru = self.zor_sorular[self.current_soru - 11]
            self.label_soru.show()
            self.label_soru_text.setText(self.soru[0])
            self.label_soru_text.show()
            self.wait(5000)
            self.button_a.setText(str(self.soru[1]))
            self.label_a.show()
            self.button_a.show()
            self.wait(1500)
            self.button_b.setText(str(self.soru[2]))
            self.label_b.show()
            self.button_b.show()
            self.wait(1500)
            self.button_c.setText(str(self.soru[3]))
            self.label_c.show()
            self.button_c.show()
            self.wait(1500)
            self.button_d.setText(str(self.soru[4]))
            self.label_d.show()
            self.button_d.show()
            self.wait(1500)
            
        


app = QApplication([])

window = MyWindow()
window.show()
app.exec_()

