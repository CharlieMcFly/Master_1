import json
import urllib.request
import urllib.parse
import urllib.error
import sys
import base64
from openssl import *
from subprocess import Popen, PIPE
# Ceci est du code Python v3.x (la version >= 3.4 est conseillÃ©e pour une
# compatibilitÃ© optimale).
# --- les admins

class OpensslError(Exception):
    pass

class ServerError(Exception):
    """
    Exception dÃ©clenchÃ©e en cas de problÃ¨me cÃ´tÃ© serveur (URL incorrecte,
    accÃ¨s interdit, requÃªte mal formÃ©e, etc.)
    """
    def __init__(self, code=None, msg=None):
        self.code = code
        self.msg = msg


class Connection:
    """
    Cette classe sert Ã  ouvrir et Ã  maintenir une connection avec le systÃ¨me
    UGLIX. Voir les exemples ci-dessous.

    Pour crÃ©er une instance de la classe, il faut spÃ©cifier une ``adresse de
    base''. Les requÃªtes se font Ã  partir de lÃ , ce qui est bien pratique.
    L'adresse de base est typiquement l'adresse du systÃ¨me UGLIX.

    Cet objet Connection() s'utilise surtout via ses mÃ©thodes get(), post()...

    Il est conÃ§u pour pouvoir Ãªtre Ã©tendu facilement. En dÃ©river une sous-classe
    capable de gÃ©rer des connexions chiffrÃ©es ne nÃ©cessite que 20 lignes de
    code supplÃ©mentaires.

    Exemple :
    >>> c = Connection("http://pac.fil.cool/uglix")
    >>> c.get('/bin/echo')
    'usage: echo [arguments]'
    """
    def __init__(self, base_url):
        self.base = base_url
        # au dÃ©part nous n'avons pas d'identifiant de session
        self.session = None

    def _post_processing(self, result, http_headers):
        """
        Effectue post-traitement sur le rÃ©sultat "brut" de la requÃªte. En
        particulier, on dÃ©code les dictionnaires JSON, et on converti le texte
        encodÃ© en UTF-8 en chaine de charactÃ¨re Unicode. On peut Ã©tendre Cette
        mÃ©thode pour gÃ©rer d'autres types de contenu si besoin.
        """
        if http_headers['Content-Type'] == "application/json":
            return json.loads(result.decode())
        if http_headers['Content-Type'].startswith("text/plain"):
            return result.decode()
        # on ne sait pas ce que c'est : on tel quel
        return result

    def _query(self, url, request, data=None):
        """
        Cette fonction Ã  usage interne est appelÃ©e par get(), post(), put(),
        etc. Elle reÃ§oit en argument une url et un
        """
        try:
            # si on a un identifiant de session, on le renvoie au serveur
            if self.session:
                request.add_header('Cookie', self.session)
            # lance la requÃªte. Si data n'est pas None, la requÃªte aura un
            # corps non-vide, avec data dedans.
            with urllib.request.urlopen(request, data) as connexion:
                # rÃ©cupÃ¨re les en-tÃªtes HTTP et le corps de la rÃ©ponse, puis
                # +ferme la connection
                headers = dict(connexion.info())
                result = connexion.read()

            # si on envoie un identifiant de session, on le stocke
            if 'Set-Cookie' in headers:
                self.session = headers['Set-Cookie']

            # on effectue le post-processing, puis on renvoie les donnÃ©es.
            # c'est fini.
            return self._post_processing(result, headers)

        except urllib.error.HTTPError as e:
            # On arrive ici si le serveur a renvoyÃ© un code d'erreur HTTP
            # (genre 400, 403, 404, etc.). On rÃ©cupÃ¨re le corps de la rÃ©ponse
            # car il y a peut-Ãªtre des explications dedans. On a besoin des
            # en-tÃªte pour le post-processing.
            headers = dict(e.headers)
            message = e.read()
            raise ServerError(e.code, self._post_processing(message, headers)) from None


    def get(self, url):
        """
        Charge l'url demandÃ©e. Une requÃªte HTTP GET est envoyÃ©e.

        >>> c = Connection("http://pac.fil.cool/uglix")
        >>> c.get('/bin/echo')
        'usage: echo [arguments]'

        En cas d'erreur cÃ´tÃ© serveur, on rÃ©cupÃ¨re une exception.
        >>> c.get('/bin/foobar') # doctest: +ELLIPSIS
        Traceback (most recent call last):
        ...
        client.ServerError: (404, ...)
        """
        # prÃ©pare la requÃªte
        request = urllib.request.Request(self.base + url, method='GET')
        return self._query(url, request)


    def post(self, url, **kwds):
        """
        Charge l'URL demandÃ©e. Une requÃªte HTTP POST est envoyÃ©e. Il est
        possible d'envoyer un nombre arbitraire d'arguments supplÃ©mentaires
        sous la forme de paires clef-valeur. Ces paires sont encodÃ©es sous la
        forme d'un dictionnaire JSON qui constitue le corps de la requÃªte.

        Python permet de spÃ©cifier ces paires clef-valeurs comme des arguments
        nommÃ©s de la mÃ©thode post(). On peut envoyer des valeurs de n'importe
        quel type sÃ©rialisable en JSON.

        >>> c = Connection("http://pac.fil.cool/uglix")
        >>> c.post('/bin/echo', string_example="toto", list_example=[True, 42, {'foo': 'bar'}])
        {'content_found': {'string_example': 'toto', 'list_example': [True, 42, {'foo': 'bar'}]}}
        """
        # prÃ©pare la requÃªte
        request = urllib.request.Request(self.base + url, method='POST')
        data = None
        # kwds est un dictionnaire qui contient les arguments nommÃ©s. S'il
        # n'est pas vide, on l'encode en JSON et on l'ajoute au corps de la
        # requÃªte.
        if kwds:
            request.add_header('Content-type', 'application/json')
            data = json.dumps(kwds).encode()
        return self._query(url, request, data)


    def put(self, url, content):
        """
        Charge l'URL demandÃ©e avec une requÃªte HTTP PUT. L'argument content
        forme le corps de la requÃªte. Si content est de type str(), il est
        automatiquement encodÃ© en UTF-8. cf /doc/strings pour plus de dÃ©tails
        sur la question.
        """
        request = urllib.request.Request(self.base + url, method='PUT')
        if type(content) == str:
            content = content.encode()
        return self._query(url, request, data=content)


    def post_raw(self, url, data, content_type='application/octet-stream'):
        """
        Charge l'url demandÃ©e avec une requÃªte HTTP POST. L'argument data
        forme le corps de la requÃªte. Il doit s'agir d'un objet de type
        bytes(). Cette mÃ©thode est d'un usage plus rare, et sert Ã  envoyer des
        donnÃ©es qui n'ont pas vocation Ã  Ãªtre serialisÃ©es en JSON (comme des
        donnÃ©es binaires chiffrÃ©es, par exemple).

        Principalement utilisÃ© pour Ã©tendre le client et lui ajouter des
        fonctionnalitÃ©.
        """
        request = urllib.request.Request(self.base + url, method='POST')
        request.add_header('Content-type', content_type)
        return self._query(url, request, data)

