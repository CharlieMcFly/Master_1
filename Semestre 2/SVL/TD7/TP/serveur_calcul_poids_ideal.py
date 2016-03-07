import cherrypy
import poids_ideal

PAGE_INDEX = """
<html>
<head>
<title>Calcul du poids idéal</title>
</head>
<body>
<form id="formulaire_poids_ideal" method="post" action="/poids_ideal">
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
<a id='retour_poids_ideal' href='/index'>Retour au Calcul du poids idéal</a>
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
<a id='retour_poids_ideal' href='/index'>Retour à l'Accueil</a>
</body>
</html>
"""

class MonServeur:(object):

        @cherrypy.expose
        def index(self):
            return PAGE_INDEX

        @cherrypy.expose
        def poids_ideal(self, **params):
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
            poids = calculer_poids_ideal(float(taille), sexe)
            return PAGE_RESULT.format(str(poids))

        @cherrypy.expose
        def error(self, message):
            return PAGE_RESULTAT_ERRONE.format(message)

    if __name__ == '__main__':
        cherrypy.quickstart(PoidsIdeal())
