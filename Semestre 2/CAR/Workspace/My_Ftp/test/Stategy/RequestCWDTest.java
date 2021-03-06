package Stategy;

import static org.mockito.Mockito.mock;

import java.io.File;
import java.io.IOException;

import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.TemporaryFolder;
import org.mockito.Mockito;

import Client.Client;
import Serveur.FtpRequest;
import Strategy.Request;
import Strategy.RequestCWD;

public class RequestCWDTest {
	
	@Rule
    public TemporaryFolder tmpFolder = new TemporaryFolder();

	@Test
	public void testSansArgument() {
	
		FtpRequest ftp = mock(FtpRequest.class);
		String [] request = {"CWD", ""};
		
		RequestCWD cwd = new RequestCWD();
		cwd.doRequest(ftp, request);
				
		Mockito.verify(ftp).sendMessage("501 Syntax error in parameters");
	}
	
	@Test
	public void testRetour() {
		FtpRequest ftp = mock(FtpRequest.class);
		String [] request = {"CWD", ".."};
		
		RequestCWD cwd = new RequestCWD();
		cwd.doRequest(ftp, request);
				
		Mockito.verify(ftp).sendMessage("550 No access to parent folder");
	}
	
	@Test
	public void testCDFichier() throws IOException {
		FtpRequest ftp = mock(FtpRequest.class);
		String [] request = {"CWD", "/fichier"};
		Client c = mock(Client.class);
		
		File folder = tmpFolder.newFolder("dossier");
		File file = tmpFolder.newFile("dossier/fichier");

		Mockito.when(ftp.getClient()).thenReturn(c);
		Mockito.when(c.getPathname()).thenReturn(folder.getAbsolutePath());	
		
	
		RequestCWD cwd = new RequestCWD();
		cwd.doRequest(ftp, request);
		
		Mockito.verify(ftp).sendMessage("550 Cannot go into a file (CWD on file)");
	}
	
	@Test
	public void testDossierInexistant() throws IOException {
		FtpRequest ftp = mock(FtpRequest.class);
		String [] request = {"CWD", "/dossierInexistant"};
		Client c = mock(Client.class);
		
		File folder = tmpFolder.newFolder("dossier");
	
		Mockito.when(ftp.getClient()).thenReturn(c);
		Mockito.when(c.getPathname()).thenReturn(folder.getAbsolutePath());	
		
	
		RequestCWD cwd = new RequestCWD();
		cwd.doRequest(ftp, request);
				
		Mockito.verify(ftp).sendMessage("550 No such directory");
	}
	
	@Test
	public void testCWDOk() throws IOException {
		FtpRequest ftp = mock(FtpRequest.class);
		String [] request = {"CWD", "/fichier"};
		Client c = mock(Client.class);
		

		File folder = tmpFolder.newFolder("dossier");
		(new File(folder.getAbsolutePath() + "/fichier")).mkdirs();


		Mockito.when(ftp.getClient()).thenReturn(c);
		Mockito.when(c.getPathname()).thenReturn(folder.getAbsolutePath());	
		
	
		RequestCWD cwd = new RequestCWD();
		cwd.doRequest(ftp, request);
				
		Mockito.verify(ftp).sendMessage("250 CWD command successfull");
	}
	


}
