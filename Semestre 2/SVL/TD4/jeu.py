# SVL 1516
# CTD4 - C. Quetstroey

# jeu du déviner nombre
# le programme choisit un nombre entre 0 et 9
# le joueur à N tentative pour deviner ce nombre
# à chaque tentative le programme lui indique s'il est
# trop haut ou trop bas
class JeuDevinerUnNombre:

    def __init__(self, generateur, lecteur, afficheur):
        self.generateur = generateur
        self.lecteur = lecteur
        self.afficheur = afficheur

    def jouer(self):
        a_deviner = self.generateur.genere_nombre_a_deviner()
        gagne = False
        while not gagne:
            self.afficheur.notifier_invitation_choisir_un_nombre()
            proposition = self.lecteur.lire_un_nombre()
            if proposition == a_deviner :
                gagne = True
            elif proposition < a_deviner :
                self.afficheur.notifier_nombre_trop_petit()
            else
                self.afficheur.notifier_nombre_trop_grand()
                
        self.afficheur.notifier_joueur_a_gagne()

import sys

class LecteurSurEntreeStandard:

    def __init__(self, flot_entree=sys.stdin):
        self.flot_entree = flot_entree

    def lire_un_nombre(self):
        return int(self.flot_entree.readline())
