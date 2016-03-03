"""
Class Bibliothèque
"""

class ServiceEmprunt:
	def __init__(self, les_emprunts):
		self.fabrique_emprunt = les_emprunts

	def emprunter(self, livre, membre):
		if not livre.estEmpruntable():
			raise LivreNonEmpruntableError()
		if not membre.peutEmprunter():
			raise QuotaAtteintError()
		# pas de new en interne : (ne pas faire) emprunt = Emprunt(livre, membre)
		return self.fabrique_emprunt.creer_emprunt(livre, membre)

	def rendre_livre(self, livre, membre):

		emprunt = self.fabrique_emprunt.get_emprunt(livre, membre)
		return emprunt.cloturer_emprunt(livre, membre)

class LivreNonEmpruntableError(Exception):
	pass

class QuotaAtteintError(Exception):
	pass

class DateDepasseeEmpruntError(Exception):
	pass

class Livre:
	"""
	>>>livre = Livre()
	>>>livre.estEmpruntable()
	True
	"""
	pass

class Membre:
	"""
	>>>membre = Membre()
	>>>membre.peutEmprunter()
	True
	"""
