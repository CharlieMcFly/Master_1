import cherrypy

PAGE_INDEX = """
<html>
<head>
<title>Accueil</title>
</head>
<body>
<form id="imc_form" method="get" action="generate">
  Taille : <input id="imc_input" type="text" name="taille"><br>
  <input type="radio" name="sexe" value="homme"> Homme<br>
  <input type="radio" name="sexe" value="femme"> Femme<br>
  <input type="submit" value="Submit">
</form>
</body>
</html>
"""

PAGE_RESULT = """
<html>
<head>
<title>Resultat</title>
</head>
<body>
{0}
<a id='retour_Accueil' href='/index'>Retour à l'Accueil</a>
</body>
</html>
"""

PAGE_RESULTAT_ERRONE = """
<html>
<head>
<title>Erreur</title>
</head>
<body>
<label id='id_message_valeur_erronee'>{0}</label><br/>
<a id='retour_Accueil' href='/index'>Retour à l'Accueil</a>
</body>
</html>
"""


class PoidsIdeal(object):
    """
        Calcul le poids idéal pour un homme ou une femme
    """
    def calculer_poids_ideal(self, taille, sexe):
        if sexe == "homme":
            return taille * 100 - 100 - (taille * 100 - 150) / 4
        else:
            return taille * 100 - 100 - (taille * 100 - 150) / 2.5

    @cherrypy.expose
    def index(self):
        return PAGE_INDEX

    @cherrypy.expose
    def generate(self, **params):
        if 'taille' not in params :
            return self.error("Pas de paramètre taille envoyé")
        if 'sexe' not in params :
            return self.error("Pas de paramètre sexe envoyé")
        taille = params["taille"]
        taille = taille.replace(",", ".")
        try:
            taille = float(taille)
        except ValueError:
            return self.error("Not a float")
        sexe = params['sexe']
        if sexe != "homme" and sexe != "femme":
            return self.error("Paramètre sexe inccorect")
        poids = self.calculer_poids_ideal(float(taille), sexe)
        return PAGE_RESULT.format(str(poids))

    @cherrypy.expose
    def error(self, message):
        return PAGE_RESULTAT_ERRONE.format(message)

if __name__ == '__main__':
    cherrypy.quickstart(PoidsIdeal())
