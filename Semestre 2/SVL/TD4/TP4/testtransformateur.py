"""
Test transformateur de log
    Objet :
        - Fichier log
                * un message de log par ligne
        - Message de log
                * date (yyyy-mm-dd)
                * priorité de 0 a 10
                * contenu du message (sans , )
                ! des , entre chaque contenu ET  \n à la fin des lignes
    Fonctionnalité :
        -  conserver les messages dont la priorité est supérieur à
                -----TEST-----
            * si priorité est supérieur à 5
            * si priorité est inférieur à 5
            * si pas de messages
                --------------
        -  lire les messages d'un fichier log
                -----TEST-----
            * le fichier existe ?
            * le fichier est bien formaté ?
            * droit de lecture ?
                --------------
        -  ecrire les messages dans un nouveau fichier log
"""
import unittest
from mockito import *
from transformateur import *
import io
"""
    class test sur le lecteur de fichier log
"""
class TestTransformateur(unittest.TestCase):

    def setUp(self):
        self.lecteur = mock()
        self.redacteur =  mock()
        self.transformateur = Transformateur(self.lecteur, self.redacteur)

    def test_conserver_message_priorite_10(self):

        message = Message("2010-02-25",10,"error in database")
        messages = [message]
        messages = self.transformateur.filter_message(messages)
        self.assertEqual(message in messages, True)

    def test_conserver_message_priorite_4_non_conserve(self):

        message = Message("2010-02-25",4,"error in database")
        messages = [message]
        messages = self.transformateur.filter_message(messages)
        self.assertEqual(message in messages, False)

    def test_conserver_pas_de_message(self):
        messages = []
        messages = self.transformateur.filter_message(messages)
        self.assertEqual(messages, [])

class TestLecteur(unittest.TestCase):

    def setUp(self):
        self.date = "2010-02-25"
        self.priorite = 10
        self.contenu = "error in database"
        self.ligne = "2010-02-25, 10, error in database\n"
        self.ligne_f_1 = "aerkdeajo paekzk k kakakke"
        self.ligne_f_2 = "azerarn, 10, error in database\n"
        self.ligne_f_3 = "2010-02-25, sdmfkgj, error in database\n"
        self.fabrique_message = mock()
        self.message = mock()

    def test_lire_ligne_vide(self):
        when(self.fabrique_message).creer_msg(self.date, self.priorite, self.contenu).thenReturn(self.message)
        flux = io.StringIO("")
        lecteur = Lecteur(flux, self.fabrique_message)
        messages = lecteur.lire_fichier()
        self.assertEqual(len(messages),0 )

    def test_lire_ligne_fichier(self):
        when(self.fabrique_message).creer_msg(self.date, self.priorite, self.contenu).thenReturn(self.message)
        flux = io.StringIO(self.ligne)
        lecteur = Lecteur(flux, self.fabrique_message)
        messages = lecteur.lire_fichier()
        self.assertEqual(messages[0], self.message)

    def test_format_ligne_incorrecte(self):
        flux = io.StringIO(self.ligne_f_1)
        lecteur = Lecteur(flux, self.fabrique_message)
        self.assertRaises(FormatLigneError, lecteur.valid_ligne, self.ligne_f_1)

    def test_format_ligne_date_incorrecte(self):
        flux = io.StringIO(self.ligne_f_2)
        lecteur = Lecteur(flux, self.fabrique_message)
        self.assertRaises(DateFormatError, lecteur.valid_ligne, self.ligne_f_2)

    def test_format_ligne_priorite_incorrecte(self):
        flux = io.StringIO(self.ligne_f_3)
        lecteur = Lecteur(flux, self.fabrique_message)
        self.assertRaises(PrioriteError, lecteur.valid_ligne, self.ligne_f_3)
