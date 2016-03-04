from client import Connection
from client import ServerError
from openssl import *
import base64
import time
import json

def testecho1():
	c = Connection("http://pac.fil.cool/uglix")
	res = c.get('/bin/echo')
	print(res)

def testecho2():
	c = Connection("http://pac.fil.cool/uglix")
	res = c.post('/bin/echo', string_example="toto")
	print(res)

def testlogin():
	c = Connection("http://pac.fil.cool/uglix")
	res = c.post('/bin/login', user='guest', password="guest")
	print(res)

def testhome():
	c = Connection("http://pac.fil.cool/uglix")
	res = c.post('/bin/login', user='guest', password="guest")
	print(res)
	res = c.get('/home/guest')
	print(res)

def testFile1():
	c = Connection("http://pac.fil.cool/uglix")
	res = c.post('/bin/login', user='guest', password="guest")
	print (res)
	res = c.get('/home/guest/NASA-SETI.bin')
	print(res)

def testFile2():
	c = Connection("http://pac.fil.cool/uglix")
	c.post('/bin/login', user='guest', password="guest")
	res = c.get('/home/guest/soundtrack_0.s3m')
	print(res)

def testINBOX():
	c = Connection("http://pac.fil.cool/uglix")
	c.post('/bin/login', user='guest', password="guest")
	res = c.get('/home/guest/INBOX')
	print(res)

def testMail():
	c = Connection("http://pac.fil.cool/uglix")
	c.post('/bin/login', user='guest', password="guest")
	res = c.get('/home/guest/INBOX/266')
	print(res)

def testMailBody():
	c = Connection("http://pac.fil.cool/uglix")
	c.post('/bin/login', user='guest', password="guest")
	res = c.get('/home/guest/INBOX/266/body')
	print(res)

def testMailUnread():
	c = Connection("http://pac.fil.cool/uglix")
	c.post('/bin/login', user='guest', password="guest")
	res = c.get('/home/guest/INBOX/unread')
	print(res)

def testSendMail():
	c = Connection("http://pac.fil.cool/uglix")
	res = c.post('/bin/login', user='guest', password="guest")
	print(res)
	res = 	c.post('/bin/sendmail', to='guest', subject="test", content="coucou")
	print(res)

def testVraiLogin():
	c = Connection("http://pac.fil.cool/uglix")
	res = c.post('/bin/login', user='gritchie', password="Vt*1fJsM7@")
	print(res)
	res = c.get('/home/gritchie')
	print(res)
	res = c.get('/home/gritchie/INBOX')
	print(res)
	res = c.get('/home/gritchie/INBOX/580')
	print(res)

def helpDesk():
	c = Connection("http://pac.fil.cool/uglix")
	res = c.post('/bin/login', user='gritchie', password="Vt*1fJsM7@")
	print(res)
	res = c.get('/bin/crypto_helpdesk')
	print(res)

def helpDesk2():
	c = Connection("http://pac.fil.cool/uglix")
	res = c.post('/bin/login', user='gritchie', password="Vt*1fJsM7@")
	print(res)
	res = c.get('/bin/crypto_helpdesk/ticket/43')
	print(res)

def helpDesk3():
	c = Connection("http://pac.fil.cool/uglix")
	res = c.post('/bin/login', user='gritchie', password="Vt*1fJsM7@")
	print(res)
	res = c.get('/bin/crypto_helpdesk/ticket/43/attachment/fetch-me')
	print(res)


def testSendMail2():
	c = Connection("http://pac.fil.cool/uglix")
	res = c.post('/bin/login', user='gritchie', password="Vt*1fJsM7@")
	print(res)
	a = {'foo':'Company secretary', 'bar':42}
	res = 	c.post('/bin/sendmail', to='pauline.toy', subject="test", content=a)
	print(res)

def testMail2():
	c = Connection("http://pac.fil.cool/uglix")
	res = c.post('/bin/login', user='gritchie', password="Vt*1fJsM7@")
	print(res)
	res = c.get('/home/gritchie/INBOX/3714') # on peut mtn fermer le ticket
	print(res)

def helpDeskCloseTicket():
	c = Connection("http://pac.fil.cool/uglix")
	res = c.post('/bin/login', user='gritchie', password="Vt*1fJsM7@")
	print(res)
	res = c.post('/bin/crypto_helpdesk/ticket/43/close', confirm=True)
	print(res)

def decode64file(path):

	with open(path, 'r') as myfile:
		doc=myfile.read()
	doc_dec = base64.b64decode(doc).decode()
	file = open(path + ".dec", "w")
	file.write(doc_dec)
	file.close()
