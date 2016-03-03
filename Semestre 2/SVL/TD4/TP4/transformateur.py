"""
  class Lecteur de fichier de log
"""

import re
class Transformateur:

    def __init__(self, lecteur, redacteur):
        self.lecteur = lecteur
        self.redacteur = redacteur

    def filter_message(self, messages):
        list_msg = []
        if len(messages) == 0 :
            return list_msg
        for m in messages:
            if m.priorite > 5:
                list_msg.append(m)
        return list_msg

class Message:

    def __init__(self, date, priorite, contenu):
        self.date = date
        self.priorite = priorite
        self.contenu = contenu


class Lecteur:

    def __init__(self, flux, messages):
        self.flux = flux
        self.fabrique_message = messages

    """
    Teste si la ligne est formater correctement
    cad "2002-12-22, 5, error\n"
    """
    def valid_ligne(self, ligne):

        l = ligne.split(", ")
        if len(l) != 3 :
            raise FormatLigneError()
        date = l[0].strip()
        testdate = re.match('(\d{4})-(\d{2})-(\d{2})$', date)
        if testdate == None :
            raise DateFormatError()
        priorite = l[1]
        testprio = re.match('[1]?[0-9]$', priorite)
        if testprio == None :
            raise PrioriteError()
        priorite = int(priorite)
        content = l[2].rstrip()
        return self.fabrique_message.creer_msg(date, priorite, content)

    """
    Lit les lignes d'un fichier
    """
    def lire_fichier(self):
        messages = []
        lignes = self.flux.readlines()
        for ligne in lignes:
            msg = self.valid_ligne(ligne)
            messages.append(msg)
        return messages

class FormatLigneError(Exception):
    pass

class FichierVideError(Exception):
    pass

class DateFormatError(Exception):
    pass

class PrioriteError(Exception):
    pass
