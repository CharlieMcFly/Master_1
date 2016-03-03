# SVL 1516 - M. Nebut - 02/2016
# CTD6 - test d'acceptation avec Selenium

from selenium import webdriver
import unittest

class TestPageAccueil(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.navigateur = webdriver.Firefox()
        cls.navigateur.get('http://localhost:8080')

    @classmethod
    def tearDownClass(cls):
        cls.navigateur.quit()
        
    def test_la_page_a_un_titre(self):
        titre = self.navigateur.title
        
        self.assertEqual(titre, "accueil")

    def test_la_page_contient_un_lien_qui_a_une_URL(self):
        self.lien = self.navigateur.find_element_by_id('id_lien_tranformateur_temperature')
        url = self.lien.get_attribute('href')

        self.assertEqual(url, "http://localhost:8080/temperature")


class TestPageTemperature(unittest.TestCase):
# à tester : élements html de la page
# titre de la page
# texte
# boîte de saisie

    def test_la_page_contient_une_boite_de_saisie(self):
        self.navigateur = webdriver.Firefox()
        self.navigateur.get('http://localhost:8080/temperature')
        self.boite = self.navigateur.find_element_by_id('id_boite_saisie_valeur_celsius')
        type = self.boite.get_attribute('type')
        self.navigateur.quit()
        self.assertEqual("text", type)


class TestCalculTemperature(unittest.TestCase):
# à tester :
# - cas d'erreur : afficahge message erreur
# - cas nominal : affichage valeur 

    @classmethod
    def setUpClass(cls):
        cls.navigateur = webdriver.Firefox()
        cls.navigateur.get('http://localhost:8080/temperature')

    @classmethod
    def tearDownClass(cls):
         cls.navigateur.quit()

    def test_la_valeur_entree_est_erronee_affichage_message_erreur(self):        
         self.boite = self.navigateur.find_element_by_id('id_boite_saisie_valeur_celsius')
         self.boite.send_keys("&é(\n")
         self.message = self.navigateur.find_element_by_id('id_message_valeur_erronee')

         self.assertEqual(self.message.text, "valeur erronée")
