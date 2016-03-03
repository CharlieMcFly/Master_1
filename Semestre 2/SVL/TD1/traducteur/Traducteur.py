"""
SVL 1516 - Charlie Q. - CTD1
Zorglang
>>> traducteur = TradZorgland()
>>> traducteur.zorgland("Hello world")
'olleH dlrow'
"""
import unittest
class TradZorglang():

	def zorgland(self, chaine):
		mots = chaine.split(' ')
		envers = ''
		firstWord = True
		for mot in mots :
			res = ''
			for c in mot :
				res =  c + res
			if firstWord :
				firstWord = False
				envers = res
			else :
				envers = envers + ' ' + res
		return envers

class TestTraducteur(unittest.TestCase):
	
	def test_la_chaine_vide_est_traduite_en_chaine_vide(self):
		traducteur = TradZorglang()
		self.assertEqual(traducteur.zorgland(""), "")

	def test_la_chaine_de_taille_1(self):
		traducteur = TradZorglang()
		self.assertEqual(traducteur.zorgland("a"), "a")

	def test_une_chaine_composee_de_lettres_est_retournee(self):
		traducteur = TradZorglang()
		self.assertEqual(traducteur.zorgland("albert"),"trebla")

	def test_une_chaine_composee_de_plusieurs_mots(self):
		traducteur =  TradZorglang()
		self.assertEqual(traducteur.zorgland("Hello World"), "olleH dlroW")