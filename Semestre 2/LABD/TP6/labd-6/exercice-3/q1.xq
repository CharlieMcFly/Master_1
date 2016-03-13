declare function local:getFamilyName($botanicalname, $root){
    for $family in doc($root)//FAMILY
    where $family/SPECIES/text() eq $botanicalname
    return
      <FAMILY>
        {$family/NAME/text()}
      </FAMILY>
};


<CATALOG>
{
let $p := "plant_catalog.xml"
let $f := "plant_families.xml"
for $plant in doc($p)//PLANT
  return
      <PLANT>
        {$plant/COMMON}
        {$plant/BOTANICAL}
        {$plant/ZONE}
        {$plant/LIGHT}
        {$plant/PRICE}
        {local:getFamilyName($plant/BOTANICAL/text(), $f)}
        {$plant/AVAILABILITY}
      </PLANT>
}
</CATALOG>
