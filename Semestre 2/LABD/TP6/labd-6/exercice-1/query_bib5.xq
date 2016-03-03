let $bib := "biblio.xml"
return
<bib>
   {
 for $b in doc($bib)//book
   where count($b/author) > 0
   return
      <book>
      {$b/title}
      { for $a in $b/author[position() <= 2]
        return $a }
      { if (count($b/author) > 2)
        then <et-al/> else () }
  </book>
}
</bib>

(:
Explication :

Recupère tout les livres avec au moins un auteur, affiche le titre de ces auteurs dans une balise book.
Pour les 3 premiers auteurs, on affiche l'auteur et si le nombre d'auteur est supérieur à  2 on met un balise fermante <et-al/>
:)