import sys
import time
import json
class Main:

    def __init__(self, c):
        if c == None :
            self.c = Connection("http://pac.fil.cool/uglix")
        else :
            self.c = c

# CONNECTION

    def connection_guest(self):
        print("Connection en cours ...")
        self.c.post('/bin/login', user="guest", password="guest")
        print(self.c.get("/home/guest"))
        self.afficher_menu()

    def connection_gritchie(self):
        print("Connection en cours ...")
        self.c.post('/bin/login', user="gritchie", password="Vt*1fJsM7@")
        print(self.c.get("/home/gritchie"))
        self.afficher_menu()

    def connection_securise_gritchie(self):
        print("Connection en cours ...")
        challenge = self.c.get("/bin/login/CHAP")
        plaintext = "gritchie-"+challenge["challenge"]
        result = encrypt(plaintext, 'Vt*1fJsM7@', 'aes-128-cbc')
        print(self.c.post('/bin/login/CHAP', user="gritchie", response=result))
        self.afficher_menu()

# MENU

    def afficher_menu(self):
        rep = None
        while rep == None :
            print("----- Menu -----\n 1- Mail \n 2- Helpdesk \n 3- Police")
            rep = input("Entrez l'action choisis : ")
        if rep == '1' :
            self.action_mail()
        if rep == '2' :
            self.action_helpdesk()
        if rep == '3' :
            self.action_police()

