
import sys
from threading import Thread
import time

commande = []


class Pompe(Thread):

    def __init__(self, numero):
        Thread.__init__(self)
        self.numero = numero

    def run(self):
        while True:
            if len(commande)>0:
                sys.stdout.flush()
                if int(commande[0][0]) == int(self.numero):
                    sys.stdout.write("La pompe numero "+str(self.numero)+" fournit "+str(commande[0][1])+"L \n")
                    sys.stdout.flush()
                    attente=commande[0][1] / 10
                    commande.remove(commande[0])
                    time.sleep(attente)
                    sys.stdout.write("La pompe numero "+str(self.numero)+" est libre \n")

class Caisse(Thread):

    def __init__(self):
        Thread.__init__(self)


    def run(self):
        while True:
            sys.stdout.write("Entrez numero de caisse \n")
            sys.stdout.flush()
            numeroCaisse=input()
            sys.stdout.write("Entrez la quantitee d'escence \n")
            sys.stdout.flush()
            qte = input()
            commande.append([int(numeroCaisse), int(qte)])

pompe1=Pompe(1)
pompe2=Pompe(2)

pompe1.start()
pompe2.start()

caisse= Caisse()

caisse.start()

pompe1.join()
pompe2.join()
caisse.join()