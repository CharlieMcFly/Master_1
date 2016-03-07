from selenium import webdriver
import unittest

class TestPageAccueilMonEssai(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.navigateur = webdriver.Firefox()

    @classmethod
    def tearDownClass(cls):
        cls.navigateur.quit()

    # DEMO
    def test_la_page_d_accueil_a_un_titre(self):
        self.navigateur.get('http://localhost:8080')
        titre = self.navigateur.title
        
        self.assertEqual(titre, "Accueil")

    def test_le_lien_temperature_a_un_texte(self):
        self.navigateur.get('http://localhost:8080')
        lien_temperature = self.navigateur.find_element_by_id('id_lien_temperature')
        texte = lien_temperature.get_attribute('text')        

        self.assertEqual(texte, 'Transformateur de température')

    # DEMO
    def test_le_lien_temperature_a_une_url(self):
        self.navigateur.get('http://localhost:8080')
        lien_temperature = self.navigateur.find_element_by_id('id_lien_temperature')
        url = lien_temperature.get_attribute('href')

        self.assertEqual(url, self.navigateur.current_url + 'temperature')

class TestPageTemperature(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.navigateur = webdriver.Firefox()
        cls.navigateur.get('http://localhost:8080/temperature')
    
    @classmethod
    def tearDownClass(cls):
        cls.navigateur.quit()

    def test_la_page_a_un_titre(self):        
        titre = self.navigateur.title
        
        self.assertEqual(titre, "Transformation de températures")

    def test_la_page_contient_un_formulaire_post(self):
        formulaire = self.navigateur.find_element_by_id('id_formulaire_temperature')
        self.assertEqual(formulaire.get_attribute('method'), 'post')
        
    def test_la_page_contient_un_formulaire_qui_reste_sur_temperature(self):
        formulaire = self.navigateur.find_element_by_id('id_formulaire_temperature')
        action = formulaire.get_attribute('action')
        self.assertEqual(action, 'http://localhost:8080/temperature')

    # DEMO ?
    def test_la_page_contient_une_boite_de_saisie_de_type_text(self):
        boite_saisie = self.navigateur.find_element_by_id('id_boite_saisie_temperature')
        type = boite_saisie.get_attribute('type')
        self.assertEqual(type, 'text')

class TestValiderLeFormulairePourConvertirUneTemperature(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.navigateur = webdriver.Firefox()
        cls.navigateur.get('http://localhost:8080/temperature')
    
    @classmethod
    def tearDownClass(cls):
        cls.navigateur.quit()

    # DEMO
    def test_convertir_un_format_errone_affiche_un_message_d_erreur(self):
        boite_saisie = self.navigateur.find_element_by_id("id_boite_saisie_temperature")
        boite_saisie.send_keys("dix\n")
        resultat = self.navigateur.find_element_by_id("id_response_label")
        # valeur = resultat.get_attribute('text') # pas équivalent
        valeur = resultat.text
        self.assertEqual(valeur, "valeur incorrecte")
        
    def test_convertir_un_format_erronne_propose_toujours_la_boite_de_saisie(self):
        boite_saisie = self.navigateur.find_element_by_id("id_boite_saisie_temperature")
        boite_saisie.send_keys("dix\n")
        boite_saisie = self.navigateur.find_element_by_id("id_boite_saisie_temperature")
        self.assertEqual(boite_saisie.text, '')

    # DEMO
    def test_convertir_une_temperature_correcte_affiche_le_resultat(self):
        boite_saisie = self.navigateur.find_element_by_id("id_boite_saisie_temperature")
        boite_saisie.send_keys("100\n")
        resultat = self.navigateur.find_element_by_id("id_response_label")
        valeur = resultat.text
        self.assertEqual(valeur, "100.0 celsius valent 212.0 farhenheit")
        
