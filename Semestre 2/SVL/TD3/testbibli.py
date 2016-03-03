""" 
	Fonctionnalité de l'emprunt :
	- emprunter un livre
		- si le livre n'est pas empruntable l'emprunt echoue
		- si le membre a atteint son quota l'emprunt echoue
		- sinon 
			- un emprunt est créeé et disponible pour l'affichage
	- rendre un livre
		- vérifier le livre
		- vérifier la date
	- signaler un litige

Pattern
	factory fabriq
	injection des dépendances

"""
from mockito import *
import unittest
from bibli import *
class TestEmprunt(unittest.TestCase) :

	def setUp(self):
		self.livre = mock()
		self.membre =mock()
		self.fabrique_emprunt = mock()
		self.emprunt = mock()
		self.service_emprunt = ServiceEmprunt(self.fabrique_emprunt)

	def test_livre_consultable_uniquement_l_emprunt_echoue(self):
		when(self.livre).estEmpruntable().thenReturn(False)
		self.assertRaises(LivreNonEmpruntableError, self.service_emprunt.emprunter, self.livre, self.membre)

	def test_le_membre_a_atteint_son_quota_l_emprunt_echoue(self):
		when(self.livre).estEmpruntable().thenReturn(True)
		when(self.membre).peut_emprunter().thenReturn(False)
		self.assertRaises(QuotaAtteintError, self.service_emprunt.emprunter, self.livre, self.membre)

	def test_l_emprunt_est_cree(self):
		when(self.livre).estEmpruntable().thenReturn(True)
		when(self.membre).peutEmprunter().thenReturn(True)
		when(self.fabrique_emprunt).creer_emprunt(self.livre, self.membre).thenReturn(self.emprunt)
		self.assertEqual(self.service_emprunt.emprunter(self.livre, self.membre), self.emprunt)

	def test_rendre_livre_date_depassee(self):
		when(self.fabrique_emprunt).get_emprunt(self.livre, self.membre).thenReturn(self.emprunt)
		when(self.emprunt).cloturer_emprunt(self.livre, self.membre).thenRaise(DateDepasseeEmpruntError)
		self.assertRaises(DateDepasseeEmpruntError, self.service_emprunt.rendre_livre, self.livre, self.membre)

	def test_lemprunt_est_cloturer(self):
		when(self.fabrique_emprunt).get_emprunt(self.livre, self.membre).thenReturn(self.emprunt)
		when(self.emprunt).cloturer_emprunt(self.livre, self.membre).thenReturn(True)
		self.assertEqual(self.service_emprunt.rendre_livre(self.livre, self.membre), True)