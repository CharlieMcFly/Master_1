from subprocess import Popen, PIPE
import base64

# en cas de problème, cette exception est déclenchée
class OpensslError(Exception):
    pass

def gener_key_rsa():

    args = ['openssl', 'genpkey', '-algorithm', "RSA", "-out", "PrivateKey.pem", "-pkeyopt", "rsa_keygen_bits:2048"]
    pipeline = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)

def recup_pk_privatekey():

    # rsa -in maCle.pem -pubout -out maClePublique.pem
    #     openssl pkey -in <fichier contenant la clef secrète> -pubout
    args = ['openssl', 'pkey', '-in', "PrivateKey.pem", "-pubout", '-out', 'PublicKey.pem']
    pipeline = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)

def signer_document(plaintext, secret_key):
            # openssl dgst -sha256 -sign secret_key.pem
    args = ['openssl', 'dgst', '-sha256', '-sign', secret_key]

    if isinstance(plaintext, str):
        plaintext = plaintext.encode()

    pipeline = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    stdout, stderr = pipeline.communicate(plaintext)

    error_message = stderr.decode()
    if error_message != '':
        raise OpensslError(error_message)

    return base64.b64encode(stdout).decode()

def encrypt(plaintext, passphrase, cipher='aes-128-cbc'):

    pass_arg = 'pass:{0}'.format(passphrase)
    args = ['openssl', 'enc', '-' + cipher, '-base64', '-pass', pass_arg]

    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')

    pipeline = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    stdout, stderr = pipeline.communicate(plaintext)

    error_message = stderr.decode()
    if error_message != '':
        raise OpensslError(error_message)

    return stdout.decode()

def encrypt_key(plaintext, file_key, cipher='rsautl'):

    args = ['openssl', cipher, '-encrypt', '-inkey', file_key, '-pubin']

    if isinstance(plaintext, str):
        plaintext = plaintext.encode()

    pipeline = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    stdout, stderr = pipeline.communicate(plaintext)

    error_message = stderr.decode()
    if error_message != '':
        raise OpensslError(error_message)

    return (base64.b64encode(stdout)).decode()

def decrypt(plaintext, passphrase, cipher='aes-128-cbc'):

    # openssl rc2-ofb -d -a -in Fichier_chiffre -pass pass:"ijw_3tX75y" -out secrets.txt.new
    pass_arg = 'pass:{0}'.format(passphrase)
    args = ['openssl', 'enc', '-d', '-'+cipher,'-base64', '-pass', pass_arg]

    # si le message clair est une chaine unicode, on est obligé de
    # l'encoder en bytes() pour pouvoir l'envoyer dans le pipeline vers
    # openssl
    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')

    # ouvre le pipeline vers openssl. Redirige stdin, stdout et stderr
    #    affiche la commande invoquée
    #    print('debug : {0}'.format(' '.join(args)))
    pipeline = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    # envoie plaintext sur le stdin de openssl, récupère stdout et stderr
    stdout, stderr = pipeline.communicate(plaintext)

    # si un message d'erreur est présent sur stderr, on arrête tout
    # attention, sur stderr on récupère des bytes(), donc on convertit
    error_message = stderr.decode()
    if error_message != '':
        raise OpensslError(error_message)

    # OK, openssl a envoyé le chiffré sur stdout, en base64.
    # On récupère des bytes, donc on en fait une chaine unicode
    return stdout.decode()

def decrypt_key(plaintext, file_key):
    # prépare les arguments à envoyer à openssl (inkey cle secret / pubin  )
    # openssl pkeyutl -encrypt -pubin -inkey <fichier contenant la clef publique>
    args = ['openssl', 'pkeyutl', '-decrypt', '-inkey', file_key]

    print("decrypt file")

    if isinstance(plaintext, str):
        plaintext = plaintext.encode('utf-8')

    # ouvre le pipeline vers openssl. Redirige stdin, stdout et stderr
    #    affiche la commande invoquée
    #    print('debug : {0}'.format(' '.join(args)))
    pipeline = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    # envoie plaintext sur le stdin de openssl, récupère stdout et stderr
    stdout, stderr = pipeline.communicate(plaintext)

    # si un message d'erreur est présent sur stderr, on arrête tout
    # attention, sur stderr on récupère des bytes(), donc on convertit
    error_message = stderr.decode()
    if error_message != '':
        raise OpensslError(error_message)

    # OK, openssl a envoyé le chiffré sur stdout, en base64.
    # On récupère des bytes, donc on en fait une chaine unicode
    return base64.b64encode(stdout).decode()

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
