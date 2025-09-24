"""Thread helper performing GRBL's homing cycle."""

from threading import Thread


class PriseOrigine(Thread):
    def __init__(self, connexion):
        super().__init__()
        self.running = True
        self.rxPriseOrigine = []
        self.connexion = connexion

    def run(self):
        while self.running:
            self.connexion.write("$H\n".encode())
            print("TML HOMMING")
            self.rxPriseOrigine.append(self.connexion.readline().decode().strip())
            if self.rxPriseOrigine[0].find("ALARM:9") > -1:
                for _ in range(4):
                    self.rxPriseOrigine.append(self.connexion.readline().decode().strip())
                self.connexion.write("$X\n".encode())
                for _ in range(2):
                    self.rxPriseOrigine.append(self.connexion.readline().decode().strip())
            # Si la prise d'origine réussi

            self.stop()

    def stop(self):
        self.running = False
			

