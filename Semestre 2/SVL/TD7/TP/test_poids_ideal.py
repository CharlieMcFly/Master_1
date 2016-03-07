from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from mockito import *
import unittest
from poids_ideal import *


"""
    Test si la méthode calculer poids ideal est correcte pour les 2 sexes
"""
class TestCalculPoidsIdeal(unittest.TestCase):

    def setUp(self):
        self.poidsIdeal = PoidsIdeal()

    def test_calculer_poids_homme(self):
        res = self.poidsIdeal.calculer_poids_ideal(1, "homme")
        self.assertEqual(res, 12.5)

    def test_calculer_poids_femme(self):
        res = self.poidsIdeal.calculer_poids_ideal(2, "femme")
        self.assertEqual(res, 80)

"""
    Test pour la page d'Accueil
"""
class TestPageAccueil(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.navigateur = webdriver.Firefox()
        cls.navigateur.get('http://localhost:8080')

    @classmethod
    def tearDownClass(cls):
        cls.navigateur.quit()

    def test_si_page_a_titre(self):
        titre = self.navigateur.title
        self.assertEqual(titre, "Accueil")

    def test_si_page_contient_formulaire(self):
        self.form = self.navigateur.find_element_by_id('imc_form')
        action = self.form.get_attribute('action')
        self.assertEqual(True, "generate" in action)

    def test_si_page_contient_input_taille(self):
        self.input = self.navigateur.find_element_by_id('imc_input')
        type = self.input.get_attribute('type')
        self.assertEqual("text", type)

    def test_si_page_contient_inputs_sexe(self):
        self.inputs = self.navigateur.find_elements_by_name('sexe')
        for inp in self.inputs:
            type = inp.get_attribute('type')
            self.assertEqual("radio", type)

class TestPageResultat(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.navigateur = webdriver.Firefox()
        cls.navigateur.get('http://localhost:8080/')

    @classmethod
    def tearDownClass(cls):
        cls.navigateur.quit()

    def test_la_page_args_corrects(self):
        self.navigateur.get("http://localhost:8080/generate?taille=2&sexe=homme")
        titre = self.navigateur.title
        self.assertEqual(titre, "Resultat")

    def test_page_resultat_arg_taille_virgule(self):
        self.navigateur.get("http://localhost:8080/generate?taille=1%2C80&sexe=homme")
        titre = self.navigateur.title
        self.assertEqual(titre, "Resultat")

    def test_page_resultat_arg_taille_point(self):
        self.navigateur.get("http://localhost:8080/generate?taille=1%2C80&sexe=homme")
        titre = self.navigateur.title
        self.assertEqual(titre, "Resultat")

    def test_page_resultat_sans_argument(self):
        self.navigateur.get("http://localhost:8080/generate")
        titre = self.navigateur.title
        self.assertEqual(titre, "Erreur")

    def test_page_resultat_mauvais_argument_taille_string(self):
        self.navigateur.get("http://localhost:8080/generate?taille=troll&sexe=homme")
        titre = self.navigateur.title
        self.assertEqual(titre, "Erreur")

    def test_page_resultat_arg_sexe_incorrect(self):
        self.navigateur.get("http://localhost:8080/generate?taille=1%2C80&sexe=other")
        titre = self.navigateur.title
        self.assertEqual(titre, "Erreur")
