declare function local:getFamilyName($botanicalname, $root){
    for $family in doc($root)//FAMILY
    where $family/SPECIES/text() eq $botanicalname
    return
      <FAMILY>
        {$family/NAME/text()}
      </FAMILY>
};

declare function local:creationPlant($light, $root, $families){
    for $plant in doc($root)//PLANT
    where $plant/LIGHT/text() eq $light
    order by $plant/COMMON ascending
    return
      <PLANT>
        {$plant/COMMON}
        {$plant/BOTANICAL}
        {$plant/ZONE}
        {$plant/PRICE}
        {local:getFamilyName($plant/BOTANICAL/text(), $families)}
        {$plant/AVAILABILITY}
      </PLANT>
};

<CATALOG>
{
let $d := "plant_catalog.xml"
let $f := "plant_families.xml"
for $light in distinct-values(doc($d)//LIGHT/text())
order by $light ascending
  return
      <LIGHT>
        <EXPOSURE> {$light} </EXPOSURE>
        {local:creationPlant($light, $d, $f)}
      </LIGHT>
}
</CATALOG>
