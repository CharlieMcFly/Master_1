declare function local:books-by-author ($root, $last, $first) { 
   for $b in $root/book 
   where some $ba in $b/author 
   satisfies ($ba/last = $last and  
              $ba/first=$first) 
   return $b/title  
}; 

let $bib := "biblio.xml"
return
<results> {
let $a := doc($bib)//author 
for $last in distinct-values($a/last), 
$first in distinct-values($a[last=$last]/first) 
order by $last, $first
return <result> 
   <author> <last>{$last}</last>   
   <first>{$first}</first> </author> 
   <number> {count(local:books-by-author(doc($bib)/bib,$last, $first))} </number>
    </result> 
   } 
</results>
