"""
  Fonctionnalité et principe du jeu
        - Joueur lance 2 dés et additionne
        - Ferme une combinaison de clapets
                (Tant qu'il n'est pas bloqué)
        - Fin de tour et somme des points clapets ouvert
        - Si clapets 789 fermé peut lancé un seul dés
        - Fin en 10 tours
        - le gagnant gagne avec le plus petit point
        - le gagnant gagne avec tous les clapets fermés
"""
import unittest
from mockito import *
from shutthebox import *
class TestShutTheBox(unittest.TestCase):
    """
        Class testant les fonctionnalités du jeu
            - test gagnant avec le plus petit points - [ok]
            - test gagnant avec tous les clapets fermés - [ok]
            - test les clapets fermés - [ok]
            - test clapets sélectionnées - [ok]
            - test si le joueur peut lancer 1 de - [ok]
            - test si passe au joueur suivant
    """
    def setUp(self):
        # Joueur
        self.joueur1 = mock()
        self.joueur2 = mock()
        self.joueurs = [self.joueur1, self.joueur2]
        self.joueurActif = 1
        self.joueurActif1 = 0
        # Tous ouverts sauf le 3
        self.clapets_start = [False]*9
        self.clapets_start[2] = True
        # Clapet pour 1 dés
        self.clapets_1_de = [False]*9
        self.clapets_1_de[8] = True
        self.clapets_1_de[7] = True
        self.clapets_1_de[6] = True
        # Tous fermés
        self.clapets_end = [True]*9
        # Des
        self.lanceur = mock()
        # lecteur
        self.lecteur = mock()
        # Tour
        self.tour = 10
        # Test Class
        self.stb_next = ShutTheBox(self.joueurs, self.clapets_start, self.lanceur, self.joueurActif1, self.tour, self.lecteur)
        self.stb = ShutTheBox(self.joueurs, self.clapets_start, self.lanceur, self.joueurActif, self.tour, self.lecteur)
        self.stb_fin = ShutTheBox(self.joueurs, self.clapets_end, self.lanceur, self.joueurActif, self.tour, self.lecteur)
        self.stb_1_de = ShutTheBox(self.joueurs, self.clapets_1_de, self.lanceur, self.joueurActif, self.tour, self.lecteur)

    """
        IL FAUT INTEGRER LE LECTEUR ET AFFICHEUR AUX TESTS
        AINSI QUE LE TABLEAU DE DES

        Test si le gagnant a bien le plus petit score ou que tous ses clapets sont fermés
    """
    def test_gagnant_avec_le_petit_points(self):
        SCORE_J1 = 10
        SCORE_J2 = 15
        when(self.joueur1).score().thenReturn(SCORE_J1)
        when(self.joueur2).score().thenReturn(SCORE_J2)
        gagnant = self.stb.gagnant()
        self.assertEqual(gagnant, self.joueur1)

    def test_gagnant_avec_tous_clapets_fermes(self):
        gagnant = self.stb_fin.gagnant_tous_clapets_fermes()
        self.assertEqual(gagnant, self.joueur2)

    """
        Test les clapets sélectionnés
    """
    def test_valid_clapets_selectionnes_corrects(self):
        when(self.lanceur).des().thenReturn(7)
        result = self.stb.valid_clapets_selects([2, 5])
        self.assertEqual(result, True)

    def test_valid_clapets_selectionnes_incorrects(self):
        when(self.lanceur).des().thenReturn(7)
        result = self.stb.valid_clapets_selects([3, 5])
        self.assertEqual(result, False)

    def test_valid_clapets_ouverts(self):
        when(self.lanceur).des().thenReturn(7)
        result = self.stb.valid_clapets_selects([2, 5])
        self.assertEqual(result, True)

    def test_valid_clapets_fermes(self):
        when(self.lanceur).des().thenReturn(7)
        result = self.stb.valid_clapets_selects([3, 4])
        self.assertEqual(result, False)

    """
        Test les clapets
    """
    def test_fermes_clapets_correcte(self):
        when(self.lanceur).des().thenReturn(7)
        new_clapets = self.stb.fermes_clapets([2, 5])
        res_clapets = [False, True, True, False, True, False, False, False, False]
        self.assertEqual(res_clapets, new_clapets)

    def test_fermes_clapets_incorrecte(self):
        CHOIX = [3 , 4]
        when(self.lanceur).des().thenReturn(7)
        self.assertRaises(FermetureClapetsError,self.stb.fermes_clapets, CHOIX)

    """
        Test si le joueur peut lancer un seul dés
    """
    def test_joueur_peut_lancer_1_de_correct(self):
        res = self.stb_1_de.peut_lancer_1_de()
        self.assertEqual(res, True)

    def test_joueur_peut_lancer_1_de_incorrect(self):
        res = self.stb.peut_lancer_1_de()
        self.assertEqual(res, False)

    """
        Test si on passe bien au joueur suivant et reboot les clapets
    """

    def test_reset_joueur_suivant_correct(self):
        self.stb_next.reset_tour()
        self.assertEqual(self.stb_next.jActif, self.joueurActif)

    def test_reset_clapets_tous_ouvert(self):
        self.stb_next.reset_tour()
        self.assertEqual(self.stb_next.clapets, [False]*9)

    """
        Test un tour du jeu
    """
