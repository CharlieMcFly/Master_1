declare function local:creationPlant($light, $root){
    for $plant in doc($root)//PLANT
    where $plant/LIGHT/text() eq $light
    return
      <PLANT>
        <COMMON> {$plant/COMMON} </COMMON>
      </PLANT>
};


<CATALOG>
{
let $d := "plant_catalog.xml"
for $light in distinct-values(doc($d)//LIGHT/text()),
  return
      <LIGHT>
        <EXPOSURE> {$light} </EXPOSURE>
        {local:creationPlant($light, $d)}
      </LIGHT>
}
</CATALOG>
