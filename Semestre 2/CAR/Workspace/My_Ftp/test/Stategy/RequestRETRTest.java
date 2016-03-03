package Stategy;


import static org.mockito.Mockito.mock;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.Socket;

import org.junit.Before;
import org.junit.Rule;
import org.junit.Test;
import org.junit.rules.TemporaryFolder;
import org.mockito.Mockito;

import Client.Client;
import Serveur.DataService;
import Serveur.FtpRequest;
import Strategy.RequestRETR;

public class RequestRETRTest {

	@Rule
    public TemporaryFolder testFolder = new TemporaryFolder();
	

	private FtpRequest ftp;
	private DataService ds;
	private FileInputStream fis;
	private OutputStream out;
	private Socket s;
	private Client c;
	
	@Before
    public void setUp() throws IOException {
		ftp = mock(FtpRequest.class);
		ds = mock(DataService.class);
		fis = mock(FileInputStream.class);
		out = mock(OutputStream.class);
		s = mock(Socket.class);
		c = mock(Client.class);
		
		Mockito.when(ftp.getClient()).thenReturn(c);
		Mockito.when(ftp.getDataService()).thenReturn(ds);
		Mockito.when(ds.openDataStream()).thenReturn(s);
		Mockito.when(s.getOutputStream()).thenReturn(out);
    }
	
	@Test()
	public void testFichierNonTrouve() throws IOException {

		File tempFolder = testFolder.newFolder("folder");
		String [] request = {"RETR", "/fichier.txt"};
		
		Mockito.when(ftp.getServerPath()).thenReturn(tempFolder.getAbsolutePath());
		RequestRETR retr = new RequestRETR();
		
		retr.doRequest(ftp, request);
				
		Mockito.verify(ftp).sendMessage("550 Requested action not taken; file unavailable");	
	}
	
	@Test
	public void testOK() throws IOException {

		File folder = testFolder.newFolder("folder");
		File file = testFolder.newFile("fichier.txt");
		String [] request = {"RETR", "fichier.txt"};
		
		Mockito.when(ftp.getServerPath()).thenReturn("");
		
		RequestRETR retr = new RequestRETR();
		
		retr.doRequest(ftp, request);
		
		Mockito.verify(ftp).sendMessage("150 File status okay; about to open data connection");	
	}

}