# ACTION

    def action_police(self):
        print(self.c.get("/bin/police_hq"))
        input("Entrer to continue")
        print("------ Menu Police -----\n 1- Lire Ticket")
        a = input("Entrer un choix : ")
        if a == "1" :
            b = input("Entrer le numero de ticket :")
            self.action_police_ticket(b)



    def action_mail(self):
        print(self.c.get("/home/gritchie/INBOX"))
        input("Entrer to continue")
        print("----- Menu MAIL -----\n 1- Lire Mail \n 2- Envoyer Mail \n 3- Signer Fichier\n 0- Retour Menu \n----------------")
        rep = input("Entrez l'action choisis : ")
        if rep == "1" :
            a = input("Entrez le mail à lire : ")
            print(self.c.get("/home/gritchie/INBOX/"+a+""))
            input("Entrer to continue")
            self.action_mail()
        if rep == "2":
            to = input("Entrer le destinataire : ")
            subject = input("Entrer le sujet : ")
            content = input("Entrer le message : ")
            self.send_mail(to, subject, content)
            input("Entrer to continue")
            self.action_mail()
        if rep == "3" :
            self.signer_doc()
        if rep == "0" :
            self.afficher_menu()

    def send_mail(self, to, subject, content):
        print("Envoie de mail")
        print(self.c.post('/bin/sendmail', to=to, subject=subject,content=content))

    def action_helpdesk(self):
        print(self.c.get("/bin/crypto_helpdesk"))
        input("Enter to continue ")
        print("----- Menu HELP -----\n 1- Lire Ticket \n 2- Clore Ticket\n 0- Retour Menu \n----------------")
        rep = input("Entrez l'action choisis : ")
        if rep == "1" :
            a = input("Entrez le ticket à lire : ")
            self.action_ticket(a)
            input("Enter to continue")
            self.action_helpdesk()
        if rep == "2":
            ticket = input("Entrer le ticket à clore : ")
            print(self.c.post('/bin/crypto_helpdesk/ticket/'+ticket+'/close', confirm=True))
            input("Entrer to continue")
            self.action_helpdesk()
        if rep == "0":
            self.afficher_menu()

#Police Ticket

    def action_police_ticket(self, ticket):
        print(self.c.get("/bin/police_hq/ticket/"+ticket))
        input("Enter to continue")
        self.connection_kerberos(ticket)
        self.test_request()

    def connection_kerberos(self, ticket):
            # Authentification service
            dic = self.c.post('/bin/kerberos/authentication-service', username="gritchie")
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
            dic2 = self.c.post('/bin/kerberos/ticket-granting-service', TGT=tgt, service="hardware", authenticator=auth)
            sesskey = dic2['Client-Server-session-key']
            servtick = dic2['Client-Server-ticket']
            cle = decrypt(sesskey, pw)
            #  Connection service
            d2 = {'username': 'gritchie', 'timestamp': time.time()}
            e2 = json.dumps(d2)
            auth2 = encrypt(e2, cle)
            serv = self.c.post('/service/hardware/hello', ticket=servtick, authenticator=auth2)
            print(serv)


    def test_request(self):
            #  REQUEST
            a = '{"url": "/bin/get", "method": "GET"}'
            data = encrypt(a, "debug-me")
            res = self.c.post_raw('/bin/test-gateway', data)
            print(res)

#TICKET
    def action_ticket(self, n):
        print(self.c.get("/bin/crypto_helpdesk/ticket/"+n))
        # Clore le ticket
        print("-------Menu Ticket n°"+n+"----- \n 1 - Attachement \n 2 - Crypter Fichier \n 3 - Decrypter Fichier\n 0 - Retour")
        a = input("Votre choix : ")
        # Voir les attachment d'un ticket
        if a == '1' :
            self.afficher_attachment(n)
            self.action_ticket(n)
        if a == '2' :
            self.chiffre_menu(n)
        if a == '0' :
            self.action_helpdesk()

    def afficher_attachment(self, n):
        string = input("Entrez le nom de l'attachment :")
        print(self.c.get("/bin/crypto_helpdesk/ticket/"+n+"/attachment/"+string))

