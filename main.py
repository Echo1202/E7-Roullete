from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLineEdit, QPushButton, QScrollArea, QHBoxLayout, QCompleter,
                             QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy)
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import (Qt, QSize)
import random, sys, os.path, json
import requests


# create widget that will add and remove characters from the roulette pool
class AddRemoveWidget(QWidget):
    def __init__(self, name):
        super(AddRemoveWidget, self).__init__()

        self.name = name
        self.added = False

        # set up add and remove buttons
        self.label = QLabel(self.name)
        self.button_remove = QPushButton("Remove")
        self.button_add = QPushButton("Add")

        # set up the "box" for interaction
        self.hBox = QHBoxLayout()
        self.hBox.addWidget(self.label)
        self.hBox.addWidget(self.button_remove)
        self.hBox.addWidget(self.button_add)

        self.button_add.clicked.connect(self.add)
        self.button_remove.clicked.connect(self.remove)

        self.setLayout(self.hBox)

        self.update_button_state()

    def add(self, name):
        self.added = True
        self.update_button_state()

    def remove(self, name):
        self.added = False
        self.update_button_state()

    def update_button_state(self):
        if self.added == True:
            self.button_add.setStyleSheet("background-color: #32CD32; color #fff;")
            self.button_remove.setStyleSheet("background-color: none; color: none;")
        else:
            self.button_add.setStyleSheet("background-color: none; color: none;")
            self.button_remove.setStyleSheet("background-color: #D32F2f; color: #fff")


