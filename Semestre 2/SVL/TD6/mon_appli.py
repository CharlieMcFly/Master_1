# SVL 1516 - M. Nebut - 02/2016
# CTD6 - test d'acceptation avec Selenium

import cherrypy

PAGE_INDEX = """
<html>
<head>
<title>accueil</title>
</head>
<body>
<a id='id_lien_tranformateur_temperature' href='/temperature'>transformateur de température</a>
</body>
</html>
"""

PAGE_TEMPERATURE = """
<html>
<head>
<title>Transformateur de température</title>
</head>
<body>
<form id='id_formulaire_calcul_temperature' method='post' action='/temperature'>
<input id='id_boite_saisie_valeur_celsius' name='valeur_celsius' type='text'></input>
</form>
</body>
</html>
"""

PAGE_RESULTAT_ERRONE = """
<html>
<head>
<title>Transformateur de température</title>
</head>
<body>
<form id='id_formulaire_calcul_temperature' method="post" action="/temperature">
<input id='id_boite_saisie_valeur_celsius' type='text' name='valeur_celsius'></input>
<label id='id_message_valeur_erronee'>valeur erronée</label>
</form>
</body>
</html>
"""

class MonAppli:

    @cherrypy.expose
    def index(self):
        return PAGE_INDEX

    @cherrypy.expose
    def temperature(self, valeur_celsius=None):
        if valeur_celsius == None:
            return PAGE_TEMPERATURE
        else:
            return self.page_resultat_conversion(valeur_celsius)

    def page_resultat_conversion(self, valeur_celsius):
        return PAGE_RESULTAT_ERRONE

if __name__ == '__main__':
    cherrypy.quickstart(MonAppli())