# Chiffrer / Dechiffrer un document

    def chiffre_menu(self, ticket):
        print("---- Menu Chiffrage ----- \n 1- Chiffrement avec Password \n 2- Chiffrement avec Public Key RSA \n 3- Génération de clé \n 4- Recupérer Clé Public \n 0-  Retour")
        a = input("Entrer votre choix : ")
        if a == "1" :
            self.chiffre_doc(ticket)
        if a == "2" :
            self.chiffrer_avec_public_key(ticket)
        if a == "3" :
            self.generer_cle_rsa()
        if a == "4" :
            self.recuperer_cle_pub_de_cle_priv()
        if a == "0" :
            self.action_ticket(ticket)

    def chiffre_doc(self, ticket):
        a = input("Fichier : un attachment (0) un text (1) ")
        if a == "0" :
            f = input("Entrez le nom du fichier :")
            fichier = self.c.get("/bin/crypto_helpdesk/ticket/"+ticket+"/attachment/"+f)
        if a == "1" :
            fichier = input("Entrez le texte devant etre chiffrer : ")
        b = input("Passphrase : Attachement (0) Manuelle (1) ")
        if b == '0' :
            password = self.c.get("/bin/crypto_helpdesk/ticket/"+ticket+"/attachment/password")
        if b == '1' :
            password = input("Entrer une passphrase : ")
        result = encrypt(fichier, password)
        with open("fichier_crypter.pem", "w") as f:
                f.write(result)
        print(result)
        self.chiffre_menu(ticket)


    def chiffrer_avec_public_key(self, ticket):
        a = input("Clé : Attachement (0) Finger (1) : ")
        if a == "0":
            key = self.c.get("/bin/crypto_helpdesk/ticket/"+ticket+"/attachment/public-key")
            with open("public_key.pem", "w") as f:
                f.write(key)
        if a == "1":
            self.afficher_attachment(ticket)
            b = input("Entrer le nom du user : ")
            with open("public_key.pem", "w") as f:
                f.write(self.c.get("/bin/finger/"+b+"/pk"))

        b = input("Chiffrer : un attachment (0) un text (1) fichier (2) : ")
        if b == "0" :
            f = input("Entrez le nom du fichier :")
            fichier = self.c.get("/bin/crypto_helpdesk/ticket/"+ticket+"/attachment/"+f)
        if b == "1" :
            fichier = input("Entrez le texte devant etre chiffrer : ")
        if b == "2" :
            c = input("Entrer le fichier à crypter : ")
            monf = open(c, "r")
            fichier = monf.read()
        result = encrypt_key(fichier, "public_key.pem")
        print(result)

    def generer_cle_rsa(self):
        pass
        # gener_key_rsa()
        # f = open("PrivateKey.pem", "r")
        # fichier = f.read()
        # print(fichier)

    def recuperer_cle_pub_de_cle_priv(self):
        # recup_pk_privatekey
        f = open("PublicKey.pem", "r")
        fichier = f.read()
        self.c.put("/home/gritchie/.pk.email.openssl", fichier)

    def signer_doc(self):
        document = self.c.get("/home/gritchie/INBOX/3903/body")
        content = signer_document(document, "PrivateKey.pem")
        print(content)
        self.send_mail('osinski.marva', "Contrat signer", content)

    # def test(self):
    #     # Clé = azerty
    #     dic = {}
    #     dic["skey"] = "wiAcQTkLDkSqLAolWuoACMAhzJ3MQIWdskFE5uPyuRwrmG+tx9q0OgbWRRkCNWhBMdb+J624A1Ksd0xMk7grY+aSUl+7b4AYxwcMuJe15ToQne5G+aC1i4E2u0Iakd8d4/QQQljllIuuaegutortr41zUfo5dM+NXKSi2p0QPYQ="
    #     f = open("fichier_crypter.pem", "r")
    #     dic["document"] = f.read()
    #     to = self.c.get("/bin/crypto_helpdesk/ticket/317/attachment/client")['email']
    #     subject = input("Entrer le sujet : ")
    #     content = dic

