import org.xml.sax.XMLReader;
import org.xml.sax.helpers.XMLReaderFactory;


public class Main {

	public static void main(String[] args) {
		try {
			XMLReader saxReader = XMLReaderFactory.createXMLReader();
			saxReader.setContentHandler(new MyHandler());
			saxReader.parse("./maisons.xml");
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
}
