# SVL 1516 - M. Nebut

import cherrypy
import calcul_temperature

PAGE_ACCUEIL = """
<html>
<head>
<title>Accueil</title>
</head>
<body>
<a id='id_lien_temperature' href='/temperature'>Transformateur de température</a>
</body>
</html>
"""

PAGE_TEMPERATURE = """
<html>
<head>
<title>Transformation de températures</title>
</head>
<body>
<form id='id_formulaire_temperature' method='post' action='/temperature'>
<label>Entrez une valeur en Celsius</label>
<input id='id_boite_saisie_temperature' name='valeur_celsius'></input>
</form>
</body>
</html>

"""

PAGE_RESULTAT = """
<html>
<head>
<title>Transformation de températures</title>
</head>
<body>
<form id='id_formulaire_temperature' method='post' action='/temperature'>
<label>Entrez une valeur en Celsius</label>
<input id='id_boite_saisie_temperature' name='valeur_celsius'></input>
<label id='id_response_label'>{message}</label>
</form>
</body>
</html>        
        """


class MonServeur:

    @cherrypy.expose
    def index(self):
        return PAGE_ACCUEIL

    @cherrypy.expose
    def temperature(self, valeur_celsius=None):
        if not valeur_celsius:
            return PAGE_TEMPERATURE
        else:
            return self.page_resultat_conversion(valeur_celsius)
        
    def page_resultat_conversion(self, valeur_celsius):
        try:
            valeur_celsius_int = float(valeur_celsius)
            valeur_farhenheit = calcul_temperature.celsius_to_farhenheit(valeur_celsius_int)
            message_valeur = str(valeur_celsius_int) + " celsius valent " + str(valeur_farhenheit) + " farhenheit"
            return PAGE_RESULTAT.format(message=message_valeur)
        except ValueError:
            return PAGE_RESULTAT.format(message='valeur incorrecte')

        
        
if __name__ == '__main__':
    cherrypy.quickstart(MonServeur())
