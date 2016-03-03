"""
Login
	- fonctionnalité :
		- creation de login :
			- Plan A : Login composé des 8 premieres lettres du nom
				- si fail : login deja pris echoue
			- Plan B :  Login composé des 7 premieres lettres du nom + initial prénom
				- si fail : l'admin se débrouille

		- creation d'un utilisateur dans la base à partir de ses noms, preom et login
		- same mais calculé automatiquement à partir des regles présentées plus haut.

"""
from mockito import *
import unittest
from login import *

class TestLogin(unittest.TestCase):

	def setUp(self):
		self.fabrique_utilisateur = mock()
		self.login = Login(self.fabrique_utilisateur)
		self.utilisateur = mock()
		self.login_correct = "quetstro"
		self.login_plan_B = "cquetstr"
		self.login4 = "azer"
		self.login10 = "azertyuiop"
		self.nom10 =  "quetstroey"
		self.nomMAJ = "QUETSTROEY"
		self.loginV = None
		self.prenom = "charlie"
		self.nom = "aaa"
		self.nomV = None
		self.prenomV = None
		self.nom_pas_chaine = 12
		self.prenom_pas_chaine = 12
		self.loginMAJ="MACFLY"

	"""
		Test sur la premiere façon de créer des utilisateurs
	"""

	def test_utilisateur_login_compose_de_plus_de_huit_lettre_echoue(self):
		self.assertRaises(LoginTropLongError, self.login.valid_login, self.login10)

	def test_utilisateur_login_vide_echoue(self):
		self.assertRaises(LoginVideError, self.login.valid_login, self.loginV)

	def test_utilisateur_login_majuscule(self):
		self.assertEqual(self.login.valid_login(self.loginMAJ), "macfly")

	def test_utilisateur_nom_vide_echoue(self):
		self.assertRaises(NomVideError, self.login.valid_input, self.nomV, self.prenom)

	def test_utilisateur_pren_utilisateurom_vide_echoue(self):
		self.assertRaises(PrenomVideError, self.login.valid_input, self.nom, self.prenomV)

	def test_utilisateur_nom_pas_chaine_de_caractere_echoue(self):
		self.assertRaises(NomPasUneChaineDeCaractereError, self.login.valid_input, self.nom_pas_chaine, self.prenom)

	def test_utilisateur_prenom_pas_chaine_de_caractere_echoue(self):
		self.assertRaises(PrenomPasUneChaineDeCaractereError, self.login.valid_input, self.nom, self.prenom_pas_chaine)

	def test_utilisateur_est_cree(self):
		when(self.fabrique_utilisateur).creer_user(self.login_correct, self.nom, self.prenom).thenReturn(self.utilisateur)
		self.assertEqual(self.login.creer_utilisateur(self.login_correct, self.nom, self.prenom), self.utilisateur)

	def test_utilisateur_existe_deja_echoue(self):
		when(self.fabrique_utilisateur).creer_user(self.login_correct, self.nom, self.prenom).thenRaise(LoginDejaPrisError)
		self.assertRaises(LoginDejaPrisError, self.login.creer_utilisateur, self.login_correct, self.nom, self.prenom)
	"""
		Test sur la deuxieme façon de créer des utilisateurs :

			PLAN A

		Creation de login PLAN A
	"""
	def test_plan_A_creation_login_nom_plus_huit(self):
		self.assertEqual(self.login.creation_login_A(self.nom10, self.prenom), "quetstro")

	def test_plan_A_creation_nom_majuscule(self):
		self.assertEqual(self.login.creation_login_A(self.nomMAJ, self.prenom), "quetstro")

	# peut être un test pour tester si le login existe deja ?

	"""
		Creation de login  PLAN B
	"""
	def test_plan_B_creation(self):
		self.assertEqual(self.login.creation_login_B(self.nom10, self.prenom), "quetstrc")

	def test_plan_B_creation_nom_majuscule(self):
		self.assertEqual(self.login.creation_login_B(self.nomMAJ, self.prenom), "quetstrc")

	def test_plan_B_creation_login_deja_pris_echoue(self):
		when(self.fabrique_utilisateur).creer_user(self.login_correct, self.nom, self.prenom).thenRaise(LoginDejaPrisError)
		self.assertRaises(LoginDejaPrisError, self.login.creer_utilisateur, self.login_correct, self.nom, self.prenom)
