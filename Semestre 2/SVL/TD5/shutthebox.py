import sys
class ShutTheBox:

    def __init__(self, participants, clapets, lanceur, actif, nbTour, lecteur, nbJoueur = 2):
        self.joueurs = participants
        self.clapets = clapets
        self.lanceur = lanceur
        self.jActif = actif
        self.tour = nbTour
        self.lecteur = lecteur
        self.nbJoueur = nbJoueur
    """
    def jouer_stb(self):
        boucle
            test si gagnant
            lancer des
            selectionné des
            test valid des
            ferme clapets
            test si tous les clapets sont fermés si oui  gagnant :D
        fin

    def lancerpartie() -> tour 10
    """
    def gagnant(self):
        minimum = sys.maxsize
        gagnant = None
        for j in self.joueurs:
            if j.score() < minimum :
                minimum = j.score()
                gagnant = j
        return gagnant

    def gagnant_tous_clapets_fermes(self):
        for a in self.clapets:
            if a == False:
                return None
        return self.joueurs[self.jActif]

    def valid_clapets_selects(self, choix):
        valid = False
        val_des = self.lanceur.des()
        # Test de la valeur des clapets selectionnés par rapport aux dés
        res = choix[0] + choix[1]
        if res == val_des :
            valid = True
        else :
            return False
        # Test par rapport aux clapets
        if self.clapets[choix[0]-1] :
            return False
        if self.clapets[choix[1]-1] :
            return False
        return valid

    def fermes_clapets(self, choix):
        if not self.valid_clapets_selects(choix):
            raise FermetureClapetsError()
        self.clapets[choix[0]-1] = True
        self.clapets[choix[1]-1] = True
        return self.clapets

    def peut_lancer_1_de(self):
        a = self.clapets[8]
        b = self.clapets[7]
        c = self.clapets[6]
        return a and b and c

    def reset_tour(self):
        self.jActif = (self.jActif + 1) % self.nbJoueur
        self.clapets = [False]*9

class FermetureClapetsError(Exception):
    pass
