
def calculer_poids_ideal(self, taille, sexe):
    if sexe == "homme":
        return taille * 100 - 100 - (taille * 100 - 150) / 4
    else:
        return taille * 100 - 100 - (taille * 100 - 150) / 2.5