def xor2files():

	with open("exhiA.decode.bin", 'r') as myfile:
		docA=myfile.read()
	with open("exhiB.decode.bin", 'r') as myfile:
		docB=myfile.read()

	xorAB = bool(docA) != bool(docB)
	file = open("resultAB.bin", "w")
	file.write(xorAB)
	file.close()

def xor_strings(xs, ys):
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(xs, ys))

def xor(m, k):
    """Given strings m and k of characters 0 or 1,
    it returns the string representing the XOR
    between each character in the same position.
    This means that m and k should be of the same length.

    Use this function both for encrypting and decrypting!"""
    r = []
    for i, j in zip(m, k):
        r.append(str(int(i) ^ int(j)))  # xor between bits i and j
    return "".join(r)

def delpi_bancaire():
    correct = True

    res = c.get('/bin/police_hq')
    print(res)

    res = c.get('/bin/police_hq/ticket/317')
    print(res)

    email = c.get('/bin/police_hq/ticket/317/attachment/client')["email"]

    lots = c.get('/bin/banks/forensics')

    identifiant = lots["identifier"]
    cards_data = lots["card-numbers"]

    print(lots)

    status = []

    for card_number in cards_data :

        correct = True

        print("\n")
        card_data = c.get('/bin/banks/card-data/' + card_number)
        """
        Récupération des différents elts
        """


        certi_card = card_data['card-certificate']
        certi_bank = card_data['bank-certificate']

        bank_name = card_data['bank-name']
        card_number = card_data['card-number']
        signature = card_data['signature']
        challenge = card_data['challenge']


        #bank_challenge = card_data["challenge"]
        #bank_signature = card_data["signature"]


        """
        Création des certificats sur le disque
        """
        filename_certi_global = 'global_certi'
        file_key = open(filename_certi_global, 'w')
        file_key.write(c.get('/bin/banks/CA'))
        file_key.close()

        filename_certi_bank = 'bank_certi'
        file_key2 = open(filename_certi_bank, 'w')
        file_key2.write(certi_bank)
        file_key2.close()


        filename_certi_card = 'card_certi'
        file_key3 = open(filename_certi_card, 'w')
        file_key3.write(certi_card)
        file_key3.close()


        """
        Création des pK a partir des certificats
        Verifications des signatures et challenges
        """
        card_publickey = getPublicKeyFromCerti(certi_card)
        bank_publickey = getPublicKeyFromCerti(certi_bank)

        bb = base64.b64decode(signature)
        file_key4 = open('card_signature.bin', 'wb')
        file_key4.write(bb)
        file_key4.close()

        file_key5 = open('card_publickey.pem', 'w')
        file_key5.write(card_publickey)
        file_key5.close()

        """bb = base64.b64decode(bank_signature)
        file_key6 = open('bank_signature.bin', 'wb')
        file_key6.write(bb)
        file_key6.close()

        file_key7 = open('bank_publickey.pem', 'w')
        file_key7.write(bank_publickey)
        file_key7.close()"""

        res_sign = verifSign(challenge, 'card_publickey.pem', 'card_signature.bin')
        if "OK" not in res_sign:
            print("Verification du challenge carte : fail")
            correct = False

        """res_sign = verifSign(bank_challenge, 'card_publickey.pem', 'bank_signature.bin')
        if "OK" not in res_sign:
            print("Verification du challenge banque : fail")
            correct = False"""

        #print(consultCertif(certi_bank))
        #print(consultCertif(certi_card))

        try:
            res = verifyCert(certi_bank, filename_certi_global)
        except OpensslError as e:
            print("Transaction failed : openssl error")
            correct = False
        try:
            res2 = verifyCert(certi_card, filename_certi_global, filename_certi_bank)
        except OpensslError as e:
            print("Transaction failed : openssl error")
            correct = False

        if bank_name not in getCertifName(certi_bank):
            print("Transaction failed : nom de banques différentes")
            correct = False

        if card_number not in getCertifName(certi_card):
            print("Transaction failed : numero de carte différentes")
            correct = False


        if "error" in res or "error" in res2 :
            print("Transaction error pour openssl")
            correct = False



        if correct == True:
            print("Transaction correcte")
            status.append(True)
        else:
            status.append(False)

    message = {"identifier":identifiant,"statuses":status}
    res = c.post('/bin/sendmail', to=email, subject='fermeture ticket', content=message )
    print(res)

