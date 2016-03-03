from mockito import *
import unittest
from restaurant import *
class TestVisualiserSoldeCaisse(unittest.TestCase):

	def setUp(self):
		caisse = Caisse()

	def test_visualiser_solde_carte(self):
		LE_SOLDE = 10
		# carte = Carte()
		# remplacer par une "fausse carte"
		# carte = MockCarte(LE_SOLDE) à la main
		carte = mock()
		when(carte).solde().thenReturn(LE_SOLDE)
		self.caisse.inserer_carte(carte)
		self.assertEqual(self.caisse.solde(), LE_SOLDE )

	def test_visualiser_solde_sans_carte_echoue(self):
		self.assertRaises(CarteManquanteError, self.caisse.solde)

	def test_visualiser_nombre_ticket_restaurant(self):
		NB_TICKET = 2
		#
		carte = mock()
		when(carte).ticket().thenReturn(NB_TICKET)
		self.caisse.inserer_carte(carte)
		self.assertEqual(caisse.ticket(), NB_TICKET )

	def test_visualiser_ticket_sans_carte_echoue(self):
		self.assertRaises(CarteManquanteError, self.caisse.ticket)

	def test_visualiser_valeur_ticket(self):
		VAL_TICKET = 5.8
		#
		carte = mock()
		when(carte).valeur_ticket().thenReturn(VAL_TICKET)
		self.caisse.inserer_carte(carte)
		self.assertEqual(self.caisse.valeur_ticket(), VAL_TICKET)

	def test_visualiser_valeur_ticket(self):
		self.assertRaises(CarteManquanteError, caisse.valeur_ticket)


class TestPayerUnRepasSansTicket(unittest.TestCase):

	def test_la_caisse_debite_la_carte(self):
		caisse = Caisse()
		carte = mock()
		caisse.inserer_carte(carte)
		#
		REPAS = 7.0
		caisse.payer_repas_sans_ticket(REPAS)
		# verify ne va rien faire si c'est le bon caractère
		# ne pas faire d'assertEqual
		verify(carte).debiter(REPAS)

	def test_pas_suffisamment_d_argent_le_paiement_echoue(self):
		caisse = Caisse()
		carte = mock()
		caisse.inserer_carte(carte)
		#
		REPAS = 7.0
		when(carte).debiter(REPAS).thenRaise(SoldeInsuffisantError)
		self.assertRaises(SoldeInsuffisantError, caisse.payer_repas_sans_ticket, REPAS)

class TestPayerUnRepasAvecTicket(unittest.TestCase):

	def setUp(self):
		self.caisse = Caisse()

	def test_la_caisse_debite_la_carte(self):
		carte = mock()
		self.caisse.inserer_carte(carte)
		#
		REPAS = 5.0
		self.caisse.payer_repas_avec_ticket(REPAS)
		#
		verify().debiter_ticket(REPAS)

	def test_nombre_ticket_insuffisant(self):
		carte = mock()
		self.caisse.inserer_carte(carte)
		#
		REPAS = 5.0
		#
		when(carte).debiter_ticket(REPAS).thenRaise(TicketInsuffisantError)
		self.assertRaises(TicketInsuffisantError, self.caisse.payer_repas_avec_ticket, REPAS)

class TestCarte(unittest.TestCase):

	def test_solde_carte(self):
		carte = Carte(0.0, 0, 2.0)
		self.assertEqual(carte.solde, 0.0)

	def test_debiter_montant_de_la_carte_sans_ticket(self):
		carte = Carte(5.0, 0, 2.0)
		REPAS = 3.0
		carte.debiter(REPAS)
		self.assertEqual(carte.solde, 2.0)

	def test_debiter_carte_sans_ticket_solde_insuffisant(self):
		carte = Carte(5.0, 0, 2.0)
		REPAS = 7.0
		self.assertRaises(SoldeInsuffisantError, carte.debiter, REPAS)

	def test_debiter_carte_montant_incorrect(self):
		carte = Carte(5.0, 0, 2.0)
		REPAS = -5.0
		self.assertRaises(MontantIncorrectError, carte.debiter, REPAS)

	def test_ticket_carte(self):
		carte = Carte(0.0, 5, 2.0)
		self.assertEqual(carte.ticket, 5)

	def test_valeur_ticket(self):
		carte = Carte(0.0, 5, 3.0)
		self.assertEqual(carte.valeur_ticket, 3.0)

	def test_debiter_montant_avec_ticket(self):
		carte = Carte(5.0, 2, 3.0)
		REPAS = 5.0
		carte.debiter_ticket(REPAS)
		self.assertEqual(carte.solde, 3.0)

	def test_debiter_montant_avec_ticket_insuffisant(self):
		carte = Carte(5.0, 0, 3.0)
		REPAS = 5.0
		self.assertRaises(TicketInsuffisantError, carte.debiter_ticket, REPAS)


# pas utiliser ici
class MockCarte:
	"""
	Pour mock manuel
	"""
	def __init__(self, montant):
		self.montant = montant

	def solde(self):
		return self.montant
