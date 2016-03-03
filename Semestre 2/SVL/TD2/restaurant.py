#Restaurant d'entreprise
#Fonctionnalité
#Caisse :
#	- visualiser le solde de la carte
#	- visualiser le nombre de tickets Restaurant
#	- visualiser la valeur d'un ticket
#	- payer un repas sans ticket
#	- payer un repas avec un ticket

"""
	- visualiser le solde de la carte
	-- cas nominal : solde caisse = solde carte
	-- pas de carte insérée : erreur

	- payer un repas sans ticket
	-- nominal : la carte est débitée
	-- pas assez d'argent sur la carte : erreur
	-- pas de carte insérée : erreur
	-- erreur prix repas
"""
class Caisse:
	"""
	On peut créer une caisse.
	>>> caisse = Caisse()

	et on ne peut rine faire avant d'avoir inséré une carte
	>>> caisse.solde()
	Traceback (most recent call  last ):
	...
	restaurant.CarteManquanteError

	Une fois la carte insérée on peut consulter son solde.
	>>> carte = Carte()
	>>> caisse.inserer_carte(carte)
	>>> caisse.solde()
	0.0

	On peut payer un repas sans ticket

	nominal
	>>> ...

	pas assez d'argent
	>>> ...
	"""

	def __init__(self):
		self.carte = None

	def raise_carte_manquante(self):
		if self.carte == None :
			raise CarteManquanteError()

	def inserer_carte(self, carte):
		self.carte = carte

	def solde(self):
		self.raise_carte_manquante()
		# LE_SOLDE = 10
		return self.carte.solde()

	def payer_repas_sans_ticket(self, montant):
		self.carte.debiter(montant)

	def ticket(self):
		self.raise_carte_manquante()
		return self.carte.ticket()

	def valeur_ticket(self):
		self.raise_carte_manquante()
		return self.carte.valeur_ticket()

	def payer_repas_avec_ticket(self, montant):
		self.carte.debiter_ticket(montant)

class Carte:
	"""
	On peut consulter le solde de la carte.
	>>> carte = Carte()
	>>> carte.solde()
	0.0

	>> carte.debiter(5)

	On peut consulter le nombre de ticket de la carte.
	>>> carte = Carte()
	>>> carte.ticket()
	0

	>> carte.debiter_ticket(montant)
	...
	"""
	def __init__(self, solde, ticket, valeur_ticket):
		self.solde = solde
		self.ticket = ticket
		self.valeur_ticket = valeur_ticket

	def debiter(self, montant):
		if self.solde < montant :
			raise SoldeInsuffisantError
		if montant < 0 :
			raise MontantIncorrectError
		self.solde -= montant

	def debiter_ticket(self, montant):
		if self.ticket == 0 :
			raise TicketInsuffisantError
		montantTmp = montant
		self.ticket -= 1
		montantTmp = montant - self.valeur_ticket
		self.solde -= montantTmp

class CarteManquanteError(Exception):
	pass

class SoldeInsuffisantError(Exception):
	pass

class TicketInsuffisantError(Exception):
	pass

class MontantIncorrectError(Exception):
	pass
