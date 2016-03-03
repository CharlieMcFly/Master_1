def test():
    correct = True

    res = c.get('/bin/police_hq')
    print(res)

    res = c.get('/bin/police_hq/ticket/311')
    print(res)

    email = c.get('/bin/police_hq/ticket/311/attachment/client')["email"]

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



##############
dans openssl
##############


def verifyCert(plaintext, file_trusted_certi = '', file_untrusted_certi = ''):

    args = ['openssl', 'verify']
    if file_trusted_certi != '':
        args = ['openssl', 'verify', '-trusted', file_trusted_certi]
    if file_untrusted_certi != '':
        args = ['openssl', 'verify', '-trusted', file_trusted_certi, '-untrusted', file_untrusted_certi]

    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')

    pipeline = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    stdout, stderr = pipeline.communicate(plaintext)

    error_message = stderr.decode()
    if error_message != '':
        raise OpensslError(error_message)

    return stdout.decode()

def getCertifName(plaintext):
    args = ['openssl', 'x509', '-subject', '-noout']
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')

    pipeline = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    stdout, stderr = pipeline.communicate(plaintext)

    error_message = stderr.decode()
    if error_message != '':
        raise OpensslError(error_message)

    return stdout.decode()


def getPublicKeyFromCerti(plaintext):
    args = ['openssl', 'x509', '-pubkey', '-noout']
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')

    pipeline = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    stdout, stderr = pipeline.communicate(plaintext)

    error_message = stderr.decode()
    if error_message != '':
        raise OpensslError(error_message)

    return stdout.decode()

def consultCertif(plaintext):
    args = ['openssl', 'x509', '-text', '-noout']
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')

    pipeline = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    stdout, stderr = pipeline.communicate(plaintext)

    error_message = stderr.decode()
    if error_message != '':
        raise OpensslError(error_message)

    return stdout.decode()

def sign(plaintext, filename = 'myPrivateKey'):
    args = ['openssl', 'dgst', '-sha256', '-sign', filename]
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')

    pipeline = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    stdout, stderr = pipeline.communicate(plaintext)

    error_message = stderr.decode()
    if error_message != '':
        raise OpensslError(error_message)

    return base64.b64encode(stdout).decode()

def verifSign(plaintext, publickey, signedFile):
    args = ['openssl', 'dgst', '-sha256', '-verify', publickey, '-signature', signedFile]
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')

    pipeline = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    stdout, stderr = pipeline.communicate(plaintext)

    error_message = stderr.decode()
    if error_message != '':
        raise OpensslError(error_message)

    return stdout.decode()
