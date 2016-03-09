(: Calcule la somme entre la quantité et le prix :)
declare function local:somme($common, $quantite, $root_c){
    for $plant in doc($root_c)//PLANT
    where $plant/COMMON/text() eq $common
    let $res := xs:integer($quantite) * xs:double(substring($plant/PRICE, 2))
    return
      $res
};

<PRICE>
{
round-half-to-even(
sum(
let $o := "plant_order.xml"
let $d := "plant_catalog.xml"
let $somme := 0
(: Recupere pour chaque plant son common et sa quantite :)
for $plant in doc($o)//PLANT,
    $common in $plant/COMMON/text(),
    $quantite in $plant/QUANTITY/text()
return
    local:somme($common, $quantite, $d)
)
, 2)
}
</PRICE>