#  A FORMATTER
    # def dechiffre_doc(self, ticket):
    #     b = input("Dechiffre avec clé RSA ? 0/1 : " )
    #     if b == '1':
    #         self.dechiffrement_doc_avec_key("3890", ticket)
    #     a = self.c.get("/bin/crypto_helpdesk/ticket/"+ticket+"/attachment/client")
    #     to = a["email"]
    #     f = input("Entrez le nom du fichier à decrypter : ")
    #     fichier_c = self.c.get("/bin/crypto_helpdesk/ticket/"+ticket+"/attachment/"+f)
    #     password = self.c.get("/bin/crypto_helpdesk/ticket/"+ticket+"/attachment/password")
    #     method_cipher = self.c.get("/bin/crypto_helpdesk/ticket/"+ticket+"/attachment/cipher")
    #     print(method_cipher)
    #     content = decrypt(fichier_c, password, method_cipher)
    #     print(content)
    #     self.close_ticket(ticket, to, content, "Decription du fichier")

    # def dechiffrement_doc_avec_key(self, mail, ticket):
    #     # fichier = self.c.get("/home/gritchie/INBOX/3892/body")
    #     # print(fichier)
    #     # fichier = base64.b64decode(fichier)
    #     # print(fichier)
    #     # fichier = decrypt_key(fichier, "PrivateKey.pem")
    #     # fichier = base64.b64decode(fichier)
    #     # print(fichier)
    #     # fichier = fichier.decode()
    #     # print(fichier)

    #     a = self.c.get("/bin/crypto_helpdesk/ticket/"+ticket+"/attachment/client")
    #     to = a['email']
    #     subject = "Ticket n°"+ticket
    #     # print(self.c.post('/bin/sendmail', to=to, subject=subject,content=fichier))
    #     self.close_ticket(ticket, to, subject, "hey")

    # def mail_197(self, ticket):
    #     a = self.c.get("/bin/crypto_helpdesk/ticket/"+ticket+"/attachment/contact")
    #     subject = "D'aide ticket n°"+ticket
    #     content = "informations sensibles"
    #     with open("public_key_alice.pem", "w") as f:
    #         f.write(self.c.get("/bin/finger/"+a+"/pk"))
    #     # Fichier à chiffrers
    #     result = encrypt_key(content, "public_key_alice.pem")
    #     # Génerer une clé privé rsa
    #     # gener_key_rsa()
    #     # Extraire la partie publique
    #     # recup_pk_privatekey()
    #     # recupérer la clé publiquee du fichier
    #     # f = open("PublicKey.pem","r")
    #     # fichier = f.read()
    #     # # Mettre la clé publique de cette clé dans le dossier openssl
    #     # print(self.c.put('/home/gritchie/.pk.email.openssl', fichier))
    #     print(self.c.post('/bin/sendmail', to=a, subject=subject, content=result))
    #     self.action_mail()

    # def mail_198(self, ticket):
    #     a = self.c.get("/bin/crypto_helpdesk/ticket/"+ticket+"/attachment/contact")
    #     subject = "D'aide ticket n°"+ticket
    #     content = self.c.get("/bin/crypto_helpdesk/ticket/"+ticket+"/attachment/reciprocity")
    #     with open("public_key_alice.pem", "w") as f:
    #         f.write(self.c.get("/bin/finger/"+a+"/pk"))
    #     result = encrypt_key(content, "public_key_alice.pem")
    #     print(self.c.post('/bin/sendmail', to=a, subject=subject, content=result))

    def test(self):
        correct = True

        res = self.c.get('/bin/police_hq')
        print(res)

        res = self.c.get('/bin/police_hq/ticket/317')
        print(res)

        email = self.c.get('/bin/police_hq/ticket/317/attachment/client')["email"]

        lots = self.c.get('/bin/banks/forensics')

        identifiant = lots["identifier"]
        cards_data = lots["card-numbers"]

        print(lots)

        status = []

        print(len(cards_data))

        for card_number in cards_data :


            correct = True

            print("\n")
            card_data = self.c.get('/bin/banks/card-data/' + card_number)
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
            file_key.write(self.c.get('/bin/banks/CA'))
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

            """
            bb = base64.b64decode(bank_signature)
            file_key6 = open('bank_signature.bin', 'wb')
            file_key6.write(bb)
            file_key6.close()

            file_key7 = open('bank_publickey.pem', 'w')
            file_key7.write(bank_publickey)
            file_key7.close()
            """

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


        print("MAIL")
        message = {"identifier":identifiant,"statuses":status}
        res = self.c.post('/bin/sendmail', to=email, subject='fermeture ticket', content=message )
        print(res)


if __name__ == '__main__':
    main = Main(Connection("http://pac.fil.cool/uglix"))
    print("-----Connection-----\n 0 - Visiteur \n 1 - Gritchie \n 2 - Gritchie CHAP")
    p = input("Votre Choix : ")
    if p == '1':
        main.connection_gritchie()
    if p == '0':
        main.connection_guest()
    if p == '2':
        main.connection_securise_gritchie()
