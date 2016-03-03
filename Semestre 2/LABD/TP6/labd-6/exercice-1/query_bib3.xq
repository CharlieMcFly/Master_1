let $bib := "biblio.xml"
return
<results> {
let $a := doc($bib)//author
for $last in distinct-values($a/last),
$first in distinct-values($a[last=$last]/first)
order by $last, $first
return
<result><author> <last>{$last}</last>
<first>{$first}</first> </author>
   { for $b in doc($bib)/bib/book
     where some $ba in $b/author
     satisfies ($ba/last = $last and
                $ba/first=$first)
     return $b/title }
      </result>   }
</results>

(:
Explications :

Récupère le nom et le prenom de chaque autheur. Affiche le nom dans la balise last et le prénom dans la balise first.
Ainsi que les titres de cet auteur, ayant le même nom et le même prénom que les valeurs dans les balises le précédent.
:)
