from client import Connection
from client import ServerError
from openssl import *
import base64



def connected(username):

	piece = ""
	pieceB = ""
	pieceEncry = ""
	publicKey = ""
	fichierMem = ""
	while True:
		print ("""
		2.Consulter INBOX
		3.Consulter un mail
		6.Envoyer un mail
		17. HelpDesk Police
		18. Consulter ticket police
		19. Consulter piece jointe police
		20. Consulter une deuxieme piece jointe police
		21. XOR entre les deux pieces jointes en mémoire
		22. Fermer un ticket police
		""")
		ans2=input("What would you like to do? ")
		if ans2=="2":
			res = c.get('/home/'+username+'/INBOX')
			print(res)
		elif ans2=="3":
			numMail = input("Numéro du mail? ")
			res = c.get('/home/'+username+'/INBOX/' + str(numMail))
			print(res)
		elif ans2=="6":
			aqui = input("A qui? ")
			sujet = input("Sujet? ")
			contenu = input("Contenu?")
			res = 	c.post('/bin/sendmail', to=aqui, subject=sujet, content=contenu)
			print(res)
		elif ans2=="17":
			res = c.get('/bin/police_hq')
			print(res)
		elif ans2=="18":
			numTicket = input("Numéro du ticket? ")
			res = c.get('/bin/police_hq/ticket/' + str(numTicket))
			print(res)
		elif ans2=="19":
			numTicket = input("Numéro du ticket? ")
			nomPiece = input("Nom de la pièce jointe? ")
			res = c.get('/bin/police_hq/ticket/' + str(numTicket) + '/attachment/' + nomPiece)

			decodeEn64 = input("Voulez-vous décoder la piece jointe en B64? 1=oui")
			if decodeEn64=="1":
				res = base64.b64decode(res)
			print(res)
			pieceJointe = input("Voulez-vous sauvegarder la pièce jointe en mémoire? 1=oui")
			if pieceJointe=="1":
				piece = res
		elif ans2=="20":
			numTicket = input("Numéro du ticket? ")
			nomPiece = input("Nom de la pièce jointe? ")
			res = c.get('/bin/police_hq/ticket/' + str(numTicket) + '/attachment/' + nomPiece)
			res = base64.b64decode(res)
			print(res)
			pieceJointe = input("Voulez-vous sauvegarder la pièce jointe en mémoire? 1=oui")
			if pieceJointe=="1":
				pieceB = res
		elif ans2=="21":

			binaire = "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
			b = bytearray()
			b.extend(map(ord, binaire))
			xorAB = bytearray()
			xorABZ = bytearray()

			for idx, value in enumerate(piece):
				byte = piece[idx] ^ pieceB[idx]
				xorAB.append(byte)
				abz = byte ^ b[idx]
				xorABZ.append(abz)
			print(xorAB)
			print("\n-------\n")
			print(xorABZ)
			print("\n*****************\n")
			print(type(xorABZ))
			clair = xorABZ.decode('latin-1')
			print(clair)
			print("\n********************\n")

		elif ans2=="22":
			numTicket = input("Numéro du ticket? ")
			res = c.post('/bin/police_hq/ticket/' + str(numTicket) + '/close', confirm=True)
			print(res)

		elif ans2 !="":
		  print("\n Not Valid Choice Try again")

if __name__ == '__main__':

	c = Connection("http://pac.fil.cool/uglix")

	while True:
		print ("""
		2.Connect en CHAP
		""")
		ans=input("What would you like to do? ")
		if ans =="2":
			login = input("Login: ")
			mdp = input("MDP: ")
			dictio = c.get('/bin/login/CHAP')
			challenge = dictio.get("challenge")
			plaintext = login + "-" + challenge
			reponse = encrypt(plaintext, mdp)
			res = c.post('/bin/login/CHAP', user=login, response=reponse)
			print(res)
			connected(login)
		elif ans !="":
		  print("\n Not Valid Choice Try again")
