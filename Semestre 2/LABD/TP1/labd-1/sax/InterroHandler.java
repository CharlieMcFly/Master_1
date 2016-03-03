import org.xml.sax.* ;
import org.xml.sax.helpers.* ;

public class InterroHandler extends DefaultHandler {	
	private int n ;
	private boolean fermante ;
	
	public void startDocument() {this.n = 0 ; this.fermante = false ;}
	
	public void endDocument() {System.out.println() ;}
	
	public void startElement(String nameSpaceURI, 
							 String localName, 
							 String rawName, 
							 Attributes attributs)  {
		if (this.fermante) System.out.print(" , ") ;
		System.out.print(localName + "-" + this.n + "( ") ; 
		this.n++ ;
		this.fermante = false ;
	}
	
	public void endElement(	String nameSpaceURI, 
						   String localName, 
						   String rawName)  {
		System.out.print(" )") ; 
		this.n++ ; 
		this.fermante = true ;       
	}
	
	public static void main(String[] args) {
		try {
			XMLReader saxReader = XMLReaderFactory.createXMLReader();
			saxReader.setContentHandler(new InterroHandler());
			saxReader.parse(args[0]);
		} catch (Exception t) {
			t.printStackTrace();
		}
	}
	
}
