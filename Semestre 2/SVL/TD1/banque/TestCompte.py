"""
Test banque
demo SVL CTD1 - Charlie Q - 1516
"""
#que teste-t-on?
# - création d'un compte
# 	* avec solde null
#	* avec solde paramétré
# - créditer
# 	*cas nominal : mettre à jour le solde
# - débiter
# - consultation du solde
import unittest
from Compte import Compte
from Compte import MontantIncorrectError
from Compte import SoldeInsuffisantError
class TestCompte(unittest.TestCase):

	def test_un_compte_est_cree_avec_solde_nul(self):
		compte = Compte()
		self.assertEqual(compte.solde, 0.0)

	def test_crediter_un_compte_augmente_son_solde(self):
		compte = Compte()
		compte.crediter(20.0)
		compte.calculer_solde()
		self.assertEqual(compte.solde, 20.0)

	def test_le_montant_est_positif_crediter(self):
		compte = Compte()
		#compte.crediter(-10.0)
		self.assertRaises(MontantIncorrectError, compte.crediter, -10.0)

	def test_le_montant_est_strictement_positif_crediter(self):
		compte = Compte()
		self.assertRaises(MontantIncorrectError, compte.crediter, 0.0)

	def test_on_peut_crediter_plusieurs_fois(self):
		compte = Compte()
		compte.crediter(10.0)
		compte.crediter(30.0)
		compte.calculer_solde()
		self.assertEqual(compte.solde, 40.0)

	def test_debiter_un_compte_diminue_son_solde(self):
		compte = Compte()
		compte.crediter(10.0)
		compte.debiter(5.0)
		compte.calculer_solde()
		self.assertEqual(compte.solde, 5.0)

	def test_on_ne_peut_pas_debiter_avec_solde_insuffisant(self):
		compte = Compte()
		compte.crediter(10.0)
		compte.debiter(20.0)
		self.assertRaises(SoldeInsuffisantError, compte.calculer_solde)

	def test_le_montant_est_positif_debiter(self):
		compte = Compte()
		#compte.debiter(-10.0)
		self.assertRaises(MontantIncorrectError, compte.debiter, -10.0)

	def test_le_montant_est_strictement_positif_debiter(self):
		compte = Compte()
		self.assertRaises(MontantIncorrectError, compte.debiter, 0.0)

	def test_on_peut_debiter_plusieurs_fois(self):
		compte = Compte()
		compte.crediter(60.0)
		compte.debiter(30.0)
		compte.debiter(20.0)
		compte.calculer_solde()
		self.assertEqual(compte.solde, 10.0)

if __name__ == '__main__':
	unittest.main()