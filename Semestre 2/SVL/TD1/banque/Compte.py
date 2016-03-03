"""
Application bancaire : comptes 
""" 
class Compte():
		
	def __init__(self):
		""" Initialise le compte avec un solde à zéro """
		self.solde = 0.0
		self.operations = []

	def crediter(self, montant):
		""" Crédite le compte avec un certain montant """
		if montant <= 0.0 :
			raise MontantIncorrectError()
		self.operations.append(montant)

	def debiter(self, montant):
		""" Débite le compte avec un certain montant """
		if montant <= 0.0 :
			raise MontantIncorrectError()
		self.operations.append(-montant)

	def calculer_solde(self):
		""" Fait les operations (debiter/crediter) les unes après les autres """
		montantTmp = self.solde	
		for operation in self.operations:
			montantTmp += operation
		if montantTmp < 0.0 :
			raise SoldeInsuffisantError()
		else : 
			self.operations = []
			self.solde = montantTmp

class MontantIncorrectError(Exception):
	pass

class SoldeInsuffisantError(Exception):
	pass