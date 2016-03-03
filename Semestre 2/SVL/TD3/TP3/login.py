"""
Class Login
	permet de créer un utilisateur de 2 façons :
		- créer un utilisateur avec son nom, prenom et un login.
		- créer un utilisateur en utilisant un plan A ou un plan B
"""

class Login :

	def __init__(self, utilisateurs):
		self.utilisateurs = utilisateurs

	"""
		Creer le login à partir des données (nom, prénom) plan B
	"""
	def creation_login_A(self, nom, prenom):
		login = nom
		if len(nom) > 8 :
			login = nom[0:8]

		if self.utilisateurs.login_deja_pris() == True :
			login = self.creation_login_B(nom, prenom)

		return login.lower()

	"""
		Creer le login à partir des données (nom, prenom) plan B
	"""
	def creation_login_B(self, nom, prenom):

		login = nom+''+prenom[0]
		if len(nom) > 7 :
			login = nom[0:7]+''+prenom[0]

		return login.lower()

	"""
		Validation des inputs (nom, prenom)
	"""
	def valid_input(self, nom, prenom):

		if nom == None or nom == "":
			raise NomVideError()
		if prenom == None or prenom == "":
			raise PrenomVideError()
		if not isinstance(nom, str) :
			raise NomPasUneChaineDeCaractereError()
		if not isinstance(prenom, str):
			raise PrenomPasUneChaineDeCaractereError()

	"""
		Validation de l'input login
	"""
	def valid_login(self, login):
		if login == None :
			raise LoginVideError()
		if len(login) > 8 :
			raise LoginTropLongError()
		return login.lower()

	"""
		Permet de créer un utilisateur avec son nom, prenom et un login.
	"""
	def creer_utilisateur(self, login, nom, prenom):

		login = self.valid_login(login)
		self.valid_input(nom, prenom)

		return self.utilisateurs.creer_user(login, nom, prenom)

	def creer_user_meme_pas_peur(self, nom, prenom):

		self.valid_input(nom, prenom)
		login = self.creation_login_A(nom, prenom)

		return self.utilisateurs.creer_user(login, nom, prenom)

class LoginVideError(Exception):
	pass

class LoginDejaPrisError(Exception):
	pass

class LoginTropLongError(Exception):
	pass

class NomVideError(Exception):
	pass

class PrenomVideError(Exception):
	pass

class NomPasUneChaineDeCaractereError(Exception):
	pass

class PrenomPasUneChaineDeCaractereError(Exception):
	pass
