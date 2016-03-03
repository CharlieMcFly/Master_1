#SVL 1516
#CTD4 - C. Quetstroey

#Scénarios à tester

# fonctionnalité : le jeu
# le joueur gagne du premier coupe
# le joueur gagne en plusiseurs coups
# le joueur gagne en exactement N coups
# le joueur perd
import unittest
from mockito import *
class TestJeuDevinerUnNombre(unittest.TestCase):

    def setUp(self):
        pass

    def test_le_joueur_gagne_du_premier_coup(self):
        A_DEVINER = 4
        generateur_nombre_entre_0_et_9 = mock()
        when(self.generateur_nombre_entre_0_et_9).genere_nombre_a_deviner().thenReturn(A_DEVINER)

        lecteur = mock()
        when(lecteur).lire_un_nombre().thenReturn(A_DEVINER)

        afficheur = mock()

        jeu = JeuDevinerUnNombre(self.generateur_nombre_entre_0_et_9)
        jeu.jouer()

        verify(afficheur).notifier_joueur_a_gagne()

    def test_le_joueur_gagne_en_plusieurs_coups(self):
        A_DEVINER = 4
        TROP_PETIT = 3
        TROP_GRAND = 6
        generateur_nombre_entre_0_et_9 = mock()
        when(generateur_nombre_entre_0_et_9).genere_nombre_a_deviner().thenReturn(A_DEVINER)
        lecteur = mock()
        when(lecteur).lire_un_nombre().thenReturn(TROP_PETIT).thenReturn(TROP_GRAND).thenReturn(A_DEVINER)
        afficheur = mock()
        jeu = JeuDevinerUnNombre(generateur_nombre_entre_0_et_9, afficheur)
        jeu.jouer()
        inorder.verify(afficheur, time=3).notifier_invitation_choisir_un_nombre()
        inorder.verify(afficheur).notifier_nombre_trop_petit()
        inorder.verify(afficheur, time=3).notifier_invitation_choisir_un_nombre()
        inorder.verify(afficheur).notifier_nombre_trop_grand()
        inorder.verify(afficheur, time=3).notifier_invitation_choisir_un_nombre()
        inorder.verify(afficheur).notifier_joueur_a_gagne()


"""
Fonctionnalités à tester : lire un nombre
   nominal : renvoie bien un nombre entre 0 et 9
       correspondant à l'entée au clavier
   exception : échec si entrée erronée
"""
import io

class TestLecteur(unittest.TestCase):

    def test_le_nombre_retourne_correspond_a_l_entree(self):
        flot_entree = io.StringIO("5\n")
        lecteur = LecteurSurEntreeStandard(flot_entree)
        self.assertEqual(lecteur.lire_un_nombre(), 5)

class TestIntegration:

    def test_joueur_avec_un_vrai_lecteur(self):
        A_DEVINER = 4
        generateur_nombre_entre_0_et_9 = mock()
        when(generateur_nombre_entre_0_et_9).genere_nombre_a_deviner().thenReturn(A_DEVINER)

        lecteur = LecteurSurEntreeStandard()

        afficheur = mock()

        jeu = JeuDevinerUnNombre(generateur_nombre_entre_0_et_9, lecteur, afficheur)
        jeu.jouer()

        verify(afficheur).notifier_invitation_choisir_un_nombre()
        verify(afficheur).notifier_joueur_a_gagne()
