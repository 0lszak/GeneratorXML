# -*- coding: utf-8 -*-

#This is a simple PyQt app. The main task here is to select different criteriums and generate a report based on them.

#Notatka po polsku: ktrótka historia tej aplikacji: Znajomy mine poprosił o napisanie prostego GUI, który by generował
#kod XML w zależności od podanych opcji i kryteriów. Dla mnie to idealny powód, żeby zapoznać się z biblioteką PyQt.
#Dojście do tego etapu zajęło mi dwa dni. Kod wymaga jeszcze refaktoryzacji i wciąż jest pare błędów do naprawienia,
#ale przynajmniej wiem jak posługiwać się widżetami z tej biblioteki. No i apka działa, a to najważniejsze.
#Nie dostałem jeszcze od gościa tego XMLa, który ma uzupełniać ta apka, dlatego na razie zwraca zwykły tekst.

#This is how it looks after two days of learning PyQT. I think I need few more days to refactor and improve this code.
#Right now it still heaves some minor errors that need to be fixed, and I still need to receive XML code from guy I did
#it for, but it works quite fine.

#The report uses the current date and all the PyQt widgets you can see below.
import sys
from datetime import date
from PyQt5.QtWidgets import QWidget, QApplication, QComboBox, QVBoxLayout, QGridLayout, QGroupBox,QPushButton,\
    QTableWidget, QTableWidgetItem, QMessageBox, QRadioButton, QAbstractItemView, QLabel, QCheckBox, QLineEdit,\
    QPlainTextEdit

class BaseApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setGeometry(50, 50, 560, 500) #Setting up window geometry. The width is fixed.
        self.setMaximumWidth(560)
        self.setWindowTitle('Just a simple app in PyQt5')
        self.initUI()


    def initUI(self): #This function holds all declarations of widgets used in the application.
        #First, the radio buttons connected to function doCaseOrRepo, which shows widgest depending on the option selected
        self.case = QRadioButton("Case")
        self.repo = QRadioButton("Raport")
        self.case.toggled.connect(self.doCaseOrRepo)
        self.repo.toggled.connect(self.doCaseOrRepo)

        #All of the widgets below is hiden at start. To show them you mast slect case or report
        self.urgent = QCheckBox("Pilne")
        self.urgent.setEnabled(False)
        self.urgent.hide()
        self.note = QCheckBox("notatka")

        self.reason = QLineEdit("powód")
        self.reason.setEnabled(False)
        self.reason.hide()
        self.urgent.stateChanged.connect(self.doCheckReason)

        self.note_txt = QLineEdit("notatka")
        self.note_txt.setEnabled(False)
        self.note.stateChanged.connect(self.doCheckNote)
        self.note.hide()
        self.note_txt.hide()

        self.sub_label = QLabel("dodaj podmiot:")
        self.sub1 = QCheckBox("podmiot1")
        self.sub2 = QCheckBox("podmiot2")
        self.sub3 = QCheckBox("podmiot3")
        self.sub4 = QCheckBox("podmiot4")
        self.sub_label.hide()
        self.sub1.hide()
        self.sub2.hide()
        self.sub3.hide()
        self.sub4.hide()

        self.country = QComboBox(self)
        self.country.addItem("Wybierz kraj")
        for i in range(25):
            self.country.addItem("Kraj %i" % i)
        self.pos1 = QComboBox(self)

        # Defining criteriums. It could be a function that produces these criteriums but in real life each of them
        # contains different items, and it should be defined separately
        self.pos1.addItem("Kryterium1")
        for i in range(4):
            self.pos1.addItem("opcja %i" % i)
        self.pos2 = QComboBox(self)
        self.pos2.addItem("Kryterium2")
        for i in range(4):
            self.pos2.addItem("opcja %i" % i)
        self.pos3 = QComboBox(self)
        self.pos3.addItem("Kryterium3")
        for i in range(4):
            self.pos3.addItem("opcja %i" % i)
        self.pos4 = QComboBox(self)
        self.pos4.addItem("Kryterium4")
        for i in range(4):
            self.pos4.addItem("opcja %i" % i)
        self.country.hide()
        self.pos1.hide()
        self.pos2.hide()
        self.pos3.hide()
        self.pos4.hide()

        #Definition of critrtium table
        self.tab_crit = QTableWidget(1, 5)
        self.tab_crit.columnWidth(60)
        #disable editing of cells
        self.tab_crit.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tab_crit.hide()

        #Here are buttons used to create and change criteriums.
        self.dodaj = QPushButton("Dodaj wiersz")
        self.dodaj.clicked.connect(self.addCrit)
        self.dodaj.hide()

        self.usun_kom =QPushButton("Usuń komórkę")
        self.usun_kom.clicked.connect(self.removeCell)
        self.usun_kom.hide()

        self.usun_wi =QPushButton("Usuń wiersz")
        self.usun_wi.clicked.connect(self.removeRow)
        self.usun_wi.hide()

        #someone has tu accept this criteriums
        self.accept_label = QLabel("Akceptacja:")
        self.minion = QCheckBox("minion")
        self.master = QCheckBox("master")
        self.superior = QCheckBox("superior")
        self.accept_label.hide()
        self.minion.hide()
        self.master.hide()
        self.superior.hide()

        #here is where the date format is used
        self.rapo_date_sent = QCheckBox("Raport wysłano: "+ str(date.today()))
        self.case_date_sent = QCheckBox("Zapytanie wysłano: "+ str(date.today()))
        self.rapo_date_sent.hide()
        #function connected to date checkbox activares generate_xml button
        self.rapo_date_sent.stateChanged.connect(self.activateXML)
        self.case_date_sent.hide()
        self.case_date_sent.stateChanged.connect(self.activateXML)

        self.generate_xml = QPushButton("Generuj XML")
        self.generate_xml.setEnabled(False)
        self.generate_xml.hide()
        self.generate_xml.clicked.connect(self.genXML)

        #after generating XML it shows new textbox with report
        self.XML_code = QPlainTextEdit()
        self.XML_code.hide()

        #Here is where the layout is defined. I used grid layout because its easier to plan the whole GUI and it's quite
        #resistant to resolution changes
        self.createLayout()
        win_layout = QVBoxLayout()
        win_layout.addWidget(self.horizontalGroupBox)
        self.setLayout(win_layout)
        self.show()

    def createLayout(self):
        #name of groupbox
        self.horizontalGroupBox = QGroupBox("Wprowadź dane.")
        layout = QGridLayout()

        layout.setColumnMinimumWidth(0,80)
        layout.setColumnMinimumWidth(1,80)
        layout.setColumnMinimumWidth(2,80)
        layout.setColumnMinimumWidth(3,80)
        layout.setColumnMinimumWidth(4,80)

        #all the widgets pland in their places. Args in addWigdet are: widget, row, col, rowspan, colspan
        layout.addWidget(QLabel("Co chcesz zrobić: "), 0, 0)
        layout.addWidget(self.case, 0, 1)
        layout.addWidget(self.repo, 0, 2)
        layout.addWidget(self.urgent, 1, 0)
        layout.addWidget(self.reason, 1, 1, 1, 3)
        layout.addWidget(self.note, 2, 0)
        layout.addWidget(self.note_txt, 2, 1, 1, 3)

        layout.addWidget(self.sub_label, 3, 0,)
        layout.addWidget(self.sub1, 4, 0)
        layout.addWidget(self.sub2, 5, 0)
        layout.addWidget(self.sub3, 6, 0)
        layout.addWidget(self.sub4, 7, 0)

        layout.addWidget(self.country, 8, 0)
        layout.addWidget(self.pos1, 8, 1)
        layout.addWidget(self.pos2, 8, 2)
        layout.addWidget(self.pos3, 8, 3)
        layout.addWidget(self.pos4, 8, 4)

        layout.addWidget(self.dodaj, 9, 0)
        layout.addWidget(self.usun_kom, 9, 1)
        layout.addWidget(self.usun_wi, 9, 2)

        layout.addWidget(self.tab_crit, 10, 0, 4, 5)
        layout.addWidget(self.accept_label,14,0)
        layout.addWidget(self.minion, 14, 1)
        layout.addWidget(self.master, 14, 2)
        layout.addWidget(self.superior, 14, 3)
        layout.addWidget(self.case_date_sent, 15, 0)
        layout.addWidget(self.rapo_date_sent, 15, 0)
        layout.addWidget(self.generate_xml, 15, 4)
        layout.addWidget(self.XML_code,16,0,10,5)

        self.horizontalGroupBox.setLayout(layout)

    #addCrit function is used to add criteriums to the table. If user doesn't select the country it will return an
    #error message.Also, there is no criterium selected it will return an error message. If some of the criteriums
    #are on primary positions it will skip them and leave the cell blank
    def addCrit(self):
        #this list holds all of the current values from country and criterium comboboxes
        list = [self.country.currentText(), self.pos1.currentText(), self.pos2.currentText(),
                self.pos3.currentText(), self.pos4.currentText()]
        x = self.tab_crit.rowCount()
        for i in range(1,6): #I heave no idea why it didn't work, when i set range from 0 to 5. Seriously.
            #what if the user wont select the country
            if list[i-1] == self.country.itemText(0):
                error_message_country = QMessageBox.information(self,"Błąd kraju", "Wybierz kraj!", QMessageBox.Ok)
                if error_message_country == QMessageBox.Ok:
                    print("Always look on the bright side of life!")
                    break
            #what if the user wont select any of the criteriums
            elif self.pos1.currentText() == self.pos1.itemText(0) \
                    and self.pos2.currentText() == self.pos2.itemText(0) \
                    and self.pos3.currentText() == self.pos3.itemText(0) \
                    and self.pos4.currentText() == self.pos4.itemText(0):
                error_message_crit = QMessageBox.information(self,"Błędne kryteria",
                                                             "Wybierz przynajmniej jedno kryterium!", QMessageBox.Ok)
                if error_message_crit == QMessageBox.Ok:
                    break
            #what if some of criteriums are in primary position
            elif list[i - 1] == self.pos1.itemText(0) or list[i - 1] == self.pos2.itemText(0) \
                    or list[i - 1] == self.pos3.itemText(0) or list[i - 1] == self.pos4.itemText(0):
                self.tab_crit.setItem(x - 1, i - 1, QTableWidgetItem(""))
            else:
                self.tab_crit.setItem(x - 1, i - 1, QTableWidgetItem(list[i - 1]))
        if list[i - 1] == self.country.itemText(0) or self.pos1.currentText() == self.pos1.itemText(0) \
                and self.pos2.currentText() == self.pos2.itemText(0) \
                and self.pos3.currentText() == self.pos3.itemText(0) \
                and self.pos4.currentText() == self.pos4.itemText(0):
            pass
        else:
            #you need to add a new row at the end of any successful adding
            self.tab_crit.setRowCount(x + 1)

    def removeCell(self):
        #if you remove country cell it will remove the whole row
        if self.tab_crit.currentColumn() == 0 and self.tab_crit.currentRow() != self.tab_crit.rowCount()-1:
            self.tab_crit.removeRow(self.tab_crit.currentRow())
        else:
            self.tab_crit.setItem(self.tab_crit.currentRow(), self.tab_crit.currentColumn(), QTableWidgetItem(""))
            #if you remove all of the criteriums in row it will remowve the whole row
            if self.tab_crit.item(self.tab_crit.currentRow(), 1)== "" \
                    and self.tab_crit.item(self.tab_crit.currentRow(), 2) == "" \
                    and self.tab_crit.item(self.tab_crit.currentRow(), 3) == "" \
                    and self.tab_crit.item(self.tab_crit.currentRow(), 4) == "":
                self.tab_crit.removeRow(self.tab_crit.currentRow())
            else:
                pass

    def removeRow(self):
        #This "if" prevents from removing last, empty row:
        if self.tab_crit.currentRow() == self.tab_crit.rowCount()-1:
            pass
        else:
            self.tab_crit.removeRow(self.tab_crit.currentRow())

    def doCheckReason(self): #this function enables reason field if user check urgent
        if self.urgent.isChecked():
            self.reason.setEnabled(True)
        else:
            self.reason.setEnabled(False)

    def doCheckNote(self): #this function enables noet field if user check note
        if self.note.isChecked():
            self.note_txt.setEnabled(True)
        else:
            self.note_txt.setEnabled(False)

    def genXML(self):
        # This function generates the output of this program. It should be XML code, but right now it just prints all of the
        # received pieces of information. it throws error messages when some of the necessary pieces of information are
        # incorrect or blank
        txt = "data "+str(date.today())+"\n"
        if self.case.isChecked():
            #if user select Case
            # it will throw error message if user check urgent and dosen't change text, or leave it blank
            if self.urgent.isChecked():
                if self.reason.text() == "" or self.reason.text() == "powód":
                    error_message_reason= QMessageBox.information(self, "Brak powodu", "Podaj Powód", QMessageBox.Ok)
                    if error_message_reason == QMessageBox.Ok:
                        print("Nobody expects the Spanish Inquisition!")
                else:
                    txt = txt + "powód: "+self.reason.text()+"\n"
            else:
                pass
            if self.note.isChecked():
                #it will throw error message if user check note and dosen't change text, or leave it blank
                if self.note_txt.text() == "" or self.note_txt.text() == "notatka":
                    error_message_note = QMessageBox.information(self, "Brak notatki", "Zapisz notatkę!", QMessageBox.Ok)
                    if error_message_note == QMessageBox.Ok:
                        print("I am an enchanter. There are some who call me...Tim.")
                else:
                    txt = txt + "notatka: " + self.note_txt.text() + "\n"
            else:
                pass
            if self.sub1.isChecked() == False and self.sub2.isChecked() == False and self.sub3.isChecked() == False \
                and self.sub4.isChecked() == False:
                # it will throw error message if user leave all of subs checkboxes unchecked
                error_message_subject = QMessageBox.information(self, "Brak powodu", "Podaj Powód", QMessageBox.Ok)
                if error_message_subject == QMessageBox.Ok:
                    print("This is but a scratch!")
            else:
                txt = txt + "Podmioty: "
                if self.sub1.isChecked():
                    txt = txt + "podmiot1, "
                if self.sub2.isChecked():
                    txt = txt + "podmiot2, "
                if self.sub3.isChecked():
                    txt = txt + "podmiot3, "
                if self.sub4.isChecked():
                    txt = txt + "podmiot4, "
                txt = txt + "\n"
            if self.minion.isChecked() == False and self.master.isChecked() == False and self.superior.isChecked() == False:
                # it will throw error message if user leave all of accept checkboxes unchecked
                error_message_accept = QMessageBox.information(self, "Bład akceptacji", "Nikt nie zaakceptował", QMessageBox.Ok)
                if error_message_accept == QMessageBox.Ok:
                    print("We use only the finest baby frogs…")
            else:
                txt = txt + "Zaakceptowano: "
                if self.sub1.isChecked():
                    txt = txt + "minion, "
                if self.sub2.isChecked():
                    txt = txt + "master, "
                if self.sub3.isChecked():
                    txt = txt + "superior, "
                txt = txt + "\n"
        else:
            #if user select report
            # it will throw error message if user check note and dosen't change text, or leave it blank
            if self.note.isChecked():
                if self.note_txt.text() == "" or self.note_txt.text() == "notatka":
                    error_message_note = QMessageBox.information(self, "Brak notatki", "Zapisz notatkę!", QMessageBox.Ok)
                    if error_message_note == QMessageBox.Ok:
                        print("I am an enchanter. There are some who call me...Tim.")
                else:
                    txt = txt + "notatka: " + self.note_txt.text() + "\n"
            else:
                pass
            if self.sub1.isChecked() == False and self.sub2.isChecked() == False and self.sub3.isChecked() == False \
                and self.sub4.isChecked() == False:
                # it will throw error message if user leave all of subs checkboxes unchecked
                error_message_subject = QMessageBox.information(self, "Brak powodu", "Podaj Powód", QMessageBox.Ok)
                if error_message_subject == QMessageBox.Ok:
                    print("This is but a scratch!")
            else:
                txt = txt + "Podmioty: "
                if self.sub1.isChecked():
                    txt = txt + "podmiot1, "
                if self.sub2.isChecked():
                    txt = txt + "podmiot2, "
                if self.sub3.isChecked():
                    txt = txt + "podmiot3, "
                if self.sub4.isChecked():
                    txt = txt + "podmiot4, "
                txt = txt + "\n"
            if self.tab_crit.rowCount() == 1:
                # it will throw error message if there are no criteriums defined
                error_message_rows= QMessageBox.information(self, "Brak kryteriów", "dodaj kryteria", QMessageBox.Ok)
                if error_message_rows == QMessageBox.Ok:
                    print("Are you suggesting that coconuts migrate?")
            else:
                for i in range(self.tab_crit.rowCount()-1):
                    for j in range(4):
                        #this loop reads cells from tab_crit and add them to report
                        txt = txt + self.tab_crit.item(i,j).text() + ", "
                    txt = txt + "\n"
            if self.minion.isChecked() == False and self.master.isChecked() == False and self.superior.isChecked() == False:
                error_message_accept = QMessageBox.information(self, "Bład akceptacji", "Nikt nie zaakceptował", QMessageBox.Ok)
                if error_message_accept == QMessageBox.Ok:
                    print("We use only the finest baby frogs")
            else:
                txt = txt + "Zaakceptowano: "
                if self.sub1.isChecked():
                    txt = txt + "minion, "
                if self.sub2.isChecked():
                    txt = txt + "master, "
                if self.sub3.isChecked():
                    txt = txt + "superior, "
                txt = txt + "\n"
        #all of the gathered information is shown on new texfield
        self.XML_code.show()
        self.XML_code.setPlainText(txt)

    def doCaseOrRepo(self): #depending on chosen option (case, report) it will show or hide widgets
        if self.case.isChecked():
            self.urgent.show()
            self.urgent.setEnabled(True)
            self.reason.show()
            self.note.show()
            self.note_txt.show()
            self.tab_crit.hide()
            self.sub_label.show()
            self.sub1.show()
            self.sub2.show()
            self.sub3.show()
            self.sub4.show()
            self.country.hide()
            self.pos1.hide()
            self.pos2.hide()
            self.pos3.hide()
            self.pos4.hide()
            self.dodaj.hide()
            self.usun_kom.hide()
            self.usun_wi.hide()
            self.accept_label.show()
            self.minion.show()
            self.master.show()
            self.superior.show()
            self.rapo_date_sent.hide()
            self.case_date_sent.show()
            self.generate_xml.show()
            #it also clears note textbox and disables generat_XML button
            self.generate_xml.setEnabled(False)
            self.XML_code.hide()
            self.note_txt.setText("notatka")
        else:
            self.urgent.hide()
            self.urgent.setEnabled(True)
            self.reason.hide()
            self.note.show()
            self.note_txt.show()
            self.tab_crit.show()
            self.country.show()
            self.sub_label.show()
            self.sub1.show()
            self.sub2.show()
            self.sub3.show()
            self.sub4.show()
            self.pos1.show()
            self.pos2.show()
            self.pos3.show()
            self.pos4.show()
            self.dodaj.show()
            self.usun_kom.show()
            self.usun_wi.show()
            self.accept_label.show()
            self.minion.show()
            self.master.show()
            self.superior.show()
            self.rapo_date_sent.show()
            self.case_date_sent.hide()
            self.generate_xml.show()
            # it also clears note textbox and disables generat_XML button
            self.generate_xml.setEnabled(False)
            self.XML_code.hide()
            self.note_txt.setText("notatka")

    def activateXML(self): #this function activates generate_XML button if user confirms date
        if self.rapo_date_sent.isChecked() and self.repo.isChecked():
            self.generate_xml.setEnabled(True)
        elif self.case_date_sent.isChecked() and self.case.isChecked():
            self.generate_xml.setEnabled(True)
        else:
            self.generate_xml.setEnabled(False)

if __name__ == '__main__': #at the end we need entity of this app
    app = QApplication(sys.argv)
    ex = BaseApp()
    sys.exit(app.exec_())

