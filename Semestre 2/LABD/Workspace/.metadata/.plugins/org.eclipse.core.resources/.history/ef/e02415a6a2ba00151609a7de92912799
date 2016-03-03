package labd ;

import org.xml.sax.XMLReader ;
import org.xml.sax.helpers.XMLReaderFactory ;


/**
 *  Analyseur XML pour une validation par rapport a une DTD.
 *  La validation se fait à la volée, en lisant le document.
 *  C'est un analyseur SAX -> On ne construit pas l'arbre DOM du document.
 *
 */
public class XMLParser {

  /**
   *  Methode de validation : Executer "java XMLParser leDocumentAValider.xml"
   *  On vérifie que le document est conforme a la DTD qui lui est liée
   *
   *@param  args           ligne de commande = le nom du fichier XML à valider
   *@exception  Exception  Si probleme lors de la creation des objets.
   */
  public static void main(String[] args) {
    try {
      XMLReader saxReader = XMLReaderFactory.createXMLReader(); //comme avant
      saxReader.setFeature("http://xml.org/sax/features/validation", true); // c'est la la nouveaute
      //saxReader.setContentHandler(new MonHandlerAMoi());// si on veut
      saxReader.parse(args[0]); 
    } catch (Exception t) {
      t.printStackTrace();
    }
   }
}
 