package labd ;

import org.xml.sax.*;
import org.xml.sax.helpers.* ;
import java.io.IOException;

/**
 * @author yves.roos
 *
 * Exemple d'implementation d'un ContentHandler. 
 */
public class LABDHandler extends DefaultHandler {
	
	
	/**
	 * Evenement envoye au demarrage du parse du flux xml.
	 * @throws SAXException en cas de probleme quelquonque ne permettant pas de
	 * se lancer dans l'analyse du document.
	 * @see org.xml.sax.ContentHandler#startDocument()
	 */
	public void startDocument() throws SAXException {
		System.out.println("Debut du document");
	}
	
	/**
	 * Evenement envoye a la fin de l'analyse du flux xml.
	 * @throws SAXException en cas de probleme quelquonque ne permettant pas de
	 * considerer l'analyse du document comme etant complete.
	 * @see org.xml.sax.ContentHandler#endDocument()
	 */
	public void endDocument() throws SAXException {
		System.out.println("Fin du document" );
	}
	
	/**
	 * Evenement recu a chaque fois que l'analyseur rencontre une balise xml ouvrante.
	 * @param nameSpaceURI l'url de l'espace de nommage.
	 * @param localName le nom local de la balise.
	 * @param rawName nom de la balise en version 1.0 <code>nameSpaceURI + ":" + localName</code>
	 * @throws SAXException si la balise ne correspond pas a ce qui est attendu,
	 * comme par exemple non respect d'une dtd.
	 * @see org.xml.sax.ContentHandler#startElement(java.lang.String, java.lang.String, java.lang.String, org.xml.sax.Attributes)
	 */
	public void startElement(String nameSpaceURI, String localName, String rawName, Attributes attributs) throws SAXException {
		System.out.println("Ouverture de la balise : " + localName) ;
		if (attributs.getLength() != 0) System.out.println("  Attributs de la balise : ") ;
		for (int index = 0; index < attributs.getLength(); index++) { // on parcourt la liste des attributs
			System.out.println("     - " +  attributs.getLocalName(index) + " = " + attributs.getValue(index));
		}
	}
	
	/**
	 * Evenement recu a chaque fermeture de balise.
	 * @see org.xml.sax.ContentHandler#endElement(java.lang.String, java.lang.String, java.lang.String)
	 */
	public void endElement(String nameSpaceURI, String localName, String rawName) throws SAXException {
		System.out.println("Fermeture de la balise : " + localName);
	}
	
	/**
	 * Evenement recu a chaque fois que l'analyseur rencontre des caracteres (entre
	 * deux balises).
	 * @param ch les caracteres proprement dits.
	 * @param start le rang du premier caractere a traiter effectivement.
	 * @param length le nombre de caracteres a traiter effectivement
	 * @see org.xml.sax.ContentHandler#characters(char[], int, int)
	 */
	public void characters(char[] ch, int start, int length) throws SAXException {
		String s = new String(ch, start, length).trim() ;
		if (s.length() > 0) System.out.println("     Contenu : |" + s + "|");
	}
	
	/**
	 * Recu chaque fois que des caracteres d'espacement peuvent etre ignores au sens de
	 * XML. C'est a dire que cet evenement est envoye pour plusieurs espaces se succedant,
	 * les tabulations, et les retours chariot se succedants ainsi que toute combinaison de ces
	 * trois types d'occurrence.
	 * @param ch les caracteres proprement dits.
	 * @param start le rang du premier caractere a traiter effectivement.
	 * @param length le nombre de caracteres a traiter effectivement
	 * @see org.xml.sax.ContentHandler#ignorableWhitespace(char[], int, int)
	 */
	public void ignorableWhitespace(char[] ch, int start, int length) throws SAXException {
		System.out.println("espaces inutiles rencontres : ..." + new String(ch, start, length) +  "...");
	}
	
	/**
	 * Rencontre une instruction de traitement.
	 * @param target la cible de l'instruction de traitement.
	 * @param data les valeurs associees a cette cible. En general, elle se presente sous la forme 
	 * d'une serie de paires nom/valeur.
	 * @see org.xml.sax.ContentHandler#processingInstruction(java.lang.String, java.lang.String)
	 */
	public void processingInstruction(String target, String data) throws SAXException {
		System.out.println("Instruction de traitement : " + target);
		System.out.println("  dont les arguments sont : " + data);
	}
	
	
	public static void main(String[] args) {
		try {
			XMLReader saxReader = XMLReaderFactory.createXMLReader();
			saxReader.setContentHandler(new LABDHandler());
			saxReader.parse(args[0]);
		} catch (Exception t) {
			t.printStackTrace();
		}
	}
	
	
}