def connection_kerberos(ticket):

	  # Authentification service

	  dic = c.post('/bin/kerberos/authentication-service', username="gritchie")
	  tgs = dic["Client-TGS-session-key"]
	  tgt = dic["TGT"]
	  mdp = "Vt*1fJsM7@"
	  pw = decrypt(tgs, mdp)
	  #  print('password : '+pw)
	  #   Authentificateur
	  d = {'username': 'gritchie', 'timestamp': time.time()}
	  e = json.dumps(d)
	  auth = encrypt(e, pw)
	  # Ticket granting service
	  dic2 = c.post('/bin/kerberos/ticket-granting-service', TGT=tgt, service="hardware", authenticator=auth)
	  sesskey = dic2['Client-Server-session-key']
	  servtick = dic2['Client-Server-ticket']
	  cle = decrypt(sesskey, pw)
	  #  Connection service
	  d2 = {'username': 'gritchie', 'timestamp': time.time()}
	  e2 = json.dumps(d2)
	  auth2 = encrypt(e2, cle)
	  serv = c.post('/service/hardware/hello', ticket=servtick, authenticator=auth2)
	  print(serv)
def connected():

	piece = ""
	pieceB = ""
	pieceEncry = ""
	publicKey = ""
	fichierMem = ""
	while True:
		print ("""
		1.Consulter le helpdesk
		2.Consulter INBOX
		3.Consulter un mail
		4.Consulter un ticket
		5.Consulter une pièce jointe
		6.Envoyer un mail
		7.Encrypter la pièce en mémoire
		8.Fermer un ticket
		9.Decrypter la pièce en mémoire
		10.Sauvegarder la clé publique en mémoire
		11.Encrypter la pièce en mémoire avec ma clé publique en mémoire
		12.Finger et sauver public key du user en mémoire
		13.Put Public Key in home
		14. Encrypter une phrase avec la Public Key en mémoire
		15. Envoyer un fichier en hybride
		16. Sauver un fichier un mémoire
		17. Police
		18. Consulter ticket police
		19. Consulter piece jointe police
		20. Consulter une deuxieme piece jointe police
		21. XOR entre les deux pieces jointes en mémoire
		22. Fermer un ticket police
		23. Lancer le delpi pourri
		24. Lancer kerkberos
		""")
		ans2=input("What would you like to do? ")
		if ans2=="1":
			res = c.get('/bin/crypto_helpdesk')
			print(res)
		elif ans2=="2":
			res = c.get('/home/gritchie/INBOX')
			print(res)
		elif ans2=="3":
			numMail = input("Numéro du mail? ")
			res = c.get('/home/gritchie/INBOX/' + str(numMail))
			print(res)
			email = input("Voulez-vous sauvegarder le mail en local? 1=oui")
			if email=="1":
				file = open("mail", "w")
				file.write(res)
				file.close()
			print("email sauvé en local")
		elif ans2=="4":
			numTicket = input("Numéro du ticket? ")
			res = c.get('/bin/crypto_helpdesk/ticket/' + str(numTicket))
			print(res)
		elif ans2=="5":
			numTicket = input("Numéro du ticket? ")
			nomPiece = input("Nom de la pièce jointe? ")
			res = c.get('/bin/crypto_helpdesk/ticket/' + str(numTicket) + '/attachment/' + nomPiece)
			print(res)
			pieceJointe = input("Voulez-vous sauvegarder la pièce jointe en mémoire? 1=oui")
			if pieceJointe=="1":
				piece = res
			pieceJointe = input("Voulez-vous sauvegarder la pièce jointe en local? 1=oui")
			if pieceJointe=="1":
				file = open("attachment", "w")
				file.write(res)
				file.close()
		elif ans2=="6":
			aqui = input("A qui? ")
			sujet = input("Sujet? ")
			contenu = input("Contenu? Entrez 999 pour mettre la pièce encryptée 888 pour fichier mémoire")
			if contenu =="999":
				res = 	c.post('/bin/sendmail', to=aqui, subject=sujet, content=pieceEncry)
			elif contenu == "888":
				res = 	c.post('/bin/sendmail', to=aqui, subject=sujet, content=fichierMem)
			else:
				res = 	c.post('/bin/sendmail', to=aqui, subject=sujet, content=contenu)
			print(res)

		elif ans2=="7":
			passwd = input("Entrer la passphrase pour crypto")
			pieceEncry = encrypt(piece, passwd)
		elif ans2=="8":
			numTicket = input("Numéro du ticket? ")
			res = c.post('/bin/crypto_helpdesk/ticket/' + str(numTicket) + '/close', confirm=True)
			print(res)
		elif ans2=="9":
			passwd = input("Entrer la passphrase pour decrypto")
			cipher = input("Entrez le cipher")
			pieceEncry = decrypt(piece, passwd, cipher)
			print(pieceEncry)

		elif ans2=="10":
			numTicket = input("Numéro du ticket? ")
			nomPiece = input("Nom de la pièce jointe? ")
			publicKey = res = c.get('/bin/crypto_helpdesk/ticket/' + str(numTicket) + '/attachment/' + nomPiece)

		elif ans2=="11":
			pieceEncry = encryptPub(piece, publicKey)
			print("La pièce a été encryptée et sauvée en mémoire")
		elif ans2=="12":
			nomUser= input("Nom du user dont vous voulez la Public Key ")
			res = c.get('/bin/finger/' + nomUser)
			print(res)
			publicKey = res
		elif ans2=="13":
			pubkey=""
			with open('public.pem', 'r') as myfile:
				pubkey=myfile.read()
			print(pubkey)
			res = c.put('/home/gritchie/.pk.email.openssl', pubkey)
			print(res)
		elif ans2=="14":
			phrase = input("La phrase à encrypter: ")
			pieceEncry = encryptPub(phrase, publicKey)
			print("La pièce a été encryptée et sauvée en mémoire")

		elif ans2=="15":
			clePrivee = input("Entrez la clé privée symétrique: ")
			cleCryptee = encryptPub(clePrivee, publicKey)
			with open('attachment', 'r') as myfile:
				doc=myfile.read()
			documentCrypte = encrypt(doc, clePrivee)
			dico = {'skey':cleCryptee, 'document':documentCrypte}
			pieceEncry = dico
			print("Le dico a été encrypté et sauvé en mémoire")
		elif ans2=="16":
			fichier = input("Entrez le path du fichier ")
			with open(fichier, 'r') as myfile:
				fichierMem = myfile.read()
			print("Le fichier a été sauvé en mémoire")
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
			pieceJointe = input("Voulez-vous sauvegarder la pièce jointe en local? 1=oui")
			if pieceJointe=="1":
				with open(nomPiece, 'br+') as f:
					f.write(res)
		elif ans2=="20":
			numTicket = input("Numéro du ticket? ")
			nomPiece = input("Nom de la pièce jointe? ")
			res = c.get('/bin/police_hq/ticket/' + str(numTicket) + '/attachment/' + nomPiece)
			res = base64.b64decode(res)
			print(res)
			pieceJointe = input("Voulez-vous sauvegarder la pièce jointe en mémoire? 1=oui")
			if pieceJointe=="1":
				pieceB = res
			pieceJointe = input("Voulez-vous sauvegarder la pièce jointe en local? 1=oui")
			if pieceJointe=="1":
				with open(nomPiece, 'br+') as f:
					f.write(res)
		elif ans2=="21":

			binaire = "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
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
			clair = xorABZ.decode()
			print(clair)
			print("\n**wwwwwwwmmmmmmmmmmmmmmmwwwwww**\n")

		elif ans2=="22":
			numTicket = input("Numéro du ticket? ")
			res = c.post('/bin/police_hq/ticket/' + str(numTicket) + '/close', confirm=True)
			print(res)
		elif ans2=="23":
			delpi_bancaire()
		elif ans2=="24":
			numTicket = input("Numéro du ticket? ")
			connection_kerberos(numTicket)
		elif ans2 !="":
		  print("\n Not Valid Choice Try again")

if __name__ == '__main__':

	c = Connection("http://pac.fil.cool/uglix")

	while True:
		print ("""
		1.Connect as gritchie
		2.Connect as gritchie CHAP
		3.Decoder fichier B64
		4.XOR 2 files
		""")
		ans=input("What would you like to do? ")
		if ans=="1":

			res = c.post('/bin/login', user='gritchie', password="Vt*1fJsM7@")
			print(res)
			connected()
		elif ans =="2":
			dictio = c.get('/bin/login/CHAP')
			challenge = dictio.get("challenge")
			plaintext = "gritchie-" + challenge
			reponse = encrypt(plaintext, "Vt*1fJsM7@")
			res = c.post('/bin/login/CHAP', user='gritchie', response=reponse)
			print(res)
			connected()
		elif ans =="3":
			path = input("Nom du fichier à décoder? ")
			decode64file(path)
			print("Fichier bien décodé")
		elif ans =="4":
			xor2files()
			print("XOR effectué")

		elif ans !="":
		  print("\n Not Valid Choice Try again")