# create main window (think of this as the main())
class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.initUI()

    def addCharToList(self, character):
        if not character in self.userList:
            self.userList.append(character)

    def removeCharFromList(self, character):
        if character in self.userList:
            self.userList.remove(character)

    def importChar(self):
        if os.path.isfile('Hero_List.txt'):
            self.numChar = 0
            with open("Hero_List.txt") as file_in:
                lines = []
                for line in file_in:
                    line = line.rstrip('\n')
                    self.addCharToList(line)
                    self.numChar = self.numChar + 1
            self.importStatus.setText("Imported!" + str(self.numChar) + " characters in the pool")
            self.importStatus.setStyleSheet("color: #32CD32")
            self.importStatus.adjustSize()

        else:
            self.importStatus.setText("Error: please make sure that a 'Hero_List.txt' file is in your directory")
            self.importStatus.setStyleSheet("color: #FF0000")
            self.importStatus.adjustSize()

    def initUI(self):
        self.controls = QWidget()
        self.controlsLayout = QVBoxLayout()

        # read json file and get jepg
        try:
            with open('e7dbherodata.json') as json_file:
                self.data = json.load(json_file)
        except:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage("Missing e7assets.json file")
            error_dialog.exec_()

        self.userList = []

        # list of characters, separated by star grade
        characters5 = ('Alencia', 'Ambitious Tywin', 'Apocalypse Ravi', 'Aramintha', 'Arbiter Vildred', 'Baal & Sezan',
                       'Baiken', 'Basar', 'Bellona', 'Blood Moon Haste', 'Briar Witch Iseria', 'Cecilia', 'Celine',
                       'Cerise', 'Cermia', 'Charles', 'Charlotte', 'Chloe', 'Choux', 'Dark Corvus',
                       'Desert Jewel Basar', 'Destina', 'Diene', 'Dizzy', 'Elena', 'Elphelt', 'Ervalen',
                       'Faithless Lidica', 'Fallen Cecilia', 'Flan', 'Haste', 'Holiday Yufine', 'Iseria', 'Judge Kise',
                       'Kawerik', 'Kayron', 'Ken', 'Kise', 'Krau', 'Landy', 'Last Rider Krau', 'Lidica', 'Lilias',
                       'Lilibet', 'Little Queen Charlotte', 'Ludwig', 'Luluca', 'Luna', 'Maid Chloe',
                       'Martial Artist Ken', 'Melissa', 'Mui', 'Operator Sigret', 'Pavel', 'Ravi', 'Ray',
                       'Remnant Violet', 'Roana', 'Ruele of Light', 'Sage Baal & Sezan', 'Seaside Bellona', 'Sez',
                       'Sigret', 'Silver Blade Aramintha', 'Sol', 'Specimen Sez', 'Specter Tenebria', 'Tamarinne',
                       'Tenebria', 'Top Model Luluca', 'Tywin', 'Vildred', 'Violet', 'Vivian', 'Yufine', 'Yuna', 'Zeno',
                       'Fairytale Tenebria', 'Mort')
        characters4 = ('Achates','Angelica','Armin','Assassin Cartuja','Assassin Cidd','Assassin Coli','Auxiliary Lots',
                       'Benevolent Romann','Blaze Dingo','Blood Blade Karin','Cartuja','Celestial Mercedes',
                       'Challenger Dominiel','Champion Zerato','Cidd','Clarissa','Coli','Corvus','Crescent Moon Rin',
                       'Crimson Armin','Crozet','Dingo','Dominiel','Fighter Maya','Free Spirit Tieria','Furious',
                       'General Purrgis','Guider Aither','Karin','Khawana','Khawazu','Kitty Clarissa','Kizuna AI','Leo',
                       'Lots','Maya','Mercedes','Purrgis','Rin','Roaming Warrior Leo','Romann','Rose','Schuri','Serila',
                       'Shadow Rose','Shooting Star Achates','Silk','Sinful Angelica','Surin','Tempest Surin',
                       'Troublemaker Crozet','Wanderer Silk','Watcher Schuri','Zerato')
        characters3 = ('Adlay','Adventurer Ras','Ainos','Ains','Aither','Alexa','All-Rounder Wanda',
                       'Angelic Montmorancy','Arowell','Azalea','Bask','Batisse','Butcher Corps Inquisitor',
                       'Captain Rikoris','Carmainerose','Carrot','Celeste','Chaos Inquisitor','Chaos Sect Ax',
                       'Church of Ilryos Axe','Commander Lorina','Doll Maker Pearlhorizon','Doris','Eaton','Elson',
                       'Enott','Falconer Kluri','Glenn','Gloomyrain','Godmother','Gunther','Hataan','Hazel','Helga',
                       'Hurado','Ian','Jecht','Jena','Judith','Kikirat v2', 'Kiris', 'Kluri', 'Lena', 'Lorina',
                       'Magic Scholar Doris','Mascot Hazel', 'Mercenary Helga', 'Mirsa', 'Mistychain', 'Montmorancy',
                       'Mucacha', 'Nemunas','Otillie', 'Pearlhorizon', 'Pyllis', 'Ras', 'Requiemroar',
                       'Researcher Carrot', 'Righteous Thief Roozid','Rikoris', 'Rima', 'Roozid', 'Sonia', 'Sven',
                       'Taranor Guard', 'Taranor Royal Guard', 'Tieria', 'Wanda', 'Zealot Carmainerose')
        charactersAll = characters5 + characters4 + characters3

        self.widgets = []

        for name in charactersAll:
            item = AddRemoveWidget(name)
            # attribute functions to each button
            item.button_add.clicked.connect(lambda _, name=name: self.addCharToList(name))
            item.button_remove.clicked.connect(lambda _, name=name: self.removeCharFromList(name))
            self.controlsLayout.addWidget(item)
            self.widgets.append(item)

        spacer = QSpacerItem(1, 1, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.controlsLayout.addItem(spacer)
        self.controls.setLayout(self.controlsLayout)

        self.setWindowTitle("E7 Ultimate Bravery")
        self.setGeometry(200, 200, 1024, 680)

        self.label1 = QtWidgets.QLabel(self)
        self.label1.setText("<h1>Epic 7 Roulette</h1>")
        self.label1.adjustSize()
        self.label1.move(10, 15)

        self.label2 = QtWidgets.QLabel(self)
        self.label2.setText("Add Characters to Roulette")
        self.label2.move(10, 55)
        self.label2.adjustSize()

        self.label3 = QtWidgets.QLabel(self)
        self.label3.setText("<h1>Team 1:</h1>")
        self.label3.adjustSize()
        self.label3.move(540, 60)

        self.label4 = QtWidgets.QLabel(self)
        self.label4.setText("")
        self.label4.move(540, 85)

        self.label5 = QtWidgets.QLabel(self)
        self.label5.setText("")
        self.label5.move(650, 85)

        self.label6 = QtWidgets.QLabel(self)
        self.label6.setText("")
        self.label6.move(760, 85)

        self.label7 = QtWidgets.QLabel(self)
        self.label7.setText("<h1>Team 2:</h1>")
        self.label7.adjustSize()
        self.label7.move(540, 200)

        self.label8 = QtWidgets.QLabel(self)
        self.label8.setText("")
        self.label8.move(540, 225)

        self.label9 = QtWidgets.QLabel(self)
        self.label9.setText("")
        self.label9.move(650, 225)

        self.label10 = QtWidgets.QLabel(self)
        self.label10.setText("")
        self.label10.move(760, 225)

        self.image = QImage()

        self.scroll = QScrollArea()
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(False)
        self.scroll.setWidget(self.controls)

        self.searchBar = QLineEdit()
        self.searchBar.adjustSize()
        self.searchBar.textChanged.connect(self.updateDisplay)

        self.completer = QCompleter(charactersAll)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.searchBar.setCompleter(self.completer)

        container = QWidget()
        containerLayout = QVBoxLayout()
        containerLayout.addWidget(self.searchBar)
        containerLayout.addWidget(self.scroll)
        containerLayout.setContentsMargins(10, 85, 0, 0)

        container.setLayout(containerLayout)
        container.setFixedSize(400, 600)
        self.setCentralWidget(container)

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Roll")
        self.b1.setGeometry(10, 610, 390, 40)
        self.b1.clicked.connect(self.RandRoll)

        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setText("Import")
        self.b2.setGeometry(250, 25, 100, 20)
        self.b2.clicked.connect(self.importChar)

        self.importStatus = QtWidgets.QLabel(self)
        self.importStatus.setText("")
        self.importStatus.move(360, 30)


    def updateDisplay(self, text):
        for widget in self.widgets:
            if text.lower() in widget.name.lower():
                widget.show()
            else:
                widget.hide()

    def displayImage(self, url, label):
        self.image.loadFromData(requests.get(url).content)
        label.setPixmap(QtGui.QPixmap(self.image).scaled(100, 100, Qt.KeepAspectRatio))
        label.adjustSize()

    def RandRoll(self):

        if (len(self.userList)) < 6:
            self.label4.setText("<h1>Not enough characters in pool</h1>")
            self.label4.setStyleSheet("color: #FF0000")
            self.label4.adjustSize()
            return

        #create a separate list to save "names" for rerolls
        self.tempList = []

        selectedString = random.choice(self.userList)
        self.tempList.append(selectedString)
        url_img = self.data[selectedString]['assets']['icon']
        self.displayImage(url_img, self.label4)
        self.userList.remove(selectedString)

        selectedString = random.choice(self.userList)
        self.tempList.append(selectedString)
        url_img = self.data[selectedString]['assets']['icon']
        self.displayImage(url_img, self.label5)
        self.userList.remove(selectedString)

        selectedString = random.choice(self.userList)
        self.tempList.append(selectedString)
        url_img = self.data[selectedString]['assets']['icon']
        self.displayImage(url_img, self.label6)
        self.userList.remove(selectedString)

        selectedString = random.choice(self.userList)
        self.tempList.append(selectedString)
        url_img = self.data[selectedString]['assets']['icon']
        self.displayImage(url_img, self.label8)
        self.userList.remove(selectedString)

        selectedString = random.choice(self.userList)
        self.tempList.append(selectedString)
        url_img = self.data[selectedString]['assets']['icon']
        self.displayImage(url_img, self.label9)
        self.userList.remove(selectedString)

        selectedString = random.choice(self.userList)
        self.tempList.append(selectedString)
        url_img = self.data[selectedString]['assets']['icon']
        self.displayImage(url_img, self.label10)
        self.userList.remove(selectedString)

        # add back all "removed" names into userList
        self.userList = self.userList + self.tempList

def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())


window()
