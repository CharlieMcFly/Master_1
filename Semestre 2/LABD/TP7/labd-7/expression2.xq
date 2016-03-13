xquery version "1.0";

declare default element namespace "http://www.expression.org";
declare option saxon:output "omit-xml-declaration=yes";

declare function local:fall($name){
if(count($name)>0) then

	if($name/name() = 'op') then
		if($name/@val = '/') then
			 xs:integer(local:fall($name/*[1]) div local:fall($name/*[2]))
		else(
			if($name/@val = '*') then
			 xs:integer(local:fall($name/*[1]) * local:fall($name/*[2]))
			else(
				if($name/@val = '-') then
				 xs:integer(local:fall($name/*[1]) - local:fall($name/*[2]))
				else(
					if($name/@val = '+') then
						 xs:integer(local:fall($name/*[1]) + local:fall($name/*[2]))
					else(	)
				)
			)
		)
	else(
		if($name/name() = 'var') then
			fn:error(xs:QName("ERROR"), "NaN",$name)
		else($name )
		)
else()

};


declare function local:eval($name as xs:string) as xs:integer{
	 local:fall(doc($name)/expr/op)
};

let $exp := "expression2.xml"

return  concat(local:eval($exp),'
')
