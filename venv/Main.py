import sys
from threading import Thread
import time
from PyQt5 import QtSvg
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class Pompe(Thread):

    def __init__(self, numero, commande, label, edit,spin):
        Thread.__init__(self)
        self.numero = numero
        self.commande =commande
        self.label = label
        self.edit = edit
        self.spin = spin

    def run(self):
        while True:
            if len(self.commande)>0:
                for i in self.commande:
                    if int(i[0]) == int(self.numero) and str(i[2]) == str(self.edit.text()):
                        self.edit.setText('En utilisation')
                        self.edit.setDisabled(True)
                        self.spin.setDisabled(True)
                        self.label.setStyleSheet("QLabel {  color : red; }")
                        attente = (int(i[1])*(self.spin.value()/100)) / 10
                        self.commande.remove(i)
                        time.sleep(attente)
                        self.label.setStyleSheet("QLabel {  color : green; }")
                        self.edit.setEnabled(True)
                        self.spin.setEnabled(True)
                        self.edit.setText('')
                        self.spin.setValue(100)

class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()



    def initUI(self):
        self.code = 0
        self.nbPompe=5
        self.pompeSelectionee=0
        self.listPompe=[]
        self.espaceTuple = []
        layout = QHBoxLayout()
        rightLayout = QVBoxLayout()
        leftLayout = QVBoxLayout()
        layout.addLayout(leftLayout)
        layout.addWidget(QMenuBar())
        layout.addLayout(rightLayout)
        self.choixPompe = QComboBox()
        self.choixPompe.setToolTip("Choix de pompe")
        self.setLayout(layout)
        self.setGeometry(200, 100, 500, 500)
        self.setWindowTitle('Station service')
        self.show()
        for i in range (0,self.nbPompe):
            editLayout = QHBoxLayout()
            spinLayout = QHBoxLayout()
            self.choixPompe.addItem(("Pompe "+str(i)))
            label = QLabel("Pompe : "+str(i))
            label.setStyleSheet("QLabel {  color : green; }");
            edit =QLineEdit()
            spin = QSpinBox()
            spin.setRange(0, 100)
            spin.setValue(100)
            pompeThread =Pompe(i,self.espaceTuple,label,edit,spin)
            pompeThread.start()
            self.listPompe.append([label,edit,pompeThread])
            editLayout.addWidget(QLabel("Entrez votre code:"))
            editLayout.addWidget(edit)

            spinLayout.addWidget(QLabel("Pourcentage preleve"))
            spinLayout.addWidget(spin)

            rightLayout.addWidget(label)
            rightLayout.addLayout(spinLayout)
            rightLayout.addLayout(editLayout)

        self.choixPompe.currentIndexChanged.connect(self.selectionnerPompe)
        leftLayout.addWidget(self.choixPompe)
        self.qte = QLineEdit()
        leftLayout.addWidget(self.qte)
        self.payerButton = QPushButton('Payer',self)
        self.payerButton.clicked[bool].connect(self.payer)
        leftLayout.addWidget(self.payerButton)
        self.codeLabel =QLabel('')
        leftLayout.addWidget(self.codeLabel)



    def selectionnerPompe(self,i):
        self.pompeSelectionee=i
        self.update()

    def payer(self):
        self.espaceTuple.append([self.pompeSelectionee,self.qte.text(),self.code])
        self.codeLabel.setText("Votre code: "+str(self.code))

        self.code+=1
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

