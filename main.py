import sys
from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QDialog, QApplication, QVBoxLayout, QPushButton
from PyQt6.uic import loadUi
from pymongo import MongoClient
from PyQt6.QtWidgets import QTableWidgetItem


class Login(QDialog):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("login.ui", self)
        self.setFixedWidth(550)
        self.setFixedHeight(400)
        self.login.clicked.connect(self.loginfunction)
        self.passwordinput.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.mongo_client = MongoClient("mongodb://localhost:27017")
        self.db = self.mongo_client["triyaj"]
        self.collection = self.create_or_get_collection()

    def create_or_get_collection(self):
        collection_name = "hastalar"
        collection = self.db.get_collection(collection_name)

        # Eğer koleksiyon yoksa oluştur
        if collection_name not in self.db.list_collection_names():
            collection.create_collection(collection_name, id_field="kimlikNo")  # id_field ile ismi değiştir
            collection.create_index([("kimlikNo", 1)], unique=True)  # kimlikNo'yu benzersiz olarak ayarla

        return collection

    def loginfunction(self):
        try:
            usernameinput = self.usernameinput.text()
            passwordinput = self.passwordinput.text()

            if usernameinput == "hemsire" and passwordinput == "11":
                hemsire_window = Hemsire(self.collection)
                widget.addWidget(hemsire_window)
                widget.setCurrentWidget(hemsire_window)  # Aktif pencereyi değiştir



            elif usernameinput == "doktor" and passwordinput == "11":

                self.gosterPencere = GosterPencere(self.collection)

                widget.addWidget(self.gosterPencere)

                widget.setCurrentWidget(self.gosterPencere)


            else:
                hata_window = Hata()
                widget.addWidget(hata_window)
                widget.setCurrentWidget(hata_window)

        except Exception as e:
            print("Hata:", e)


class Hata(QDialog):
    def __init__(self):
        super(Hata, self).__init__()
        loadUi("hata.ui", self)
        self.setFixedWidth(350)
        self.setFixedHeight(200)


class GosterPencere(QDialog):
    def __init__(self, collection):
        super(GosterPencere, self).__init__()
        loadUi("hastaveri.ui", self)
        self.setFixedWidth(1000)
        self.setFixedHeight(500)
        self.collection = collection


        self.guncelleTablo()

    def guncelleTablo(self):

        hastalar = self.collection.find({}, {"_id": 0})

        for satir_index, hasta in enumerate(hastalar): #indeksle döndur
            self.hastaveri.insertRow(satir_index)

            for sutun_index, (anahtar, deger) in enumerate(hasta.items()):
                yeni_hucre = QTableWidgetItem(str(deger))
                self.hastaveri.setItem(satir_index, sutun_index, yeni_hucre)


class Hemsire(QDialog):
    def __init__(self, collection):
        super(Hemsire, self).__init__()
        loadUi("hemsire.ui", self)
        self.setFixedWidth(350)
        self.setFixedHeight(250)
        self.hemsireKayit.clicked.connect(self.hastaKayit)
        self.hemsireGor.clicked.connect(lambda: self.hastaBilgi(collection))
        self.hasta_kayit_dialog = hastaKayitalma(collection)

    def hastaKayit(self, collection):
        widget.addWidget(self.hasta_kayit_dialog)
        widget.setCurrentWidget(self.hasta_kayit_dialog)

        self.hasta_kayit_dialog.geributon.clicked.connect(self.geridon)  # geri donus
        self.collection = collection

    def hastaBilgi(self, collection):
        doktor_window = GosterPencere(collection)
        widget.addWidget(doktor_window)
        widget.setCurrentWidget(doktor_window)

    def geridon(self):
        widget.setCurrentWidget(self)
        self.setFixedWidth(350)
        self.setFixedHeight(250)

class hastaKayitalma(QDialog):
    def __init__(self, collection):
        super(hastaKayitalma, self).__init__()
        loadUi("hastaKayit.ui", self)
        self.setFixedWidth(350)
        self.setFixedHeight(650)
        self.collection = collection
        self.kaydetbuton.clicked.connect(self.kaydet)


    def kaydet(self):
        hasta_kimlikno = self.kimlikNo.text()
        hasta_adsoyad = self.kayitisim.text()
        hasta_sikayet = self.sikayet.text()
        hasta_triyajrenk = self.triyajrenk.text()
        hasta_nabiz = self.nabiz.text()
        hasta_Sp02 = self.oksi.text()
        hasta_oncesi = self.hastalik.text()
        hasta_alerji = self.alerji.text()
        hasta_ates = self.ates.text()
        hasta_tedavi = self.tedavi.text()

        yeni_hasta = {
            "Kimlik No ": hasta_kimlikno,
            "Ad Soyad ": hasta_adsoyad,
            "Şikayet ": hasta_sikayet,
            "Triyaj Rengi ": hasta_triyajrenk,
            "Nabız ": hasta_nabiz,
            "Sp02": hasta_Sp02,
            "Eski Hastalıklar ": hasta_oncesi,
            "Alerji ": hasta_alerji,
            "Ateş ": hasta_ates,
            "Uygulanan Tedavi": hasta_tedavi
        }
        self.collection.insert_one(yeni_hasta)
        hemsire_window = Hemsire(self.collection)
        widget.addWidget(hemsire_window)
        widget.setCurrentWidget(hemsire_window)


app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.show()
sys.exit(app.exec())
